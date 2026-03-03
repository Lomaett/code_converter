import os
from dotenv import load_dotenv
import gradio as gr

from converter import detect_language, convert_code

load_dotenv(override=True)  # Load .env file if present, but don't override existing env vars

TARGET_LANGUAGES = [
    "Python",
    "JavaScript",
    "TypeScript",
    "Java",
    "C++",
    "C#",
    "Go",
    "Rust",
    "Ruby",
    "PHP",
    "Kotlin",
    "Swift",
    "Other",
]


def handle_detect(code: str) -> str:
    if not code or not code.strip():
        return "(no code provided)"
    return detect_language(code)


def handle_convert(code: str, target: str, custom: str) -> str:
    if not code or not code.strip():
        return "(no code provided)"
    target_lang = custom.strip() if target == "Other" and custom.strip() else target
    try:
        result = convert_code(code, target_lang)
    except Exception as e:
        return f"Error: {e}"
    return result


with gr.Blocks(title="Code Converter") as demo:
    gr.Markdown("# Code Converter — detect & convert between languages using LLMs")

    with gr.Row():
        code_in = gr.Textbox(lines=20, label="Input Code", placeholder="Paste code here...")
        converted_out = gr.Textbox(lines=20, label="Converted Code")

    with gr.Row():
        lang_dropdown = gr.Dropdown(TARGET_LANGUAGES, value="Python", label="Target Language")
        custom_lang = gr.Textbox(label="Custom target language (when 'Other' selected)", placeholder="e.g. Nim, Haskell")
        detect_btn = gr.Button("Detect Language")
        convert_btn = gr.Button("Convert Code")

    detected = gr.Textbox(label="Detected Language", interactive=False)

    detect_btn.click(fn=handle_detect, inputs=code_in, outputs=detected)
    convert_btn.click(fn=handle_convert, inputs=[code_in, lang_dropdown, custom_lang], outputs=converted_out)


if __name__ == "__main__":
    demo.launch(inbrowser=True)
