# 📚 AI Study Assistant

A simple Streamlit app that turns any topic into a quick study guide using
the Claude API: a plain-language explanation, key points, a real-world
example, and a 3-question quiz.

## Project Structure

```
ai-study-assistant/
├── app.py             # Streamlit app (UI + Claude API call)
├── .env                # Your API key (not committed to git)
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

1. The student types a topic (e.g. "Machine Learning") into a text box.
2. Clicking **Generate** sends the topic to the Claude API with a system
   prompt that asks for a specific JSON structure back: explanation, key
   points, an example, and quiz questions with answers.
3. The app parses that JSON and renders it as a clean study guide, with
   the quiz answers hidden behind expandable sections.

Everything lives in `app.py` — one script, no extra layers.

## Setup

**1. Clone the project and enter the folder**

```bash
cd ai-study-assistant
```

**2. Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Add your API key**

Open `.env` and replace the placeholder with your real key from
[console.gemini.com](https://aistudio.google.com/api-keys):

```
GEMINI_API_KEY=sk-ant-your-real-key-here
```

The `.env` file is already listed in `.gitignore`, so the key won't be
committed to version control. The app never hardcodes the key — it's
loaded at runtime with `python-dotenv`.

## Run the App

```bash
streamlit run app.py
```

Streamlit will open the app in your browser (usually at
`http://localhost:8501`).

## Using a Different LLM Provider

The app only touches the API in one place: the `generate_study_material()`
function in `app.py`. To swap in a different provider (e.g. OpenAI), you'd
replace the `Gemini` client call inside that function with the
equivalent call for your provider, keeping the same JSON-in/JSON-out
contract with the prompt.

## Error Handling

The app handles the common failure cases so it doesn't just crash:

- **Empty topic** → shows a warning instead of calling the API.
- **Missing API key** → shows a clear message telling you to set it in `.env`.
- **Invalid API key** → caught and reported as an authentication error.
- **Rate limit / connection issues** → caught and reported with a friendly message.
- **Malformed AI response** → caught so the app shows an error instead of crashing on bad JSON.

## Notes

- Default model is `gemini-3.5-flash`; override it by uncommenting
  `GEMINI_MODEL` in `.env` if you want to try a different model.
- This project is intentionally minimal — one Streamlit script, no
  database, no backend framework — so it's easy to read, explain, and
  demo end-to-end.

## Images
