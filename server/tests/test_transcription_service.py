from unittest.mock import patch
from app.services import transcription_service


@patch(
    "app.services.transcription_service.model.transcribe"
)
def test_transcribe_audio_success(
    mock_transcribe
):
    mock_transcribe.return_value = {
        "segments": [
            {
                "text": "hello world",
                "start": 0,
                "end": 2
            },
            {
                "text": "project planning",
                "start": 3,
                "end": 7
            }
        ]
    }

    result = (
        transcription_service
        .transcribe_audio(
            "demo.mp3"
        )
    )

    assert isinstance(
        result,
        list
    )

    assert result[0][
        "text"
    ] == "hello world"

    assert result[1][
        "start"
    ] == 3


@patch(
    "app.services.transcription_service.model.transcribe"
)
def test_transcribe_audio_error(
    mock_transcribe
):
    mock_transcribe.side_effect = \
        Exception("failed")

    result = (
        transcription_service
        .transcribe_audio(
            "bad.mp3"
        )
    )

    assert "error" in result