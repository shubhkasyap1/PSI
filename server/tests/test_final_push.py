from unittest.mock import patch
from app.services import file_service


@patch("app.api.routes.chat.get_relevant_chunks")
def test_chat_exception(
    mock_chunks,
    client
):
    mock_chunks.side_effect = Exception("fail")

    r = client.post("/chat/", json={
        "file_id": "1",
        "question": "hi"
    })

    assert r.status_code == 500


@patch("app.api.routes.summary.extract_text")
def test_summary_error_case(
    mock_extract,
    client
):
    mock_extract.return_value = \
        "Error reading file"

    r = client.post("/summary/", json={
        "file_id": "1"
    })

    assert r.status_code == 200


@patch("app.services.file_service.fitz.open")
def test_pdf_exception(
    mock_open
):
    mock_open.side_effect = Exception("bad")

    result = (
        file_service
        .extract_text_from_pdf(
            "demo.pdf"
        )
    )

    assert "Error" in result


@patch("builtins.open")
def test_read_text_fail(
    mock_open
):
    mock_open.side_effect = Exception("bad")

    result = (
        file_service
        .read_text_file(
            "demo.txt"
        )
    )

    assert "Error" in result