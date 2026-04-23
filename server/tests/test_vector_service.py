from unittest.mock import patch, mock_open
from app.services import vector_service


@patch(
    "app.services.vector_service.get_embedding"
)
def test_get_embedding_mock(
    mock_embed
):
    mock_embed.return_value = [
        0.1, 0.2, 0.3
    ]

    result = (
        vector_service
        .get_embedding("hello")
    )

    assert len(result) == 3


@patch(
    "app.services.vector_service.extract_text"
)
def test_build_vector_index_error(
    mock_extract
):
    mock_extract.return_value = \
        "Error reading file"

    result = (
        vector_service
        .build_vector_index(
            "abc"
        )
    )

    assert "error" in result


@patch(
    "app.services.vector_service.os.path.exists"
)
def test_get_relevant_chunks_no_file(
    mock_exists
):
    mock_exists.return_value = False

    result = (
        vector_service
        .get_relevant_chunks(
            "abc",
            "hello"
        )
    )

    assert result == []


@patch(
    "app.services.vector_service.os.path.exists"
)
@patch(
    "app.services.vector_service.faiss.read_index"
)
@patch(
    "app.services.vector_service.get_embedding"
)
@patch(
    "builtins.open",
    new_callable=mock_open
)
@patch(
    "pickle.load"
)
def test_get_relevant_chunks_success(
    mock_pickle,
    mock_file,
    mock_embed,
    mock_read,
    mock_exists
):
    mock_exists.return_value = True

    mock_embed.return_value = [
        0.1, 0.2
    ]

    mock_pickle.return_value = [
        {
            "text": "hello",
            "timestamp": 5
        }
    ]

    fake_index = mock_read.return_value
    fake_index.search.return_value = (
        [[0.15]],
        [[0]]
)

    result = (
        vector_service
        .get_relevant_chunks(
            "abc",
            "hello"
        )
    )

    assert result[0][
        "text"
    ] == "hello"