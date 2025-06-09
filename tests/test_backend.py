import pytest
import pytest-asyncio
from fastapi.testclient import TestClient
from deploy_chatbot_python.backend.server import api, Query
from deploy_chatbot_python.config import constants


@pytest.mark.asyncio
async def test_get_root():
    with TestClient(api) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"response": "This is a chatbot"}


@pytest.mark.asyncio
async def test_post_query():
    with TestClient(api) as client:
        response = client.post(
            f"/{constants.API_POST_ENDPOINT}",
            json=Query(text='What is Cabbage?').model_dump(),
        )
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert isinstance(data["response"], str)
        assert 'dog' in data["response"].lower()
