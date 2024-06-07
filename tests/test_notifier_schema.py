import pytest

from unittest.mock import AsyncMock
from discovery.notify import SchemaNotifier, Message


class MockSettings:
    SLACK_WEBHOOKS = ["https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"]
    GA_ACCOUNT = "UA-XXXX-Y"
    GA_UID_GENERATOR_VERSION = 1
    GA4_MEASUREMENT_ID = "G-XXXXXX"
    GA4_API_SECRET = "SECRET"
    GA4_UID_GENERATOR_VERSION = 2
    N3C_AUTH_USER = "n3c_user"
    N3C_AUTH_PASSWORD = "n3c_password"


@pytest.mark.asyncio
async def test_schema_notifier_add():
    settings = MockSettings()
    notifier = SchemaNotifier(settings)

    event_message = Message(
        {
            "title": "New Schema Registration",
            "body": '10 classes have been registered under namespace "test_namespace".',
            "url": "https://discovery.biothings.io/view/test_namespace",
            "url_text": "Visualize Schema",
        }
    )

    # Mock the broadcast method
    notifier.broadcast = AsyncMock(return_value=None)

    await notifier.add("test_namespace", 10)

    # Verify that broadcast was called with the correct message
    notifier.broadcast.assert_called_once_with(event_message)

@pytest.mark.asyncio
async def test_schema_notifier_delete():
    settings = MockSettings()
    notifier = SchemaNotifier(settings)

    event_message = Message(
        {
            "title": "Schema Deleted",
            "body": '10 classes have been deleted under namespace "test_namespace".',
        }
    )

    # Mock the broadcast method
    notifier.broadcast = AsyncMock(return_value=None)

    await notifier.delete("test_namespace", 10)

    # Verify that broadcast was called with the correct message
    notifier.broadcast.assert_called_once_with(event_message)

@pytest.mark.asyncio
async def test_schema_notifier_update():
    settings = MockSettings()
    notifier = SchemaNotifier(settings)

    event_message = Message(
        {
            "title": "Schema Updated",
            "body": 'Schema "test_namespace" updated. 10 current classes.',
            "url": "https://discovery.biothings.io/view/test_namespace",
            "url_text": "Visualize Schema",
        }
    )

    # Mock the broadcast method
    notifier.broadcast = AsyncMock(return_value=None)

    await notifier.update("test_namespace", 10)

    # Verify that broadcast was called with the correct message
    notifier.broadcast.assert_called_once_with(event_message)
