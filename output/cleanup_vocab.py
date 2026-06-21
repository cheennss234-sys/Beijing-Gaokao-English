#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean up vocab_data.json:
- Remove OCR artifacts (3-5 letter combinations that aren't real words)
- Remove remaining proper nouns
- Add POS+meaning for valid words that were missed
- Ensure final word count is 1000+
"""

import json
import re

# Valid words that were missed by the dictionary (add POS + meaning)
ADDITIONAL_VOCAB = {
    'skirt': ('n.', '裙子'),
    'thieves': ('n.', '小偷（复数）'),
    'nationwide': ('adj.', '全国性的'),
    'afterwards': ('adv.', '后来；以后'),
    'cozy': ('adj.', '舒适的；惬意的'),
    'ream': ('n.', '令（纸张计量单位）'),
    'till': ('prep.', '直到'),
    'depressing': ('adj.', '令人沮丧的'),
    'gym': ('n.', '健身房；体育馆'),
    'weird': ('adj.', '奇怪的；古怪的'),
    'ere': ('prep.', '在...之前（古语）'),
    'nationwide': ('adj.', '全国性的'),
    'babe': ('n.', '婴儿；宝贝'),
    'mop': ('n.', '拖把'),
    'mile': ('n.', '英里'),
    'miles': ('n.', '英里（复数）'),
    'mum': ('n.', '妈妈（英式）'),
    'papa': ('n.', '爸爸'),
    'men': ('n.', '男人（复数）'),
    'women': ('n.', '女人（复数）'),
    'sold': ('v.', '卖（过去式）'),
    'bat': ('n.', '蝙蝠；球拍'),
    'fir': ('n.', '冷杉'),
    'abs': ('n.', '腹肌'),
    'ray': ('n.', '光线'),
    'eve': ('n.', '前夜'),
    'okay': ('adj.', '好的'),
    'pizza': ('n.', '披萨'),
    'cookies': ('n.', '饼干（复数）'),
    'snack': ('n.', '零食'),
    'snacks': ('n.', '零食（复数）'),
    'hamburger': ('n.', '汉堡包'),
    'soccer': ('n.', '足球'),
    'ballet': ('n.', '芭蕾舞'),
    'chaos': ('n.', '混乱'),
    'moth': ('n.', '飞蛾'),
    'lace': ('n.', '蕾丝；鞋带'),
    'rig': ('n.', '装备；钻井架'),
    'rid': ('v.', '摆脱'),
    'tee': ('n.', '球座'),
    'bes': ('n.', ''),  # filter out
    'ere': ('prep.', '在...之前'),
    'shift': ('n.', '转移；轮班'),
    'grind': ('v.', '磨碎；苦干'),
    'bond': ('n.', '纽带；债券'),
    'tech': ('n.', '科技'),
    'feet': ('n.', '脚（复数）'),
    'babe': ('n.', '婴儿'),
    'bored': ('adj.', '无聊的'),
    'upset': ('adj.', '心烦的'),
    'aside': ('adv.', '在旁边'),
    'asleep': ('adj.', '睡着的'),
    'chat': ('v.', '聊天'),
    'crack': ('n.', '裂缝'),
    'delight': ('n.', '快乐'),
    'deserve': ('v.', '应得'),
    'duet': ('n.', '二重奏'),
    'eatery': ('n.', '小餐馆'),
    'folks': ('n.', '人们；家属'),
    'grabbed': ('v.', '抓住（过去式）'),
    'grace': ('n.', '优雅'),
    'jersey': ('n.', '运动衫'),
    'okay': ('adj.', '好的'),
    'panicked': ('adj.', '惊慌的'),
    'progress': ('n.', '进步'),
    'scar': ('n.', '伤疤'),
    'sold': ('v.', '出售'),
    'summary': ('n.', '摘要'),
    'warmth': ('n.', '温暖'),
    'bulb': ('n.', '灯泡'),
    'buckets': ('n.', '桶（复数）'),
    'clapped': ('v.', '鼓掌（过去式）'),
    'compassion': ('n.', '同情心'),
    'cookies': ('n.', '饼干'),
    'damp': ('adj.', '潮湿的'),
    'donations': ('n.', '捐款（复数）'),
    'graduation': ('n.', '毕业'),
    'hesitation': ('n.', '犹豫'),
    'hikers': ('n.', '徒步者（复数）'),
    'hometown': ('n.', '家乡'),
    'injured': ('adj.', '受伤的'),
    'kneel': ('v.', '跪下'),
    'leap': ('v.', '跳跃'),
    'loneliness': ('n.', '孤独'),
    'miracle': ('n.', '奇迹'),
    'misread': ('v.', '读错'),
    'mobility': ('n.', '流动性'),
    'patience': ('n.', '耐心'),
    'penguins': ('n.', '企鹅（复数）'),
    'profound': ('adj.', '深刻的'),
    'retirement': ('n.', '退休'),
    'script': ('n.', '剧本'),
    'seagrass': ('n.', '海草'),
    'survival': ('n.', '生存'),
    'thankfully': ('adv.', '庆幸地'),
    'therapy': ('n.', '治疗'),
    'unknown': ('adj.', '未知的'),
    'website': ('n.', '网站'),
    'abundance': ('n.', '丰富'),
    'accent': ('n.', '口音'),
    'acupuncture': ('n.', '针灸'),
    'algorithms': ('n.', '算法（复数）'),
    'boost': ('v.', '提升'),
    'boxes': ('n.', '盒子（复数）'),
    'brightness': ('n.', '亮度'),
    'competitive': ('adj.', '竞争的'),
    'contestants': ('n.', '参赛者'),
    'countless': ('adj.', '无数的'),
    'deed': ('n.', '行为'),
    'diagnosed': ('v.', '诊断'),
    'disappointment': ('n.', '失望'),
    'distractions': ('n.', '干扰（复数）'),
    'diverse': ('adj.', '多样的'),
    'drifting': ('v.', '漂流'),
    'everyday': ('adj.', '日常的'),
    'exhaustion': ('n.', '疲惫'),
    'fabric': ('n.', '织物'),
    'feedback': ('n.', '反馈'),
    'firefighter': ('n.', '消防员'),
    'firefighters': ('n.', '消防员（复数）'),
    'fitness': ('n.', '健身'),
    'flashlight': ('n.', '手电筒'),
    'frustrated': ('adj.', '沮丧的'),
    'gently': ('adv.', '温柔地'),
    'gracefully': ('adv.', '优雅地'),
    'grapefruit': ('n.', '葡萄柚'),
    'heartwarming': ('adj.', '暖心的'),
    'hence': ('adv.', '因此'),
    'hesitantly': ('adv.', '犹豫地'),
    'hopefully': ('adv.', '有希望地'),
    'indigenous': ('adj.', '本土的'),
    'insensitivity': ('n.', '不敏感'),
    'investment': ('n.', '投资'),
    'invisible': ('adj.', '看不见的'),
    'isolating': ('v.', '隔离'),
    'legacy': ('n.', '遗产'),
    'messy': ('adj.', '凌乱的'),
    'miners': ('n.', '矿工（复数）'),
    'monsters': ('n.', '怪物（复数）'),
    'motivated': ('adj.', '有积极性的'),
    'muttered': ('v.', '嘀咕'),
    'nightlight': ('n.', '夜灯'),
    'nightmare': ('n.', '噩梦'),
    'nutrition': ('n.', '营养'),
    'occasional': ('adj.', '偶尔的'),
    'opponent': ('n.', '对手'),
    'orbisculate': ('v.', '（生造词）'),
    'overwhelming': ('adj.', '压倒性的'),
    'perfection': ('n.', '完美'),
    'possibilities': ('n.', '可能性（复数）'),
    'possibility': ('n.', '可能性'),
    'predictable': ('adj.', '可预测的'),
    'privilege': ('n.', '特权'),
    'rainforest': ('n.', '雨林'),
    'reflection': ('n.', '反思；倒影'),
    'requirements': ('n.', '要求（复数）'),
    'resilient': ('adj.', '有韧性的'),
    'restless': ('adj.', '焦躁的'),
    'reuse': ('v.', '再利用'),
    'ridiculous': ('adj.', '荒谬的'),
    'rural': ('adj.', '农村的'),
    'sandbags': ('n.', '沙袋（复数）'),
    'scan': ('v.', '扫描'),
    'sensitivity': ('n.', '敏感性'),
    'shaky': ('adj.', '摇晃的'),
    'stylish': ('adj.', '时尚的'),
    'symbolism': ('n.', '象征主义'),
    'symbolizes': ('v.', '象征'),
    'sympathetic': ('adj.', '同情的'),
    'symphony': ('n.', '交响乐'),
    'psychological': ('adj.', '心理的'),
    'mysterious': ('adj.', '神秘的'),
    'rhythmic': ('adj.', '节奏的'),
    'rhythm': ('n.', '节奏'),
    'gymnasts': ('n.', '体操运动员'),
    'schroeder': ('', ''),  # proper noun, filter
    # Additional valid words from second pass
    'clapping': ('v.', '鼓掌'),
    'glaring': ('adj.', '耀眼的'),
    'grabbing': ('v.', '抓住'),
    'imaginations': ('n.', '想象力（复数）'),
    'immune': ('adj.', '免疫的'),
    'judgments': ('n.', '判断（复数）'),
    'matted': ('adj.', '缠结的'),
    'mocked': ('v.', '嘲笑'),
    'mountainside': ('n.', '山腰'),
    'newfound': ('adj.', '新发现的'),
    'nicknamed': ('v.', '起绰号'),
    'pronounce': ('v.', '发音'),
    'questionings': ('n.', '质问'),
    'realising': ('v.', '意识到'),
    'recite': ('v.', '背诵'),
    'recited': ('v.', '背诵'),
    'recreated': ('v.', '重建'),
    'reunited': ('v.', '重聚'),
    'videocall': ('n.', '视频通话'),
    'wailed': ('v.', '哀号'),
    'orbisculated': ('v.', '（生造词）'),
}

# Additional proper nouns to remove
ADDITIONAL_PROPER_NOUNS = {
    'wang', 'asia', 'beth', 'brian', 'florida', 'hutfilz', 'ieraam', 'lara',
    'lear', 'phelps', 'riley', 'saturday', 'aaron', 'ted', 'thad', 'jerr',
    'february', 'march', 'january', 'june', 'august', 'monday', 'tuesday',
    'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
    'alice', 'brian', 'cara', 'dara', 'emma', 'grace', 'henry', 'ivan',
    'james', 'kate', 'lily', 'maria', 'nora', 'oliver', 'paul', 'quinn',
    'rachel', 'steve', 'tom', 'uma', 'vera', 'will', 'xavier', 'yuki', 'zoe',
    'norton', 'samuel', 'wyatt', 'emily', 'robert', 'clarice', 'kingsport',
    'lexi', 'rikki', 'rinehold', 'austin', 'amiri', 'dube', 'goldstein',
    'lewis', 'mcmillan', 'minmier', 'raynor', 'england', 'october',
    'september', 'july', 'monday', 'christmas', 'amazon', 'zumba', 'yoga',
    'pomodoro', 'hogarth', 'anna', 'mira', 'brittany', 'gertrude', 'luke',
    'joyce', 'squier', 'william', 'wyoming', 'chicago', 'schroeder',
    'chrystal', 'wukong', 'xuhua', 'jack', 'aria', 'larry', 'maya',
    'naidoo', 'sumi', 'blumberg', 'gombeau', 'sam', 'sara', 'travaris',
    'brandon', 'catherine', 'danny', 'dimeo', 'hugh', 'wilson', 'susan',
    'alex', 'dunn', 'max', 'tang', 'george', 'leo', 'regina', 'renwick',
    'steven', 'jake', 'marcus', 'nahmias', 'nosek', 'byrne', 'kofi', 'kung',
    'hannah', 'jessica', 'milo', 'smith', 'huang', 'zhao', 'shanghai',
    'shanxi', 'april', 'december', 'november',
    # Additional proper nouns from second pass
    'angeles', 'bonnie', 'breese', 'charles', 'claire', 'conteh', 'dammam',
    'deakin', 'delallo', 'dongting', 'ferrell', 'georgia', 'greece', 'greene',
    'hangzhou', 'hemingway', 'italian', 'jacksonville', 'joanne', 'jonathan',
    'lemieux', 'macdonald', 'mcdonald', 'mcneil', 'mengdan', 'naples', 'newton',
    'oxford', 'pennsylvania', 'portuguese', 'quebec', 'reykjavik', 'sierra',
    'singapore', 'smolyar', 'thierry', 'wensheng', 'colombian', 'scandinavians',
    'amirisa', 'avzageaaw', 'concem', 'erelesem', 'erelies', 'merbrs',
    'miehigeaw', 'miriga', 'ruitea', 'openclaw', 'leamed',
}

# OCR artifact patterns - words that are likely OCR errors
def is_ocr_artifact(word):
    """Check if a word is likely an OCR artifact."""
    # 3-4 letter words with no vowels (including y) are almost certainly OCR errors
    vowels = set('aeiouy')
    if len(word) <= 4 and not any(c in vowels for c in word):
        return True
    # 3-letter words that don't look like real English words
    if len(word) == 3:
        # Check if it's a common valid 3-letter word
        valid_3 = {'fly', 'wet', 'gym', 'bat', 'fir', 'abs', 'ray', 'eve',
                   'mop', 'tee', 'rig', 'rid', 'ion', 'bes', 'ere', 'les',
                   'ins', 'ion', 'oes', 'pes', 'ted'}
        if word not in valid_3:
            # Check if it has at least one vowel
            if not any(c in vowels for c in word):
                return True
    # 4-5 letter words with unusual patterns (no vowels in first 3 chars)
    if len(word) <= 5:
        first3 = word[:3]
        if not any(c in vowels for c in first3):
            return True
    return False


def clean_vocab_data():
    """Clean up the vocabulary data."""
    with open('/workspace/output/vocab_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_words = []
    removed_count = 0
    added_pos_count = 0

    for entry in data['words']:
        word = entry['word']
        freq = entry['frequency']

        # Skip proper nouns
        if word in ADDITIONAL_PROPER_NOUNS:
            removed_count += 1
            continue

        # Skip OCR artifacts
        if is_ocr_artifact(word):
            removed_count += 1
            continue

        # Add POS+meaning for words in additional vocab
        if word in ADDITIONAL_VOCAB:
            pos, meaning = ADDITIONAL_VOCAB[word]
            if pos:  # Only update if we have a POS
                entry['pos'] = pos
                if meaning:
                    entry['meaning'] = meaning
                added_pos_count += 1
            else:
                # Empty POS means it should be filtered
                removed_count += 1
                continue

        # Skip words that still have no POS and look suspicious
        if not entry['pos'] and not entry['meaning']:
            # Check if it's a valid word by length and pattern
            if len(word) >= 6 and re.match(r'^[a-z]+$', word):
                # Keep longer words that might be valid
                pass
            elif len(word) <= 5:
                # Short words with no POS are likely artifacts
                removed_count += 1
                continue

        cleaned_words.append(entry)

    # Re-rank
    for i, entry in enumerate(cleaned_words, 1):
        entry['rank'] = i

    # Update metadata
    data['metadata']['total_words'] = len(cleaned_words)
    data['words'] = cleaned_words

    # Save
    with open('/workspace/output/vocab_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Original words: {len(data['words']) + removed_count}")
    print(f"Removed: {removed_count}")
    print(f"Added POS from additional vocab: {added_pos_count}")
    print(f"Final words: {len(cleaned_words)}")

    # Count words with/without POS
    with_pos = sum(1 for w in cleaned_words if w['pos'])
    without_pos = sum(1 for w in cleaned_words if not w['pos'])
    print(f"With POS: {with_pos}")
    print(f"Without POS: {without_pos}")


if __name__ == '__main__':
    clean_vocab_data()
