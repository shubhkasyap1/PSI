from unittest.mock import patch
from app.services import llm_service


@patch("app.services.llm_service.ask_groq")
@patch("app.services.llm_service.ask_gemini")
def test_ask_llm_both_fail(
    mock_gemini,
    mock_groq
):
    mock_gemini.side_effect = Exception("fail")
    mock_groq.side_effect = Exception("fail")

    result = llm_service.ask_llm(
        "hello",
        "context data"
    )

    assert "context" in result.lower()


@patch("app.services.llm_service.ask_groq")
@patch("app.services.llm_service.ask_gemini")
def test_summary_fallback_groq(
    mock_gemini,
    mock_groq
):
    mock_gemini.side_effect = Exception("fail")
    mock_groq.return_value = "Groq summary"

    result = llm_service.summarize_text(
        "long text"
    )

    assert result == "Groq summary"


@patch("app.services.llm_service.ask_groq")
@patch("app.services.llm_service.ask_gemini")
def test_summary_both_fail(
    mock_gemini,
    mock_groq
):
    mock_gemini.side_effect = Exception("fail")
    mock_groq.side_effect = Exception("fail")

    result = llm_service.summarize_text(
        "abcdefghi"
    )

    assert "abc" in result


@patch("app.services.llm_service.ask_groq")
@patch("app.services.llm_service.ask_gemini")
def test_keywords_fallback(
    mock_gemini,
    mock_groq
):
    mock_gemini.side_effect = Exception("fail")
    mock_groq.return_value = "one,two,three"

    result = llm_service.generate_keywords(
        "demo"
    )

    assert "one" in result


@patch("app.services.llm_service.ask_groq")
@patch("app.services.llm_service.ask_gemini")
def test_keywords_both_fail(
    mock_gemini,
    mock_groq
):
    mock_gemini.side_effect = Exception("fail")
    mock_groq.side_effect = Exception("fail")

    result = llm_service.generate_keywords(
        "demo"
    )

    assert result == []