# utils/file_loader.py
"""
Load DOCX, PDF or plain-text into a string.
Includes a simple token-based chunker so prompts stay under the GPT-4o limit.
"""
from pathlib import Path
import docx, PyPDF2, tiktoken

# ----------------------------------------------------------------------
# File reading helpers
# ----------------------------------------------------------------------
def read_file(path: str) -> str:
    p = Path(path)
    ext = p.suffix.lower()

    if ext == ".docx":
        doc = docx.Document(p)
        return "\n".join(par.text for par in doc.paragraphs)

    if ext == ".pdf":
        text = ""
        with open(p, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for pg in reader.pages:
                text += pg.extract_text() + "\n"
        return text

    # fallback to plain text
    return p.read_text(encoding="utf-8")


# ----------------------------------------------------------------------
# Token chunking (so we don't exceed context window)
# ----------------------------------------------------------------------
enc = tiktoken.get_encoding("cl100k_base")   # same tokenizer GPT-4o uses

def chunk_text(txt: str, max_tokens: int = 3000):
    """
    Yields successive ≤max_tokens chunks of text.
    """
    tokens = enc.encode(txt)
    for i in range(0, len(tokens), max_tokens):
        yield enc.decode(tokens[i : i + max_tokens])
