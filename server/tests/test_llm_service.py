from unittest.mock import patch, MagicMock
from app.services import llm_service


def test_build_prompt():
    prompt = llm_service.build_prompt(
        "What is this?",
        "Sample context"
    )

    assert "What is this?" in prompt
    assert "Sample context" in prompt


@patch(
    "app.services.llm_service.ask_gemini"
)
def test_ask_llm_gemini_success(
    mock_gemini
):
    mock_gemini.return_value = \
        "Gemini answer"

    result = llm_service.ask_llm(
        "Hello",
        "Context"
    )

    assert result == \
        "Gemini answer"


@patch(
    "app.services.llm_service.ask_groq"
)
@patch(
    "app.services.llm_service.ask_gemini"
)
def test_ask_llm_fallback_groq(
    mock_gemini,
    mock_groq
):
    mock_gemini.side_effect = \
        Exception("fail")

    mock_groq.return_value = \
        "Groq answer"

    result = llm_service.ask_llm(
        "Hello",
        "Context"
    )

    assert result == \
        "Groq answer"


@patch(
    "app.services.llm_service.ask_gemini"
)
def test_summary_success(
    mock_gemini
):
    mock_gemini.return_value = \
        "Short summary"

    result = (
        llm_service
        .summarize_text(
            "Long text"
        )
    )

    assert result == \
        "Short summary"


@patch(
    "app.services.llm_service.ask_gemini"
)
def test_keywords_success(
    mock_gemini
):
    mock_gemini.return_value = \
        "python, ai, fastapi"

    result = (
        llm_service
        .generate_keywords(
            "demo text"
        )
    )

    assert "python" in result
    assert "ai" in result