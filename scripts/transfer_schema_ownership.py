# Transfer ownership of a registered schema namespace.
#     from scripts.transfer_schema_ownership import transfer
#     transfer("nde", "gtsueng")
# The write is read back and verified. Do not trust a transfer that did not
# print VERIFIED.


import logging

from discovery.registry import schemas


def transfer(namespace, new_owner):
    """Transfer a namespace to new_owner. Return True only if verified."""
    previous = schemas.transfer_ownership(namespace, new_owner)

    stored = schemas.get_meta(namespace).get("username")
    if stored != new_owner:
        logging.error(
            "NOT VERIFIED: %s reads as %s, expected %s. The write did not persist.",
            namespace,
            stored,
            new_owner,
        )
        return False

    logging.info("VERIFIED: %s transferred %s -> %s", namespace, previous, new_owner)
    return True
