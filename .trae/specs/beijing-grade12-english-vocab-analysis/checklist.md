# Checklist

- [x] 数据收集覆盖 2024、2025、2026 三年北京多个城区（东城、西城、海淀、朝阳等）的期中、期末、一模、二模英语试卷
- [x] 试卷来源、年份、城区、考试类型元信息已记录，覆盖缺口已说明
- [x] 文本已完成清洗（去题号、选项标记、多余空白）
- [x] 已完成分词、词形还原、去停用词
- [x] 已加载人教版 + 北师大版高中英语课本词汇表作为基准
- [x] 课本内单词已剔除，仅保留课外单词
- [x] 词频统计仅保留出现次数 ≥3（超过 2 次）的单词
- [x] 词表按词频从高到低排序，同频按字母顺序
- [x] 每个词条格式为 `word (pos.) 中文释义`
- [x] 已移除人名、地名、品牌名等专有名词
- [x] 已移除标点残留、乱码、数字、非英文符号
- [x] 已移除明显分词错误与课本内误入单词
- [x] TXT 文档已生成，路径为 `/workspace/output/beijing_grade12_english_vocab.txt`
- [x] Word 文档已生成，应用 Anthropic 品牌配色与字体，路径为 `/workspace/output/beijing_grade12_english_vocab.docx`
- [x] PDF 文档已生成，应用 Anthropic 品牌配色与字体，路径为 `/workspace/output/beijing_grade12_english_vocab.pdf`
- [x] JSON Canvas 文件已生成，包含工作流程节点与 Top 高频词示例，路径为 `/workspace/output/workflow.canvas`
- [x] Canvas 文件通过校验：ID 唯一、边引用完整、JSON 合法
- [x] 三份文档（PDF/Word/TXT）内容一致
