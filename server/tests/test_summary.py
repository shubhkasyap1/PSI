from unittest.mock import patch


@patch("app.api.routes.summary.extract_text")
@patch("app.api.routes.summary.summarize_text")
def test_summary_success(
    mock_summary,
    mock_extract,
    client
):
    mock_extract.return_value = \
        "This is sample content."

    mock_summary.return_value = \
        "Short summary."

    response = client.post(
        "/summary/",
        json={
            "file_id": "abc123"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["summary"] == \
        "Short summary."