#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 vocab_data.json 转换为 qwerty-learner 网站词典格式。

目标格式（参考 https://github.com/RealKai42/qwerty-learner/blob/master/docs/toBuildDict.md）:
[
  {
    "name": "word",
    "trans": ["pos. meaning1,meaning2,..."]
  },
  ...
]

同时生成 dictionary.ts 索引条目。
"""

import json
import os


def convert_to_qwerty_format():
    """将 vocab_data.json 转换为 qwerty-learner 词典格式。"""
    with open('/workspace/output/vocab_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    words = data['words']
    meta = data['metadata']

    # 转换为 qwerty-learner 格式
    dict_entries = []
    for entry in words:
        word = entry['word']
        pos = entry['pos']
        meaning = entry['meaning']
        freq = entry['frequency']

        # 构建 trans 字符串
        # 参考官方示例: "n. 档案,公文箱,锉刀,[计算机] 文件 vt. 列队行进,归档,申请"
        # 我们将 POS 和中文释义合并为一个字符串
        if pos and meaning:
            trans_str = f"{pos} {meaning}"
        elif pos:
            trans_str = pos
        elif meaning:
            trans_str = meaning
        else:
            trans_str = ""

        dict_entries.append({
            "name": word,
            "trans": [trans_str]
        })

    # 保存词典文件
    dict_filename = 'Beijing_Grade12_English_Vocab.json'
    dict_path = f'/workspace/output/qwerty_dict/{dict_filename}'
    os.makedirs(os.path.dirname(dict_path), exist_ok=True)

    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(dict_entries, f, ensure_ascii=False, indent=2)

    print(f"词典文件已生成: {dict_path}")
    print(f"词条数量: {len(dict_entries)}")

    # 生成 dictionary.ts 索引条目
    index_entry = {
        "id": "beijing-grade12-english-vocab",
        "name": "北京高三英语课外词汇",
        "description": f"基于2024-2026年北京高三英语试卷（一模/二模/三模/期末/期中/月考）的课外高频词汇分析，共{len(dict_entries)}词，词频≥2",
        "category": "英语学习",
        "url": f"./dicts/{dict_filename}",
        "length": len(dict_entries),
        "language": "en"
    }

    # 保存索引条目（TypeScript 格式）
    ts_path = '/workspace/output/qwerty_dict/dictionary_entry.ts'
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write("// 将以下条目添加到 qwerty-learner 项目的 /resources/dictionary.ts 文件中\n")
        f.write("// 词典文件请放置在 /public/dicts/ 目录下\n\n")
        f.write("export const beijingGrade12Vocab = ")
        f.write(json.dumps(index_entry, ensure_ascii=False, indent=2))
        f.write(";\n")

    print(f"索引条目已生成: {ts_path}")

    # 同时保存一份纯 JSON 格式的索引条目
    index_path = '/workspace/output/qwerty_dict/dictionary_entry.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_entry, f, ensure_ascii=False, indent=2)

    # 统计
    print(f"\n统计信息:")
    print(f"  总词条数: {len(dict_entries)}")
    print(f"  有词性标注: {sum(1 for e in dict_entries if any('n.' in t or 'v.' in t or 'adj.' in t or 'adv.' in t for t in e['trans']))}")
    print(f"  有中文释义: {sum(1 for e in dict_entries if e['trans'] and e['trans'][0])}")

    # 显示前 5 个和后 5 个示例
    print(f"\n前 5 个词条:")
    for entry in dict_entries[:5]:
        print(f"  {entry['name']}: {entry['trans'][0]}")

    print(f"\n后 5 个词条:")
    for entry in dict_entries[-5:]:
        print(f"  {entry['name']}: {entry['trans'][0]}")

    return dict_entries


if __name__ == '__main__':
    convert_to_qwerty_format()
