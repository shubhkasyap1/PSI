import os
from dotenv import load_dotenv
from google import genai
from groq import Groq

# ---------------------------------
# Load Environment Variables
# ---------------------------------
load_dotenv()

# ---------------------------------
# Clients
# ---------------------------------
gemini_client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------------------------
# Models
# ---------------------------------
GEMINI_MODEL = "gemini-2.5-flash"
GROQ_MODEL = "llama-3.1-8b-instant"


# ---------------------------------
# Prompt Builder
# ---------------------------------
def build_prompt(question: str, context: str) -> str:
    return f"""
You are an AI assistant.

Answer the question ONLY using the provided context.
If the answer is not present, say:
"I could not find this information in the document."

---------------------
Context:
{context}
---------------------

Question:
{question}

Answer clearly and concisely:
"""


# ---------------------------------
# Gemini Response
# ---------------------------------
def ask_gemini(prompt: str) -> str:
    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return response.text.strip()


# ---------------------------------
# Groq Response
# ---------------------------------
def ask_groq(prompt: str) -> str:
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


# ---------------------------------
# Main LLM Function (Gemini -> Groq)
# ---------------------------------
def ask_llm(question: str, context: str) -> str:
    prompt = build_prompt(question, context)

    # Try Gemini first
    try:
        return ask_gemini(prompt)

    except Exception as e:
        print("Gemini failed:", e)

    # Try Groq fallback
    try:
        return ask_groq(prompt)

    except Exception as e:
        print("Groq failed:", e)

    # Final fallback
    return context[:500] + "..."


# ---------------------------------
# Summary Function
# ---------------------------------
def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following content in a clear and structured way.
Use bullet points if needed.

Content:
{text}
"""

    # Try Gemini first
    try:
        return ask_gemini(prompt)

    except Exception as e:
        print("Gemini summary failed:", e)

    # Try Groq fallback
    try:
        return ask_groq(prompt)

    except Exception as e:
        print("Groq summary failed:", e)

    # Final fallback
    return text[:300] + "..."


# ---------------------------------
# Keyword Extraction
# ---------------------------------
def generate_keywords(text: str):
    prompt = f"""
Extract 5-10 important keywords from this text.
Return them as comma-separated values.

{text}
"""

    result = ""

    # Try Gemini first
    try:
        result = ask_gemini(prompt)

    except Exception as e:
        print("Gemini keyword failed:", e)

        # Try Groq fallback
        try:
            result = ask_groq(prompt)

        except Exception as e:
            print("Groq keyword failed:", e)
            return []

    return [k.strip() for k in result.split(",")]