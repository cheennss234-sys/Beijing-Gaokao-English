# Tasks

- [x] Task 1: 数据收集 — 检索 2024-2026 北京各城区高三英语试卷
  - [x] SubTask 1.1: 检索 2024 年（东城、西城、海淀、朝阳等城区）高三期中、期末、一模、二模英语试卷文本
  - [x] SubTask 1.2: 检索 2025 年同上四类考试英语试卷文本
  - [x] SubTask 1.3: 检索 2026 年同上四类考试英语试卷文本（已发布部分）
  - [x] SubTask 1.4: 汇总试卷来源、年份、城区、考试类型元信息，记录覆盖缺口

- [x] Task 2: 文本预处理与课本词汇剔除
  - [x] SubTask 2.1: 整合所有试卷文本，进行清洗（去题号、选项标记、多余空白）
  - [x] SubTask 2.2: 分词 + 词形还原（lemmatization）+ 去停用词
  - [x] SubTask 2.3: 加载人教版 + 北师大版高中英语课本词汇表作为基准
  - [x] SubTask 2.4: 剔除课本内单词，保留课外单词

- [x] Task 3: 词频统计与排序
  - [x] SubTask 3.1: 统计每个课外单词的总出现次数
  - [x] SubTask 3.2: 仅保留出现次数 ≥3（超过 2 次）的单词
  - [x] SubTask 3.3: 按词频从高到低排序，同频按字母顺序

- [x] Task 4: 词性与中文释义标注
  - [x] SubTask 4.1: 为每个保留单词标注词性（n./v./adj./adv./prep./conj. 等）
  - [x] SubTask 4.2: 为每个保留单词标注中文释义
  - [x] SubTask 4.3: 组装为 `word (pos.) 中文释义` 格式

- [x] Task 5: 自审与纠错
  - [x] SubTask 5.1: 移除人名、地名、品牌名等专有名词
  - [x] SubTask 5.2: 移除标点残留、乱码、数字、非英文符号
  - [x] SubTask 5.3: 移除明显分词错误与课本内误入单词
  - [x] SubTask 5.4: 重新校验排序与格式

- [x] Task 6: 生成 TXT 文档
  - [x] SubTask 6.1: 生成纯文本词表，每行一个词条，含词频
  - [x] SubTask 6.2: 保存为 `/workspace/output/beijing_grade12_english_vocab.txt`

- [x] Task 7: 生成 Word 文档（应用 brand-guidelines）
  - [x] SubTask 7.1: 使用 python-docx 生成 .docx，应用 Anthropic 品牌配色（Dark `#141413`、Orange `#d97757` 等）与字体（标题 Poppins、正文 Lora）
  - [x] SubTask 7.2: 包含标题、说明、词频词表
  - [x] SubTask 7.3: 保存为 `/workspace/output/beijing_grade12_english_vocab.docx`

- [x] Task 8: 生成 PDF 文档（应用 brand-guidelines）
  - [x] SubTask 8.1: 使用 reportlab 或类似库生成 PDF，应用品牌配色与字体
  - [x] SubTask 8.2: 包含标题、说明、词频词表，结构与 Word 一致
  - [x] SubTask 8.3: 保存为 `/workspace/output/beijing_grade12_english_vocab.pdf`

- [x] Task 9: 生成 JSON Canvas 可视化（应用 json-canvas）
  - [x] SubTask 9.1: 创建 `.canvas` 文件，包含工作流程节点（数据收集→预处理→统计→自审→多格式输出）
  - [x] SubTask 9.2: 添加 Top 高频词示例节点
  - [x] SubTask 9.3: 节点间用边连接，校验 ID 唯一性与边引用完整性
  - [x] SubTask 9.4: 保存为 `/workspace/output/workflow.canvas`

# Task Dependencies
- Task 2 依赖 Task 1
- Task 3 依赖 Task 2
- Task 4 依赖 Task 3
- Task 5 依赖 Task 4
- Task 6、7、8、9 依赖 Task 5
- Task 6、7、8、9 之间无依赖，可并行
