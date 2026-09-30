#!/usr/bin/env python3
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "output" / "pdf" / "LLM-Atlas.pdf"


def main() -> None:
    reader = PdfReader(PDF)
    pages = len(reader.pages)
    if not 120 <= pages <= 160:
        raise SystemExit(f"page count outside 120-160: {pages}")
    links = []
    for page in reader.pages:
        for reference in page.get("/Annots", []):
            annotation = reference.get_object()
            uri = annotation.get("/A", {}).get("/URI") if annotation.get("/Subtype") == "/Link" else None
            if uri:
                links.append(str(uri))
    if len(links) < 100 or not all(uri.startswith("https://github.com/fomos-openai/llm-atlas") for uri in links):
        raise SystemExit(f"invalid repository link set: {len(links)}")
    with pdfplumber.open(PDF) as document:
        texts = [(page.extract_text() or "").strip() for page in document.pages]
    if any(not text for text in texts):
        raise SystemExit("one or more pages have no extractable text")
    full = "\n".join(texts)
    for phrase in ["从模型", "学术与产业圣杯", "小模型实践", "职业迁移", "未来"]:
        if phrase not in full:
            raise SystemExit(f"missing phrase: {phrase}")
    print(f"pdf ok: {pages} pages, {len(full)} extracted characters, {len(links)} repository links")


if __name__ == "__main__":
    main()
