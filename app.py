"""
AI Study Assistant
------------------
A simple Streamlit app that uses the Gemini API to turn any
topic into a short study guide.
"""

import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

SYSTEM_PROMPT = """
You are an AI Study Assistant that helps students quickly understand
any topic they are studying.

Given a single topic, return ONLY a valid JSON object using exactly
this structure:

{
  "explanation": "A simple explanation of the topic in 3-5 sentences.",
  "key_points": [
    "point 1",
    "point 2",
    "point 3"
  ],
  "example": "One real-world example of the topic.",
  "quiz_questions": [
    {
      "question": "short question 1",
      "answer": "short correct answer 1"
    },
    {
      "question": "short question 2",
      "answer": "short correct answer 2"
    },
    {
      "question": "short question 3",
      "answer": "short correct answer 3"
    }
  ]
}

Rules:
- Keep the explanation beginner-friendly.
- Provide 3 to 5 key points.
- Provide exactly 3 quiz questions.
- Keep quiz answers short and correct.
- Include one practical real-world example.
- If the topic is vague, interpret it reasonably.
- Do not include markdown code fences.
- Do not include any text outside the JSON object.
"""


def get_client():
    """Create a Gemini client using the API key."""
    return genai.Client(api_key=API_KEY)


def clean_json_text(text):
    """Remove markdown code fences if the model adds them."""
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines)

    return text.strip()


def generate_study_material(topic):
    """Call Gemini and return structured study material."""
    client = get_client()

    prompt = f"""
{SYSTEM_PROMPT}

Student's topic:

{topic}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    raw_text = response.text
    cleaned = clean_json_text(raw_text)

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError as exc:
        raise ValueError(
            "The AI response could not be read correctly. "
            "Please try again."
        ) from exc


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Study Assistant")

st.caption(
    "Enter any topic and get an explanation, key points, "
    "a real-world example, and a quick quiz."
)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        "This AI Study Assistant uses the Gemini API to turn "
        "any topic into a short and structured study guide."
    )

    st.markdown("### How to use")

    st.markdown(
        "1. Enter a topic\n"
        "2. Click **Generate**\n"
        "3. Read your study guide"
    )

    st.divider()

    st.caption(f"Model: `{MODEL_NAME}`")


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "study_material" not in st.session_state:
    st.session_state.study_material = None

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""


# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------

topic = st.text_input(
    "Topic",
    placeholder="e.g. Machine Learning, Python Functions, Photosynthesis"
)

generate_clicked = st.button(
    "Generate",
    type="primary"
)


# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------

if generate_clicked:

    if not topic.strip():

        st.warning("Please enter a topic before generating.")

    elif not API_KEY:

        st.error(
            "No Gemini API key found. "
            "Add GEMINI_API_KEY to your .env file."
        )

    else:

        try:

            with st.spinner(
                f"Generating study material for '{topic.strip()}'..."
            ):

                st.session_state.study_material = (
                    generate_study_material(topic.strip())
                )

                st.session_state.last_topic = topic.strip()

        except Exception as exc:

            st.error(
                f"Something went wrong while contacting Gemini: {exc}"
            )


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

material = st.session_state.study_material


if material:

    st.divider()

    st.subheader(
        f"Study Guide: {st.session_state.last_topic}"
    )

    # Explanation

    st.markdown("### 📖 Explanation")

    st.write(
        material.get("explanation", "No explanation available.")
    )

    # Key Points

    st.markdown("### 🔑 Key Points")

    for point in material.get("key_points", []):

        st.markdown(f"- {point}")

    # Real World Example

    st.markdown("### 🌍 Real-World Example")

    st.info(
        material.get("example", "No example available.")
    )

    # Quiz

    st.markdown("### 📝 Quick Quiz")

    st.caption(
        "Click a question to reveal its answer."
    )

    for i, qa in enumerate(
        material.get("quiz_questions", []),
        start=1
    ):

        with st.expander(
            f"Q{i}. {qa.get('question', '')}"
        ):

            st.write(
                f"**Answer:** {qa.get('answer', '—')}"
            )

