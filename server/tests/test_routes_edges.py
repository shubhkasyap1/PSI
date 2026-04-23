from unittest.mock import patch


@patch("app.api.routes.chat.get_relevant_chunks")
def test_chat_no_chunks(mock_chunks, client):
    mock_chunks.return_value = []

    r = client.post("/chat/", json={
        "file_id": "1",
        "question": "hello"
    })

    assert r.status_code == 200
    assert "No relevant" in r.json()["answer"]


@patch("app.api.routes.summary.extract_text")
def test_summary_no_content(mock_extract, client):
    mock_extract.return_value = ""

    r = client.post("/summary/", json={
        "file_id": "1"
    })

    assert r.status_code == 200


@patch("app.api.routes.upload.shutil.copyfileobj")
def test_upload_exception(mock_copy, client):
    mock_copy.side_effect = Exception("fail")

    files = {
        "file": ("a.txt", b"abc", "text/plain")
    }

    r = client.post("/upload/", files=files)

    assert r.status_code == 500