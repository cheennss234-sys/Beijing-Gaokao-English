# 北京高三英语课外词汇 - 学习网站

1083 个基于 2024-2026 年北京高三英语试卷高频词分析的课外词汇。

## 功能

- **浏览模式**: 搜索、按词性/词频筛选、分页浏览
- **练习模式**: 随机顺序展示单词，点击显示释义，标记"认识/不认识"
- **测试模式**: 20 题四选一测试，即时反馈+得分统计

## 部署到 Vercel（最简单）

### 方法一：Vercel CLI（一行命令部署）

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 进入项目目录
cd vercel_app

# 3. 一行命令部署
vercel --prod
```

### 方法二：GitHub + Vercel 网页部署

1. 将 `vercel_app` 文件夹内容推送到你的 GitHub 仓库
2. 登录 [vercel.com](https://vercel.com)，导入该仓库
3. 保持默认构建设置，点击 Deploy
4. 部署完成后获得 `https://xxx.vercel.app` 网址

### 方法三：本地预览

```bash
cd vercel_app
npx vite preview
```

访问 http://localhost:4173

## 项目结构

```
vercel_app/
├── index.html          # 主页面
├── main.js             # 应用逻辑（浏览/练习/测试三种模式）
├── style.css           # 样式
├── package.json        # 依赖配置
├── vite.config.js      # Vite 配置
├── vercel.json         # Vercel 部署配置
├── public/
│   └── dicts/
│       └── Beijing_Grade12_English_Vocab.json  # 词典数据（1083 词）
└── dist/               # 构建输出（自动生）
```
