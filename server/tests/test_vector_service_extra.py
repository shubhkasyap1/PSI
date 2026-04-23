from unittest.mock import patch, mock_open
from app.services import vector_service


@patch("app.services.vector_service.extract_text")
@patch("app.services.vector_service.faiss.write_index")
@patch("builtins.open", new_callable=mock_open)
@patch("pickle.dump")
@patch("app.services.vector_service.get_embedding")
def test_build_vector_index_text_success(
    mock_embed,
    mock_pickle,
    mock_file,
    mock_write,
    mock_extract
):
    mock_extract.return_value = "hello world"

    mock_embed.return_value = [0.1, 0.2]

    result = vector_service.build_vector_index("abc")

    assert "message" in result


@patch("app.services.vector_service.extract_text")
@patch("app.services.vector_service.faiss.write_index")
@patch("builtins.open", new_callable=mock_open)
@patch("pickle.dump")
@patch("app.services.vector_service.get_embedding")
def test_build_vector_index_audio_success(
    mock_embed,
    mock_pickle,
    mock_file,
    mock_write,
    mock_extract
):
    mock_extract.return_value = [
        {"text": "hello", "start": 0, "end": 1},
        {"text": "world", "start": 2, "end": 3},
    ]

    mock_embed.return_value = [0.1, 0.2]

    result = vector_service.build_vector_index("abc")

    assert "message" in result


@patch("app.services.vector_service.extract_text")
def test_build_vector_index_empty(
    mock_extract
):
    mock_extract.return_value = ""

    result = vector_service.build_vector_index("abc")

    assert "error" in result


@patch("app.services.vector_service.os.path.exists")
def test_get_relevant_chunks_missing(
    mock_exists
):
    mock_exists.return_value = False

    result = vector_service.get_relevant_chunks(
        "abc",
        "hello"
    )

    assert result == []