from unittest.mock import patch


@patch("app.api.routes.chat.get_relevant_chunks")
@patch("app.api.routes.chat.ask_llm")
def test_chat_success(
    mock_ask_llm,
    mock_chunks,
    client
):
    mock_chunks.return_value = [
        {
            "text": "Project planning details",
            "timestamp": 10
        }
    ]

    mock_ask_llm.return_value = \
        "This file discusses planning."

    response = client.post(
        "/chat/",
        json={
            "file_id": "abc123",
            "question":
            "What is this about?"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert "answer" in data
    assert data["timestamp"] == 10