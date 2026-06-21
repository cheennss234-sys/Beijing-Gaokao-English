#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate TXT vocabulary list from vocab_data.json.
"""

import json


def generate_txt():
    with open('/workspace/output/vocab_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    lines = []
    meta = data['metadata']
    lines.append(f"{meta['title']}")
    lines.append(f"{meta['description']}")
    lines.append(f"收录词汇数: {meta['total_words']}  |  试卷数量: {meta['total_papers']}  |  词频阈值: {meta['frequency_threshold']}")
    lines.append(f"生成日期: {meta['generated_at']}")
    lines.append('=' * 60)
    lines.append('')

    for entry in data['words']:
        rank = entry['rank']
        word = entry['word']
        pos = entry['pos']
        meaning = entry['meaning']
        freq = entry['frequency']
        lines.append(f"{rank:>4}. {word} ({pos}) {meaning} [频次:{freq}]")

    lines.append('')
    lines.append('=' * 60)
    lines.append(f'共计 {meta["total_words"]} 个课外高频词汇')

    with open('/workspace/output/beijing_grade12_english_vocab.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"TXT generated: {len(data['words'])} words")


if __name__ == '__main__':
    generate_txt()
