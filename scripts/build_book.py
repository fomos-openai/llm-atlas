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
OUTPUT = ROOT / "LLM-ATLAS.pdf"
CHAPTERS = sorted((ROOT / "book" / "chapters").glob("*.md"))
REPO = "https://github.com/fomos-openai/llm-atlas/blob/main/"

FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"
FONT_MEDIUM = "/System/Library/Fonts/STHeiti Medium.ttc"
pdfmetrics.registerFont(TTFont("AtlasSans", FONT_LIGHT, subfontIndex=0))
pdfmetrics.registerFont(TTFont("AtlasSansMedium", FONT_MEDIUM, subfontIndex=0))

PAGE_W, PAGE_H = A5


def link_target(raw: str, source: Path) -> str:
    if raw.startswith(("http://", "https://", "mailto:")):
        return raw
    target = (source.parent / raw).resolve()
    relative = target.relative_to(ROOT).as_posix()
    return REPO + relative


def inline_markup(text: str, source: Path) -> str:
    parts = []
    cursor = 0
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        parts.append(html.escape(text[cursor:match.start()]))
        label = html.escape(match.group(1))
        target = html.escape(link_target(match.group(2), source), quote=True)
        parts.append(f'<link href="{target}" color="#2563eb"><u>{label}</u></link>')
        cursor = match.end()
    parts.append(html.escape(text[cursor:]))
    return "".join(parts).replace("`", "")


styles = getSampleStyleSheet()
cover_title = ParagraphStyle(
    "CoverTitle", fontName="AtlasSansMedium", fontSize=27, leading=38,
    textColor=colors.HexColor("#0f172a"), alignment=TA_LEFT, spaceAfter=10 * mm,
)
cover_sub = ParagraphStyle(
    "CoverSub", fontName="AtlasSans", fontSize=12, leading=21,
    textColor=colors.HexColor("#475569"), alignment=TA_LEFT,
)
chapter_title = ParagraphStyle(
    "ChapterTitle", fontName="AtlasSansMedium", fontSize=20, leading=29,
    textColor=colors.HexColor("#0f172a"), spaceAfter=8 * mm,
)
section = ParagraphStyle(
    "Section", fontName="AtlasSansMedium", fontSize=13, leading=20,
    textColor=colors.HexColor("#1d4ed8"), spaceBefore=5 * mm, spaceAfter=2.5 * mm,
)
body = ParagraphStyle(
    "Body", fontName="AtlasSans", fontSize=9.6, leading=16.2,
    textColor=colors.HexColor("#1e293b"), alignment=TA_LEFT,
    spaceAfter=3.6 * mm, wordWrap="CJK",
)
bullet = ParagraphStyle(
    "Bullet", parent=body, leftIndent=5 * mm, firstLineIndent=-3.5 * mm,
    bulletIndent=0, spaceAfter=2.4 * mm,
)
toc = ParagraphStyle(
    "TOC", fontName="AtlasSans", fontSize=10.5, leading=18,
    textColor=colors.HexColor("#334155"), leftIndent=2 * mm,
)


def page_frame(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#2563eb"))
    canvas.rect(0, PAGE_H - 4 * mm, PAGE_W, 4 * mm, fill=1, stroke=0)
    canvas.setFont("AtlasSans", 7.5)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(15 * mm, 8 * mm, "LLM Atlas · 2026-09")
    canvas.drawRightString(PAGE_W - 15 * mm, 8 * mm, str(doc.page))
    canvas.restoreState()


def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#0f172a"))
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    for x, y, radius, color in [
        (PAGE_W - 25 * mm, PAGE_H - 30 * mm, 45 * mm, "#1d4ed8"),
        (PAGE_W - 8 * mm, PAGE_H - 65 * mm, 32 * mm, "#7c3aed"),
        (22 * mm, 25 * mm, 24 * mm, "#0e7490"),
    ]:
        canvas.setFillColor(colors.Color(*colors.HexColor(color).rgb(), alpha=0.34))
        canvas.circle(x, y, radius, fill=1, stroke=0)
    canvas.restoreState()


story = [
    Spacer(1, 34 * mm),
    Paragraph("LLM Atlas", ParagraphStyle("Kicker", fontName="AtlasSansMedium", fontSize=13, textColor=colors.HexColor("#67e8f9"), leading=18)),
    Spacer(1, 5 * mm),
    Paragraph("从预测模型<br/>到行动系统", ParagraphStyle("CoverWhite", parent=cover_title, textColor=colors.white)),
    Paragraph("大模型从哪里来、当下处于什么阶段、未来要去往何处", ParagraphStyle("CoverSubWhite", parent=cover_sub, textColor=colors.HexColor("#cbd5e1"))),
    Spacer(1, 54 * mm),
    Paragraph("2026-09 · 开源知识地图精炼版", ParagraphStyle("Edition", fontName="AtlasSans", fontSize=9, textColor=colors.HexColor("#a5f3fc"), leading=14)),
    PageBreak(),
    Paragraph("阅读说明", chapter_title),
    Paragraph("本书是一张导航图，不是穷尽所有论文的百科。每章末尾的蓝色链接会跳转到 GitHub 知识库中的扩展页面；知识库保留 21 个章节、159 个主题页面、结构化目录和 Archify 交互地图。", body),
    Paragraph("目录", section),
]

for chapter in CHAPTERS:
    title = chapter.read_text(encoding="utf8").splitlines()[0].removeprefix("# ")
    story.append(Paragraph(html.escape(title), toc))
story.append(PageBreak())


def flush_paragraph(story_items, paragraph_lines, source):
    if paragraph_lines:
        story_items.append(Paragraph(inline_markup(" ".join(paragraph_lines), source), body))
    return []


for index, chapter in enumerate(CHAPTERS):
    lines = chapter.read_text(encoding="utf8").splitlines()
    story.append(Paragraph(html.escape(lines[0].removeprefix("# ")), chapter_title))
    paragraph_lines = []

    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            paragraph_lines = flush_paragraph(story, paragraph_lines, chapter)
        elif stripped.startswith("## "):
            paragraph_lines = flush_paragraph(story, paragraph_lines, chapter)
            story.append(Paragraph(inline_markup(stripped[3:], chapter), section))
        elif stripped.startswith("- "):
            paragraph_lines = flush_paragraph(story, paragraph_lines, chapter)
            story.append(Paragraph(inline_markup(stripped[2:], chapter), bullet, bulletText="•"))
        else:
            paragraph_lines.append(stripped)
    paragraph_lines = flush_paragraph(story, paragraph_lines, chapter)
    if index != len(CHAPTERS) - 1:
        story.append(PageBreak())

story.extend([
    PageBreak(),
    Paragraph("继续探索", chapter_title),
    Paragraph(f'<link href="https://github.com/fomos-openai/llm-atlas" color="#2563eb"><u>github.com/fomos-openai/llm-atlas</u></link>', body),
    Paragraph("仓库包含 Archify 交互知识地图、全部主题页、模型/数据/基准/工具目录、引用政策与可复现构建脚本。内容采用日期快照和证据等级持续维护。", body),
    Spacer(1, 12 * mm),
    Paragraph("知识应该能被追溯、质疑、更新，也应该帮助我们知道何时停止自动化并寻求人类判断。", ParagraphStyle("Closing", parent=body, fontName="AtlasSansMedium", fontSize=12, leading=21, textColor=colors.HexColor("#0f172a"))),
])

doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A5, rightMargin=15 * mm, leftMargin=15 * mm,
    topMargin=16 * mm, bottomMargin=15 * mm,
    title="LLM Atlas：从预测模型到行动系统",
    author="LLM Atlas Contributors",
    subject="大模型完整技术生命周期知识地图",
)
doc.build(story, onFirstPage=first_page, onLaterPages=page_frame)
print(f"wrote {OUTPUT}")
