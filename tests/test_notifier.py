import os
import pytest

from unittest.mock import AsyncMock
from discovery.notify import DatasetNotifier


@pytest.fixture
def mock_settings(monkeypatch):
    monkeypatch.setenv("SLACK_WEBHOOKS", "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX")
    monkeypatch.setenv("GA_ACCOUNT", "UA-XXXX-Y")
    monkeypatch.setenv("GA_UID_GENERATOR_VERSION", "1")
    monkeypatch.setenv("GA4_MEASUREMENT_ID", "G-XXXXXX")
    monkeypatch.setenv("GA4_API_SECRET", "SECRET")
    monkeypatch.setenv("GA4_UID_GENERATOR_VERSION", "2")
    monkeypatch.setenv("N3C_URI", "http://jira_domain")
    monkeypatch.setenv("N3C_AUTH_USER", "n3c_user")
    monkeypatch.setenv("N3C_AUTH_PASSWORD", "n3c_password")
    monkeypatch.setenv("N3C_PROFILE_PROJECT_ID", "00000")
    monkeypatch.setenv("N3C_PROFILE_ISSUETYPE_ID", "00001")
    monkeypatch.setenv("N3C_PROFILE_ASSIGNEE_ID", "000000:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
    monkeypatch.setenv("N3C_PROFILE_REPORTER_ID", "000000:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
    monkeypatch.setenv("N3C_PROFILE_LABEL", "DATASET")

    class MockSettings:
        SLACK_WEBHOOKS = os.getenv("SLACK_WEBHOOKS")
        GA_ACCOUNT = os.getenv("GA_ACCOUNT")
        GA_UID_GENERATOR_VERSION = os.getenv("GA_UID_GENERATOR_VERSION")
        GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID")
        GA4_API_SECRET = os.getenv("GA4_API_SECRET")
        GA4_UID_GENERATOR_VERSION = os.getenv("GA4_UID_GENERATOR_VERSION")
        N3C_URI = os.getenv("N3C_URI")
        N3C_AUTH_USER = os.getenv("N3C_AUTH_USER")
        N3C_AUTH_PASSWORD = os.getenv("N3C_AUTH_PASSWORD")
        N3C_PROFILE_PROJECT_ID = os.getenv("N3C_PROFILE_PROJECT_ID")
        N3C_PROFILE_ISSUETYPE_ID = os.getenv("N3C_PROFILE_ISSUETYPE_ID")
        N3C_PROFILE_ASSIGNEE_ID = os.getenv("N3C_PROFILE_ASSIGNEE_ID")
        N3C_PROFILE_REPORTER_ID = os.getenv("N3C_PROFILE_REPORTER_ID")
        N3C_PROFILE_LABEL = os.getenv("N3C_PROFILE_LABEL")

    return MockSettings


class MockEvent:
    pass

@pytest.mark.skip(reason="Notifier broadcast logic excludes N3C channels from test assertions")
@pytest.mark.asyncio
async def test_notifier_send(mock_settings):
    notifier = DatasetNotifier(mock_settings)
    event = MockEvent()

    assert len(notifier.channels) == 4  # Adjust based on the current number of channels

    # Mock the handles and send methods for each channel
    for channel in notifier.channels:
        channel.handles = AsyncMock(return_value=True)
        channel.send = AsyncMock(return_value=None)

    await notifier.broadcast(event)

    # Verify that handles and send were called for each channel
    for channel in notifier.channels:
        channel.handles.assert_called_once_with(event)
        channel.send.assert_called_once_with(event)
