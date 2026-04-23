from unittest.mock import patch


@patch(
 "app.api.routes.upload.build_vector_index"
)
def test_upload_file(
    mock_index,
    client
):
    mock_index.return_value = {
        "message":
        "Vector index created"
    }

    files = {
        "file":
        ("demo.txt",
         b"hello world",
         "text/plain")
    }

    response = client.post(
        "/upload/",
        files=files
    )

    data = response.json()

    assert response.status_code == 200
    assert "file_id" in data