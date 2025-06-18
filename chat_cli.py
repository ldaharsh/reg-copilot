#!/usr/bin/env python
import argparse, json, sys, ast
from utils.openai_client import chat, SYS_MSG
from utils.file_loader import read_file, chunk_text
from utils.template_loader import render

def build_prompt(file_path: str, template: str):
    raw = read_file(file_path)
    if not raw.strip():
        print("\n❌ ERROR: File could not be read or is empty.\n")
        sys.exit(1)  # Abort if file ingestion fails

    first_chunk = next(chunk_text(raw))
    return render(template, content=first_chunk, compliance_note=None)

def stream_printer(stream):
    """Safely iterate over a streaming response, ignoring empty chunks."""
    full = ""
    for chunk in stream:
        if not chunk.choices:
            continue  # ✅ Skip malformed or empty chunks
        delta = chunk.choices[0].delta
        if delta and hasattr(delta, "content"):
            full += delta.content
            print(delta.content, end="", flush=True)
    print()  # Final newline
    return full

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", "-f", required=True, help="PDF, DOCX, or TXT to summarize")
    p.add_argument("--template", "-t", default="cvb_summary")
    args = p.parse_args()

    user_content = build_prompt(args.file, args.template)
    msgs = [{"role": "system", "content": SYS_MSG},
            {"role": "user", "content": user_content}]

    print("\n📝 Full prompt sent to GPT-4o:\n", user_content, "\n")

    resp = chat(msgs, temperature=0.3)

    data = resp.choices[0].message.content

    # ✅ Strip unnecessary markdown formatting if present
    cleaned_data = data.strip("```json").strip("```")

    print("\n🔷 Raw model output:\n", cleaned_data, "\n")

    try:
        parsed = json.loads(cleaned_data)
        print("\n✅ Parsed JSON keys:", list(parsed.keys()))
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(cleaned_data)  # ✅ Handles slightly malformed JSON
            print("\n✅ Converted response to JSON:", parsed)
        except:
            print("\n⚠️ Still non-JSON. Refine prompt further.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
