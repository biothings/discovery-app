import os
import pytest

from unittest.mock import AsyncMock
from discovery.notify import SchemaNotifier, Message


@pytest.fixture
def mock_settings(monkeypatch):
    monkeypatch.setenv("SLACK_WEBHOOKS", "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX")
    monkeypatch.setenv("GA_ACCOUNT", "UA-XXXX-Y")
    monkeypatch.setenv("GA_UID_GENERATOR_VERSION", "1")
    monkeypatch.setenv("GA4_MEASUREMENT_ID", "G-XXXXXX")
    monkeypatch.setenv("GA4_API_SECRET", "SECRET")
    monkeypatch.setenv("GA4_UID_GENERATOR_VERSION", "2")
    monkeypatch.setenv("N3C_AUTH_USER", "n3c_user")
    monkeypatch.setenv("N3C_AUTH_PASSWORD", "n3c_password")

    class MockSettings:
        SLACK_WEBHOOKS = os.getenv("SLACK_WEBHOOKS")
        GA_ACCOUNT = os.getenv("GA_ACCOUNT")
        GA_UID_GENERATOR_VERSION = os.getenv("GA_UID_GENERATOR_VERSION")
        GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID")
        GA4_API_SECRET = os.getenv("GA4_API_SECRET")
        GA4_UID_GENERATOR_VERSION = os.getenv("GA4_UID_GENERATOR_VERSION")
        N3C_AUTH_USER = os.getenv("N3C_AUTH_USER")
        N3C_AUTH_PASSWORD = os.getenv("N3C_AUTH_PASSWORD")

    return MockSettings

@pytest.mark.asyncio
async def test_schema_notifier_add(mock_settings):
    notifier = SchemaNotifier(mock_settings)

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
async def test_schema_notifier_delete(mock_settings):
    notifier = SchemaNotifier(mock_settings)

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
async def test_schema_notifier_update(mock_settings):
    notifier = SchemaNotifier(mock_settings)

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
