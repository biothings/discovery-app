import pytest
import asyncio
from unittest.mock import AsyncMock

from discovery.notify import DatasetNotifier

class MockSettings:
    SLACK_WEBHOOKS = ["https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"]
    GA_ACCOUNT = "UA-XXXX-Y"
    GA_UID_GENERATOR_VERSION = 1
    GA4_MEASUREMENT_ID = "G-XXXXXX"
    GA4_API_SECRET = "SECRET"
    GA4_UID_GENERATOR_VERSION = 2
    N3C_URI = 'http://jira_domain'
    N3C_AUTH_USER = "n3c_user"
    N3C_AUTH_PASSWORD = "n3c_password"
    N3C_PROFILE_PROJECT_ID = "00000"
    N3C_PROFILE_ISSUETYPE_ID = "00001"
    N3C_PROFILE_ASSIGNEE_ID = "000000:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee" 
    N3C_PROFILE_REPORTER_ID = "000000:aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    N3C_PROFILE_LABEL = "DATASET"

class MockEvent:
    pass

@pytest.mark.asyncio
async def test_notifier_send():
    settings = MockSettings()
    notifier = DatasetNotifier(settings)
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
