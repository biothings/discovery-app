"""
Slack notifications for the scheduled schema updates.

Two levels, neither of which needs Elasticsearch or Slack:
  - message content: SchemaNotifier methods with broadcast mocked
  - when a message is sent: discovery.utils.update with _notify and the
    registry calls replaced by fakes, recording which notifications were asked for
"""
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

import discovery.utils.update as upd
from discovery.notify import SchemaNotifier, Message
from discovery.registry.common import NoEntityError, RegistryError


# -----------------------------------------------------------------------------
# Message content
# -----------------------------------------------------------------------------

@pytest.fixture
def notifier():
    notifier = SchemaNotifier(SimpleNamespace())
    notifier.broadcast = AsyncMock(return_value=None)
    return notifier


def sent_body(notifier):
    notifier.broadcast.assert_called_once()
    return notifier.broadcast.call_args[0][0]["body"]


@pytest.mark.asyncio
async def test_update_failed_message(notifier):
    await notifier.update_failed("n3c", "could not fetch")

    notifier.broadcast.assert_called_once_with(
        Message(
            {
                "title": "❌ Schema Update Failed",
                "body": "Failed to update schema `n3c`.\nError: ```could not fetch```",
            }
        )
    )


@pytest.mark.asyncio
async def test_update_failed_truncates_long_error(notifier):
    await notifier.update_failed("n3c", "x" * 5000)

    # slack limits section text to 3000 characters
    assert len(sent_body(notifier)) < 3000


@pytest.mark.asyncio
async def test_schemaorg_update_message(notifier):
    await notifier.schemaorg_update("28.0", "29.0", 1234)

    notifier.broadcast.assert_called_once_with(
        Message(
            {
                "title": "✅ Schema.org Version Updated",
                "body": "Schema.org updated from version `28.0` to `29.0`. 1234 current classes.",
                "url": "https://discovery.biothings.io/view/schema",
                "url_text": "Visualize Schema",
            }
        )
    )


@pytest.mark.asyncio
async def test_summary_lists_each_failure(notifier):
    await notifier.update_failed_summary({"a": "a broke\ntraceback...", "b": "b broke"}, total=10)

    assert notifier.broadcast.call_args[0][0]["title"] == "❌ Daily Schema Update Failures"
    # only the first line of each error is shown
    assert sent_body(notifier) == "2 of 10 schema updates failed.\n• `a`: a broke\n• `b`: b broke"


@pytest.mark.asyncio
async def test_summary_includes_job_error(notifier):
    await notifier.update_failed_summary({}, total=0, job_error="ConnectionError: es down")

    assert "stopped early: ```ConnectionError: es down```" in sent_body(notifier)


@pytest.mark.asyncio
async def test_summary_of_many_failures_stays_under_slack_limit(notifier):
    failures = {f"ns{i}": f"RegistryError: could not fetch https://example.org/schema{i}.json" for i in range(200)}

    await notifier.update_failed_summary(failures, total=200)

    body = sent_body(notifier)
    assert len(body) < 3000
    assert body.startswith("200 of 200 schema updates failed.")
    assert "more, see the logs." in body.splitlines()[-1]


# -----------------------------------------------------------------------------
# When a notification is sent
# -----------------------------------------------------------------------------

@pytest.fixture
def notified(monkeypatch):
    """Record (action, details) for every _notify call instead of sending it."""
    calls = []
    monkeypatch.setattr(upd, "_notify", lambda action, **details: calls.append((action, details)))
    return calls


def fake_registry(monkeypatch, count=5, refresh_status=299, refresh_msg=""):
    """Make schemas.update succeed or fail without touching Elasticsearch."""
    monkeypatch.setattr(upd.schemas, "get_meta", lambda namespace: {"url": "https://example.org/s.json"})
    monkeypatch.setattr(upd.schemas, "update", lambda namespace, url: count)
    status = SimpleNamespace(refresh_status=refresh_status, refresh_msg=refresh_msg)
    monkeypatch.setattr(upd.Schema, "get", lambda id: SimpleNamespace(_status=status))


def test_schema_update_success_sends_nothing(monkeypatch, notified):
    fake_registry(monkeypatch, refresh_status=299)

    assert upd.schema_update("n3c") is None
    assert notified == []


def test_schema_update_unchanged_sends_nothing(monkeypatch, notified):
    fake_registry(monkeypatch, refresh_status=200)

    assert upd.schema_update("n3c") is None
    assert notified == []


def test_schema_update_recorded_registry_error_is_reported(monkeypatch, notified):
    # schemas.update returns the RegistryError class and stores the message in _status
    fake_registry(monkeypatch, count=RegistryError, refresh_status=400, refresh_msg="bad url")

    assert upd.schema_update("n3c") == "bad url"
    assert notified == [("update_failed", {"namespace": "n3c", "error": "bad url"})]


def test_schema_update_raised_error_is_reported(monkeypatch, notified):
    def missing(namespace):
        raise NoEntityError("namespace 'n3c' does not exist.")

    monkeypatch.setattr(upd.schemas, "get_meta", missing)

    assert upd.schema_update("n3c") == "namespace 'n3c' does not exist."
    assert notified == [("update_failed", {"namespace": "n3c", "error": "namespace 'n3c' does not exist."})]


def test_schema_update_without_notify_only_returns_the_error(monkeypatch, notified):
    fake_registry(monkeypatch, count=RegistryError, refresh_status=400, refresh_msg="bad url")

    assert upd.schema_update("n3c", notify=False) == "bad url"
    assert notified == []


def fake_schema_list(monkeypatch, namespaces, fail_after=None):
    """Make Schema.search().scan() yield these namespaces, optionally raising partway."""
    def scan():
        for i, namespace in enumerate(namespaces):
            if i == fail_after:
                raise ConnectionError("es down")
            yield SimpleNamespace(meta=SimpleNamespace(id=namespace))

    monkeypatch.setattr(upd.Schema, "search", lambda: SimpleNamespace(scan=scan))


def test_daily_update_sends_one_summary(monkeypatch, notified):
    fake_schema_list(monkeypatch, ["schema", "a", "b", "c"])
    updated = []

    def fake_update(namespace, notify=True):
        updated.append((namespace, notify))
        return None if namespace == "c" else f"{namespace} broke"

    monkeypatch.setattr(upd, "schema_update", fake_update)

    upd.daily_schema_update()

    # schema.org is skipped, and no per-schema alerts are sent
    assert updated == [("a", False), ("b", False), ("c", False)]
    assert notified == [
        ("update_failed_summary", {"failures": {"a": "a broke", "b": "b broke"}, "total": 3, "job_error": None})
    ]


def test_daily_update_with_no_failures_sends_nothing(monkeypatch, notified):
    fake_schema_list(monkeypatch, ["a", "b"])
    monkeypatch.setattr(upd, "schema_update", lambda namespace, notify=True: None)

    upd.daily_schema_update()

    assert notified == []


def test_daily_update_reports_when_schema_list_cannot_be_read(monkeypatch, notified):
    def search():
        raise ConnectionError("es down")

    monkeypatch.setattr(upd.Schema, "search", search)

    upd.daily_schema_update()  # must not raise

    assert notified == [("update_failed_summary", {"failures": {}, "total": 0, "job_error": "es down"})]


def test_daily_update_reports_failures_before_stopping_early(monkeypatch, notified):
    fake_schema_list(monkeypatch, ["a", "b", "c"], fail_after=2)
    monkeypatch.setattr(upd, "schema_update", lambda namespace, notify=True: f"{namespace} broke" if namespace == "a" else None)

    upd.daily_schema_update()

    assert notified == [("update_failed_summary", {"failures": {"a": "a broke"}, "total": 2, "job_error": "es down"})]


def fake_schemaorg(monkeypatch, stored, latest, exists=True):
    """
    Fake the schema.org version lookups. 'stored' is the list of values
    get_stored_schema_org_version returns, in order (before, then after the reload).
    Returns a list that records add_core calls.
    """
    stored = iter(stored)
    monkeypatch.setattr(upd.schemas, "get_stored_schema_org_version", lambda: next(stored))
    monkeypatch.setattr(upd, "get_latest_schema_org_version", lambda: latest)
    monkeypatch.setattr(upd.schemas, "exists", lambda namespace: exists)
    monkeypatch.setattr(upd, "_add_schema_class", lambda *args, **kwargs: 1234)
    reloads = []
    monkeypatch.setattr(upd.schemas, "add_core", lambda **kwargs: reloads.append(kwargs))
    return reloads


def test_schemaorg_new_version_is_announced(monkeypatch, notified):
    reloads = fake_schemaorg(monkeypatch, stored=["28.0", "29.0"], latest="29.0")

    upd.monthly_schemaorg_update()

    assert reloads == [{"update": True, "schema_org_version": "29.0"}]
    assert notified == [("schemaorg_update", {"old_version": "28.0", "new_version": "29.0", "num_classes": 1234})]


def test_schemaorg_already_current_sends_nothing(monkeypatch, notified):
    reloads = fake_schemaorg(monkeypatch, stored=["29.0"], latest="29.0")

    upd.monthly_schemaorg_update()

    assert reloads == []
    assert notified == []


def test_schemaorg_repair_at_same_version_sends_nothing(monkeypatch, notified):
    reloads = fake_schemaorg(monkeypatch, stored=["29.0", "29.0"], latest="29.0", exists=False)

    upd.monthly_schemaorg_update()

    assert len(reloads) == 1  # the classes were reloaded
    assert notified == []


def test_schemaorg_validation_failure_is_reported(monkeypatch, notified):
    reloads = fake_schemaorg(monkeypatch, stored=["28.0"], latest="29.0")

    def invalid(*args, **kwargs):
        raise RegistryError("invalid schema")

    monkeypatch.setattr(upd, "_add_schema_class", invalid)

    upd.monthly_schemaorg_update()

    assert reloads == []  # DDE schema.org was not touched
    assert len(notified) == 1
    action, details = notified[0]
    assert action == "update_failed"
    assert details["namespace"] == "schema"
    assert "failed validation" in details["error"]
    assert "invalid schema" in details["error"]


def test_schemaorg_reload_failure_is_reported(monkeypatch, notified):
    fake_schemaorg(monkeypatch, stored=["28.0"], latest="29.0")

    def broken_reload(**kwargs):
        raise RuntimeError("es timeout")

    monkeypatch.setattr(upd.schemas, "add_core", broken_reload)

    upd.monthly_schemaorg_update()

    assert len(notified) == 1
    action, details = notified[0]
    assert action == "update_failed"
    assert "partially updated" in details["error"]
    assert "es timeout" in details["error"]


def test_schemaorg_version_mismatch_is_reported(monkeypatch, notified):
    fake_schemaorg(monkeypatch, stored=["28.0", "28.0"], latest="29.0")

    upd.monthly_schemaorg_update()

    assert notified == [
        ("update_failed", {
            "namespace": "schema",
            "error": "schema.org version mismatch after update: expected 29.0, got 28.0",
        })
    ]
