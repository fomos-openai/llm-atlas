#!/usr/bin/env python3
"""Validate the generated LLM Atlas book without changing it."""

from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "LLM-ATLAS.pdf"
EXPECTED_PAGE_COUNT = 13
REQUIRED_PHRASES = (
    "从预测模型",
    "阅读说明",
    "当下处于什么阶段",
    "未来要去往何处",
    "继续探索",
)


def main() -> None:
    reader = PdfReader(PDF_PATH)
    if len(reader.pages) != EXPECTED_PAGE_COUNT:
        raise SystemExit(
            f"unexpected page count: {len(reader.pages)} != {EXPECTED_PAGE_COUNT}"
        )

    links = []
    for page_number, page in enumerate(reader.pages, start=1):
        annotations = page.get("/Annots", [])
        for annotation_ref in annotations:
            annotation = annotation_ref.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            action = annotation.get("/A", {})
            uri = action.get("/URI")
            if uri:
                links.append((page_number, str(uri)))

    if len(links) < 20:
        raise SystemExit(f"too few PDF links: {len(links)}")
    if not all(uri.startswith("https://github.com/fomos-openai/llm-atlas") for _, uri in links):
        raise SystemExit("found a PDF link outside the project repository")

    with pdfplumber.open(PDF_PATH) as pdf:
        page_texts = [(page.extract_text() or "").strip() for page in pdf.pages]

    if any(not text for text in page_texts):
        empty_pages = [str(index + 1) for index, text in enumerate(page_texts) if not text]
        raise SystemExit(f"pages without extractable text: {', '.join(empty_pages)}")

    full_text = "\n".join(page_texts)
    missing = [phrase for phrase in REQUIRED_PHRASES if phrase not in full_text]
    if missing:
        raise SystemExit(f"missing required text: {', '.join(missing)}")

    print(
        f"pdf ok: {len(reader.pages)} pages, {len(full_text)} extracted characters, "
        f"{len(links)} repository links"
    )


if __name__ == "__main__":
    main()
