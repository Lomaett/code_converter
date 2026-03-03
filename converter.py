import os
import re
from dotenv import load_dotenv

load_dotenv(override=True)  # Load .env file if present, but don't override existing env vars

import openai
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


def detect_language(code: str) -> str:
    """Try to detect programming language using Pygments (fast, local).

    Returns a short, human-friendly language name or 'Unknown'.
    """
    try:
        lexer = guess_lexer(code)
        return lexer.name
    except ClassNotFound:
        return "Unknown"


def _strip_code_fence(text: str) -> str:
    # Remove surrounding triple-backtick code fences if present
    fence_re = re.compile(r"^\s*```[\w+-]*\n(.*)```\s*$", re.S)
    m = fence_re.match(text)
    if m:
        return m.group(1).strip()
    return text.strip()


def convert_code(code: str, target_language: str) -> str:
    """Convert `code` to `target_language` using an LLM via the OpenAI API.

    Requires `OPENAI_API_KEY` in environment or loaded via .env.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set in environment")

    system = (
        "You are an expert software engineer and language translator. "
        "When asked, convert the provided code to the requested target language, "
        "preserving behavior and idiomatic style. Return only the converted code."
    )

    user = (
        f"Convert the following code to {target_language}. "
        "Preserve behavior and variable names when possible. If external libraries are used, "
        "use idiomatic standard-library equivalents or note required libraries in a brief comment. "
        "Return only the code (preferably in a single codeblock).\n\n"
        "Code:\n```\n" + code + "\n```")

    resp = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )

    content = resp.choices[0].message.content
    return _strip_code_fence(content)
