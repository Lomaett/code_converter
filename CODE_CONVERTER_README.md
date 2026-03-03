# Code Converter (LLM-backed)

This small project provides a Gradio UI to detect a programming language from pasted code and convert it to a target language using an LLM (OpenAI).

Files added:
- `app.py` — Gradio web UI
- `converter.py` — language detection and LLM conversion helpers
- `requirements.txt` — Python dependencies
- `.env.example` — example environment variables

Quickstart
1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2. Install dependencies (use a venv):

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open the Gradio interface at `http://localhost:7860`.

Notes
- `converter.py` uses `pygments` for local language detection and `openai` for conversion. Ensure your API key is set.
- The app expects the OpenAI-compatible API. You can set `OPENAI_MODEL` in `.env` to change the model.
