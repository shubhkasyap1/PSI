from unittest.mock import patch, MagicMock
from app.services import file_service


@patch("app.services.file_service.get_file_path")
@patch("app.services.file_service.extract_text_from_pdf")
def test_extract_text_pdf(
    mock_pdf,
    mock_path
):
    mock_path.return_value = \
        "uploads/demo.pdf"

    mock_pdf.return_value = \
        "pdf content"

    result = (
        file_service.extract_text(
            "abc"
        )
    )

    assert result == \
        "pdf content"


@patch("app.services.file_service.get_file_path")
@patch("app.services.file_service.read_text_file")
def test_extract_text_txt(
    mock_read,
    mock_path
):
    mock_path.return_value = \
        "uploads/demo.txt"

    mock_read.return_value = \
        "text file"

    result = (
        file_service.extract_text(
            "abc"
        )
    )

    assert result == \
        "text file"


@patch("app.services.file_service.get_file_path")
@patch("app.services.file_service.transcribe_audio")
def test_extract_text_audio(
    mock_transcribe,
    mock_path
):
    mock_path.return_value = \
        "uploads/demo.mp3"

    mock_transcribe.return_value = [
        {
            "text": "hello",
            "start": 0,
            "end": 1
        }
    ]

    result = (
        file_service.extract_text(
            "abc"
        )
    )

    assert isinstance(
        result,
        list
    )


@patch("app.services.file_service.get_file_path")
def test_extract_text_unsupported(
    mock_path
):
    mock_path.return_value = \
        "uploads/demo.zip"

    result = (
        file_service.extract_text(
            "abc"
        )
    )

    assert result == \
        "Unsupported file type"


@patch("app.services.file_service.get_file_path")
def test_extract_text_not_found(
    mock_path
):
    mock_path.return_value = None

    result = (
        file_service.extract_text(
            "abc"
        )
    )

    assert result == \
        "File not found"