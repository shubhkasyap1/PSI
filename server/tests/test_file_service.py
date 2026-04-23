from unittest.mock import patch, mock_open
from app.services import file_service


def test_get_file_path_found():
    with patch(
        "os.listdir",
        return_value=["abc.pdf"]
    ):
        path = file_service.get_file_path("abc")

        assert "abc.pdf" in path


def test_get_file_path_none():
    with patch(
        "os.listdir",
        return_value=[]
    ):
        assert (
            file_service.get_file_path(
                "xyz"
            ) is None
        )


def test_read_text_file():
    m = mock_open(
        read_data="hello world"
    )

    with patch(
        "builtins.open", m
    ):
        text = file_service.read_text_file(
            "demo.txt"
        )

        assert text == "hello world"


def test_split_text():
    chunks = file_service.split_text(
        "abcdefghij",
        chunk_size=3
    )

    assert chunks == [
        "abc",
        "def",
        "ghi",
        "j"
    ]


def test_split_segments():
    data = [
        {
            "text": "hello",
            "start": 0
        },
        {
            "text": "world",
            "start": 5
        }
    ]

    result = (
        file_service
        .split_segments_with_timestamps(
            data,
            chunk_size=2
        )
    )

    assert result[0][
        "timestamp"
    ] == 0