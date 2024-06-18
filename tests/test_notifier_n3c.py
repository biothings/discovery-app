import pytest
import uuid

from aioresponses import aioresponses
from biothings.web.analytics.events import Message
from discovery.notify import N3CChannel
from types import SimpleNamespace


@pytest.mark.asyncio
async def test_N3C_send():
    event = Message()
    uri = "http://jira_domain"
    urn = "/rest/api/3/issue"
    url=f"{uri}{urn}"
    user = "user"
    password = uuid.uuid4().hex
    profile = SimpleNamespace()
    profile.project_id = "1"  # External Dataset project
    profile.issuetype_id = "10001"
    profile.assignee_id = "000000:aaaaaaaa-1111-bbbb-2222-cccccccccccc"
    profile.reporter_id = "000000:aaaaaaaa-1111-bbbb-2222-cccccccccccc"
    profile.label = "DATASET"
    channel = N3CChannel(uri=uri,
                         user=user,
                         password=password,
                         profile=profile)

    with aioresponses() as m:
        m.post(url=url, status=200, body="send_response")
        response_status, response_text = await channel.send(event)
        assert response_status == 200
        assert response_text == "send_response"

@pytest.mark.asyncio
async def test_N3C_send_query():
    user = "test_user"
    uri = "http://jira_domain"
    urn = f"/rest/api/3/user/search?query={user}"
    url = f"{uri}{urn}"
    username = " username"
    password = uuid.uuid4().hex
    profile = "profile"
    channel = N3CChannel(uri=uri, user=username, password=password, profile=profile)

    with aioresponses() as m:
        m.get(url=url, status=200, body="query_response")
        response_status, response_text = await channel.sends_query(user)
        assert response_status == 200
        assert response_text == "query_response"

@pytest.mark.asyncio
async def test_N3C_sends_signup():
    user = "test_user"
    uri = "http://jira_domain"
    urn = "/rest/servicedeskapi/customer"
    url = f"{uri}{urn}"
    channel = N3CChannel(uri=uri, user="username", password="password", profile="profile")
    with aioresponses() as m:
        m.post(url=url, status=200, body="signup_response")
        response_status, response_text = await channel.sends_signup(user)
        assert response_status == 200
        assert response_text == "signup_response"
