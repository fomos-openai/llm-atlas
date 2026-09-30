#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output" / "pdf" / "LLM-Atlas.pdf"
CHAPTERS = sorted((ROOT / "book" / "chapters").glob("*.md"))
REPO = "https://github.com/fomos-openai/llm-atlas/blob/codex/rewrite-v2/"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"

pdfmetrics.registerFont(TTFont("AtlasSans", FONT_LIGHT, subfontIndex=0))
pdfmetrics.registerFont(TTFont("AtlasSansMedium", FONT_MEDIUM, subfontIndex=0))
PAGE_W, PAGE_H = A5


def link_target(raw: str, source: Path) -> str:
    if raw.startswith(("http://", "https://", "mailto:")):
        return raw
    target = (source.parent / raw).resolve()
    return REPO + target.relative_to(ROOT).as_posix()


def inline_markup(text: str, source: Path) -> str:
    parts, cursor = [], 0
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        parts.append(html.escape(text[cursor:match.start()]))
        label = html.escape(match.group(1))
        target = html.escape(link_target(match.group(2), source), quote=True)
        parts.append(f'<link href="{target}" color="#2563eb"><u>{label}</u></link>')
        cursor = match.end()
    parts.append(html.escape(text[cursor:]))
    return "".join(parts).replace("`", "")


styles = getSampleStyleSheet()
cover_title = ParagraphStyle("CoverTitle", fontName="AtlasSansMedium", fontSize=25, leading=36, textColor=colors.white)
cover_sub = ParagraphStyle("CoverSub", fontName="AtlasSans", fontSize=11, leading=20, textColor=colors.HexColor("#cbd5e1"))
chapter_title = ParagraphStyle("Chapter", fontName="AtlasSansMedium", fontSize=19, leading=28, textColor=colors.HexColor("#0f172a"), spaceAfter=8 * mm)
section = ParagraphStyle("Section", fontName="AtlasSansMedium", fontSize=12.5, leading=19, textColor=colors.HexColor("#1d4ed8"), spaceBefore=5 * mm, spaceAfter=2.5 * mm, keepWithNext=True)
subsection = ParagraphStyle("Subsection", fontName="AtlasSansMedium", fontSize=10.5, leading=17, textColor=colors.HexColor("#0f766e"), spaceBefore=4 * mm, spaceAfter=2 * mm, keepWithNext=True)
body = ParagraphStyle("Body", fontName="AtlasSans", fontSize=10.5, leading=19.5, textColor=colors.HexColor("#1e293b"), alignment=TA_LEFT, wordWrap="CJK", spaceAfter=4 * mm)
toc = ParagraphStyle("TOC", fontName="AtlasSans", fontSize=9.8, leading=17, textColor=colors.HexColor("#334155"), leftIndent=2 * mm)
bullet = ParagraphStyle("Bullet", parent=body, leftIndent=5 * mm, firstLineIndent=-3.5 * mm, spaceAfter=2 * mm)


def page_frame(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#2563eb"))
    canvas.rect(0, PAGE_H - 3.5 * mm, PAGE_W, 3.5 * mm, fill=1, stroke=0)
    canvas.setFont("AtlasSans", 7.2)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(14 * mm, 7.5 * mm, "LLM Atlas v2 · 2026-10")
    canvas.drawRightString(PAGE_W - 14 * mm, 7.5 * mm, str(doc.page))
    canvas.restoreState()


def first_page(canvas, _doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#07111f"))
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    for x, y, radius, color in [
        (PAGE_W - 18 * mm, PAGE_H - 35 * mm, 50 * mm, "#2563eb"),
        (PAGE_W - 3 * mm, PAGE_H - 85 * mm, 34 * mm, "#7c3aed"),
        (20 * mm, 26 * mm, 28 * mm, "#0e7490"),
    ]:
        canvas.setFillColor(colors.Color(*colors.HexColor(color).rgb(), alpha=0.34))
        canvas.circle(x, y, radius, fill=1, stroke=0)
    canvas.restoreState()


def flush(story, lines, source):
    if lines:
        story.append(Paragraph(inline_markup(" ".join(lines), source), body))
    return []


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    story = [
        Spacer(1, 32 * mm),
        Paragraph("LLM Atlas v2", ParagraphStyle("Kicker", fontName="AtlasSansMedium", fontSize=13, textColor=colors.HexColor("#67e8f9"), leading=18)),
        Spacer(1, 5 * mm),
        Paragraph("从模型<br/>到行动系统", cover_title),
        Spacer(1, 5 * mm),
        Paragraph("完整生命周期 · 学术与产业圣杯 · Top 模型路线<br/>可复现实践 · 技术专家成长路径", cover_sub),
        Spacer(1, 55 * mm),
        Paragraph("2026-10 · 开源工程知识地图", ParagraphStyle("Edition", fontName="AtlasSans", fontSize=9, textColor=colors.HexColor("#a5f3fc"))),
        PageBreak(),
        Paragraph("如何阅读", chapter_title),
        Paragraph("本书提供连续叙事，仓库提供可独立更新的深层知识。蓝色链接指向对应主题页；模型、框架和现状信息带核验日期。建议先完整阅读，再按工作问题回到知识树和实验。", body),
        Paragraph("目录", section),
    ]
    for chapter in CHAPTERS:
        title = chapter.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
        story.append(Paragraph(html.escape(title), toc))
    story.append(PageBreak())
    for chapter_index, chapter in enumerate(CHAPTERS):
        lines = chapter.read_text(encoding="utf-8").splitlines()
        story.append(Paragraph(html.escape(lines[0].removeprefix("# ")), chapter_title))
        paragraph = []
        for line in lines[1:]:
            stripped = line.strip()
            if not stripped:
                paragraph = flush(story, paragraph, chapter)
            elif stripped.startswith("## "):
                paragraph = flush(story, paragraph, chapter)
                story.append(Paragraph(inline_markup(stripped[3:], chapter), section))
            elif stripped.startswith("### "):
                paragraph = flush(story, paragraph, chapter)
                story.append(Paragraph(inline_markup(stripped[4:], chapter), subsection))
            elif stripped.startswith("- "):
                paragraph = flush(story, paragraph, chapter)
                story.append(Paragraph(inline_markup(stripped[2:], chapter), bullet, bulletText="•"))
            else:
                paragraph.append(stripped)
        flush(story, paragraph, chapter)
        if chapter_index != len(CHAPTERS) - 1:
            story.append(PageBreak())
    story.extend([
        PageBreak(), Paragraph("继续探索", chapter_title),
        Paragraph('<link href="https://github.com/fomos-openai/llm-atlas" color="#2563eb"><u>github.com/fomos-openai/llm-atlas</u></link>', body),
        Paragraph("仓库包含 205 篇知识正文、可运行小模型实验、结构化目录、证据登记与 Archify 交互地图。知识应该帮助工程师做出可解释、可验证、可回滚的决策。", body),
    ])
    document = SimpleDocTemplate(str(OUTPUT), pagesize=A5, rightMargin=15 * mm, leftMargin=15 * mm, topMargin=16 * mm, bottomMargin=15 * mm, title="LLM Atlas v2：从模型到行动系统", author="LLM Atlas Contributors", subject="大模型技术完整生命周期")
    document.build(story, onFirstPage=first_page, onLaterPages=page_frame)
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    build()
