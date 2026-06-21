#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate PDF vocabulary statistics document with Anthropic brand styling.

Applies Anthropic brand colors and typography (with fallbacks) to produce
a paginated PDF vocabulary table from vocab_data.json.
"""

import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, LongTable, Spacer,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ---------------------------------------------------------------------------
# Font registration: STSong-Light provides CJK glyph coverage.
# Register it as a font family so <b> tags apply synthetic bolding.
# ---------------------------------------------------------------------------
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
registerFontFamily(
    'STSong-Light',
    normal='STSong-Light',
    bold='STSong-Light',
    italic='STSong-Light',
    boldItalic='STSong-Light',
)

# ---------------------------------------------------------------------------
# Anthropic brand palette
# ---------------------------------------------------------------------------
COLOR_DARK = HexColor('#141413')        # primary text
COLOR_LIGHT = HexColor('#faf9f5')       # light background / text on dark
COLOR_MID_GRAY = HexColor('#b0aea5')    # secondary elements
COLOR_LIGHT_GRAY = HexColor('#e8e6dc')  # subtle backgrounds
COLOR_ORANGE = HexColor('#d97757')      # primary accent
COLOR_BLUE = HexColor('#6a9bcc')        # secondary accent
COLOR_GREEN = HexColor('#788c5d')       # tertiary accent

# ---------------------------------------------------------------------------
# Font names (Poppins/Lora unavailable in this environment -> fallbacks)
# STSong-Light is required for any cell that may contain Chinese characters.
# ---------------------------------------------------------------------------
FONT_CN = 'STSong-Light'        # CJK-capable; used for all Chinese text
FONT_HEADING = 'Helvetica-Bold'  # Poppins fallback (Latin only)
FONT_BODY = 'Helvetica'          # Lora fallback (Latin only)

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------
INPUT_JSON = '/workspace/output/vocab_data.json'
OUTPUT_PDF = '/workspace/output/beijing_grade12_english_vocab.pdf'
GENERATION_DATE = '2026-06-21'


def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_title(data):
    """Document title: 24pt, Dark, centered."""
    style = ParagraphStyle(
        name='DocTitle',
        fontName=FONT_CN,
        fontSize=24,
        leading=30,
        textColor=COLOR_DARK,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    return Paragraph(data['metadata']['description'], style)


def build_description(data):
    """Description block on a Light Gray background panel."""
    meta = data['metadata']
    regions = '、'.join(meta['regions'])
    exam_types = '、'.join(meta['exam_types'])

    coverage = meta['coverage_notes']
    if len(coverage) > 200:
        coverage = coverage[:200] + '……'

    lines = [
        f'<b>年份范围：</b>{meta["years"]}',
        f'<b>覆盖城区：</b>{regions}',
        f'<b>考试类型：</b>{exam_types}',
        f'<b>课本基准：</b>{meta["textbook_baseline"]}',
        f'<b>最低词频：</b>{meta["min_frequency"]}',
        f'<b>词条总数：</b>{meta["total_words"]}',
        f'<b>数据覆盖说明：</b>{coverage}',
    ]

    style = ParagraphStyle(
        name='Desc',
        fontName=FONT_CN,
        fontSize=11,
        leading=18,
        textColor=COLOR_DARK,
        alignment=TA_LEFT,
    )

    paragraphs = [Paragraph(line, style) for line in lines]
    inner = [[p] for p in paragraphs]
    panel = Table(inner, colWidths=[495])
    panel.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT_GRAY),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBEFORE', (0, 0), (0, -1), 3, COLOR_ORANGE),
    ]))
    return panel


def build_table(data):
    """Vocabulary long table with branded header and zebra striping."""
    headers = ['排名', '单词', '词性', '中文释义', '频次']

    header_style = ParagraphStyle(
        name='Th',
        fontName=FONT_CN,
        fontSize=11,
        leading=14,
        textColor=COLOR_LIGHT,
        alignment=TA_CENTER,
    )

    rank_style = ParagraphStyle(
        name='Rank', fontName=FONT_CN, fontSize=10, leading=13,
        textColor=COLOR_DARK, alignment=TA_CENTER,
    )
    word_style = ParagraphStyle(
        name='Word', fontName=FONT_HEADING, fontSize=10, leading=13,
        textColor=COLOR_DARK, alignment=TA_LEFT,
    )
    pos_style = ParagraphStyle(
        name='Pos', fontName=FONT_CN, fontSize=10, leading=13,
        textColor=COLOR_DARK, alignment=TA_CENTER,
    )
    meaning_style = ParagraphStyle(
        name='Meaning', fontName=FONT_CN, fontSize=10, leading=13,
        textColor=COLOR_DARK, alignment=TA_LEFT,
    )
    freq_style = ParagraphStyle(
        name='Freq', fontName=FONT_HEADING, fontSize=10, leading=13,
        textColor=COLOR_ORANGE, alignment=TA_CENTER,
    )

    table_data = [[Paragraph(h, header_style) for h in headers]]

    for item in data['vocab_list']:
        table_data.append([
            Paragraph(str(item['rank']), rank_style),
            Paragraph(item['word'], word_style),
            Paragraph(item['pos'], pos_style),
            Paragraph(item['meaning'], meaning_style),
            Paragraph(str(item['frequency']), freq_style),
        ])

    col_widths = [40, 100, 45, 260, 50]  # sum = 495

    table = LongTable(table_data, colWidths=col_widths, repeatRows=1)

    style_cmds = [
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ORANGE),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_LIGHT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 9),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, COLOR_DARK),
        # Body cells
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('LINEBELOW', (0, 1), (-1, -1), 0.25, COLOR_MID_GRAY),
    ]

    # Zebra striping
    for i in range(1, len(table_data)):
        bg = COLOR_LIGHT if i % 2 == 1 else COLOR_LIGHT_GRAY
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

    table.setStyle(TableStyle(style_cmds))
    return table


def make_footer_callback(total_words):
    """Return a page callback that draws the branded footer."""
    def _draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT_CN, 9)
        canvas.setFillColor(COLOR_MID_GRAY)
        footer_text = f'共 {total_words} 个词条 | 生成日期：{GENERATION_DATE}'
        canvas.drawCentredString(A4[0] / 2.0, 28, footer_text)
        canvas.restoreState()
    return _draw_footer


def main():
    data = load_data(INPUT_JSON)
    total_words = data['metadata']['total_words']

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50,
        title=data['metadata']['description'],
        author='Anthropic Brand Guidelines',
    )

    story = [
        build_title(data),
        Spacer(1, 14),
        build_description(data),
        Spacer(1, 18),
        build_table(data),
    ]

    footer_cb = make_footer_callback(total_words)
    doc.build(story, onFirstPage=footer_cb, onLaterPages=footer_cb)

    file_size = os.path.getsize(OUTPUT_PDF)
    page_count = doc.page  # total pages after build

    print(f'生成路径: {OUTPUT_PDF}')
    print(f'词条总数: {total_words}')
    print(f'文件大小: {file_size} bytes ({file_size / 1024:.2f} KB)')
    print(f'页数: {page_count}')


if __name__ == '__main__':
    main()
