import asyncio
import logging
import time

import config
from discovery.notify import SchemaNotifier
from discovery.registry import schemas
from discovery.registry.schemas import _add_schema_class
from discovery.model import Schema
from discovery.utils.adapters import get_latest_schema_org_version
from discovery.registry.common import RegistryError

logger = logging.getLogger(__name__)


def _notify(action, **details):
    """Send a SchemaNotifier message from sync code. Never raises."""
    try:
        asyncio.run(getattr(SchemaNotifier(config), action)(**details))
    except Exception:
        logger.exception(f"failed to send '{action}' notification")


def schema_update(namespace, notify=True):
    """ Update registered schemas by namespace.
        To run a schema update manually:
        from discovery.utils.update import schema_update
        schema_update(namespace="n3c")

        Returns the error message if the update failed, otherwise None.
        notify=False skips the per-schema Slack alert, so a caller
        updating many schemas can send one summary instead.
    """
    logger.info(f"starting updating process for {namespace} schema")
    try:
        meta = schemas.get_meta(namespace)
        # deliberately does not pass a user: a content refresh must not be
        # able to reassign ownership. See registry.schemas.transfer_ownership.
        count = schemas.update(namespace, url=meta["url"])
        status = Schema.get(id=namespace)._status
        if not isinstance(count, int):
            # schemas.update records a RegistryError in _status instead of raising
            raise RegistryError(status.refresh_msg)
    except Exception as e:
        logger.exception(f'update of {namespace} schema failed')
        error = str(e) or type(e).__name__
        if notify:
            _notify("update_failed", namespace=namespace, error=error)
        return error
    else:
        # only failures are sent to slack; successful updates are just logged
        if status.refresh_status == 299:
            # 299 is only set when new content was fetched and saved
            logger.info(f'update of {namespace} schema complete')
        else:
            logger.info(f'{namespace} schema already at latest version')


def daily_schema_update():
    """ Daily schema updates.
    Gather a list of schemas, and update schemas
    by namespace
    """
    excluded_namespace = ['schema']
    start = time.process_time()
    schema_count = 0
    failures = {}
    job_error = None
    try:
        for schema in Schema.search().scan():
            if schema.meta.id not in excluded_namespace:
                error = schema_update(schema.meta.id, notify=False)
                schema_count += 1
                if error:
                    failures[schema.meta.id] = error
    except Exception as e:
        # e.g. elasticsearch is down, so the schema list can't be read
        logger.exception(f'daily schema update stopped after {schema_count} schemas')
        job_error = str(e) or type(e).__name__
    if failures or job_error:
        # one summary per run, not one message per failing schema
        _notify("update_failed_summary", failures=failures, total=schema_count, job_error=job_error)
    total_time = time.process_time() - start
    logger.info(f'update process complete, total processing time was {total_time} seconds for {schema_count} schemas')


def monthly_schemaorg_update():
    """ Monthly schema.org schema update.
    Validates the newer schema.org schema using biothings_schema package
    before any update. If validation fails, DDE schema.org is not updated.

    To run manually:
        from discovery.utils.update import monthly_schemaorg_update
        monthly_schemaorg_update()
    """
    logger.info("Starting monthly schema.org update process")
    start = time.process_time()


    # Get current schema.org version stored in DDE
    current_version = schemas.get_stored_schema_org_version()
    logger.info(f"Current schema.org version in DDE: {current_version}")

    # Get the latest available schema.org version from biothings_schema
    latest_version = get_latest_schema_org_version()
    logger.info(f"Latest schema.org version available: {latest_version}")

    # Check if update is needed. The stored version lives on the Schema
    # index's mapping metadata, which is separate from the actual class
    # documents in the SchemaClass index. If those documents were ever lost
    # (index reset, migration, etc.) without the version metadata being
    # cleared, a version match here would wrongly skip reloading schema.org.
    if current_version == latest_version and schemas.exists("schema"):
        logger.info("Schema.org is already at the latest version. No update needed.")
        return
    elif current_version == latest_version:
        logger.warning(
            "Stored schema.org version matches latest, but no schema.org "
            "classes are indexed. Reloading schema.org to repair the index."
        )

    # Validate by performing a dry-run before actual update
    logger.info(f"Validating schema.org version {latest_version} (dry-run)...")
    try:
        class_count = _add_schema_class(None, "schema", dryrun=True, schema_org_version=latest_version)
        logger.info(f"Validation passed - {class_count} schema classes validated")
    except (AttributeError, RegistryError) as exc:
        if hasattr(exc, 'status_code'):
            logger.error(f"Status code: {exc.status_code}")
        logger.exception(f"Validation failed for schema.org version {latest_version}. DDE schema.org will not be updated.")
        _notify(
            "update_failed",
            namespace="schema",
            error=f"schema.org {latest_version} failed validation, DDE schema.org was not updated.\n{exc}",
        )
        return

    # Validation passed - perform the actual update
    logger.info(f"Updating schema.org from {current_version} to {latest_version}")
    try:
        schemas.add_core(update=True, schema_org_version=latest_version)
    except Exception as exc:
        logger.exception(
            f"Update failed while reloading schema.org version {latest_version}. "
            "DDE schema.org may be left in a partially updated state."
        )
        _notify(
            "update_failed",
            namespace="schema",
            error=f"Reloading schema.org {latest_version} failed, DDE schema.org may be partially updated.\n{exc}",
        )
        return

    # Verify the update
    new_version = schemas.get_stored_schema_org_version()
    if new_version == latest_version:
        logger.info(f"Update verified - schema.org is now at version {new_version}")
        # a reload at the same version only repairs missing classes; don't notify for it
        if current_version != new_version:
            _notify("schemaorg_update", old_version=current_version, new_version=new_version, num_classes=class_count)
    else:
        logger.warning(f"Version mismatch: expected {latest_version}, got {new_version}")
        _notify(
            "update_failed",
            namespace="schema",
            error=f"schema.org version mismatch after update: expected {latest_version}, got {new_version}",
        )

    total_time = time.process_time() - start
    logger.info(f'Monthly schema.org update complete, processing time: {total_time:.2f} seconds')
