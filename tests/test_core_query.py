# tests/test_core_query.py

from deploy_chatbot_python.core.index_manager import IndexManager


def test_core_indexmanager_query_keywords():
    index_manager = IndexManager()

    response_1 = index_manager.query("What types of dogs do you know?")
    response_2 = index_manager.query("What is a cabbage? Elaborate.")

    assert "cabbage" in response_1.lower(), f"Expected 'cabbage' in response, got: {response_1}"
    assert "dog" in response_2.lower(), f"Expected 'dog' in response, got: {response_2}"
