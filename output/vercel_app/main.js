// 从 public 目录加载词典 JSON
let dictionary = [];
let words = [];

// 全局状态
const state = {
  currentMode: 'browse',
  filteredWords: [],
  currentPage: 1,
  pageSize: 40,
  practiceIndex: 0,
  practiceList: [],
  practiceKnown: new Set(),
  quizQuestions: [],
  quizIndex: 0,
  quizCorrect: 0,
  quizTotal: 0,
  quizAnswered: false,
};

// DOM 元素
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
  $('#total-count').textContent = '加载中...';
  setupNavigation();
  setupBrowse();
  setupPractice();
  setupQuiz();
  await loadDictionary();
});

async function loadDictionary() {
  try {
    const response = await fetch('./dicts/Beijing_Grade12_English_Vocab.json');
    dictionary = await response.json();
    processDictionary();
    $('#total-count').textContent = words.length;
    renderBrowse();
  } catch (err) {
    console.error('Failed to load dictionary:', err);
    $('#word-grid').innerHTML = '<p style="color:red;padding:20px;">词典加载失败，请刷新页面重试。</p>';
  }
}

function processDictionary() {
  words = dictionary.map((entry) => {
    const trans = entry.trans[0] || '';
    let pos = '';
    let meaning = '';
    const posMatch = trans.match(/^(n\.|v\.|adj\.|adv\.|prep\.|conj\.|pron\.|interj\.|num\.|art\.)/);
    if (posMatch) {
      pos = posMatch[1];
      meaning = trans.replace(posMatch[1], '').trim();
    } else {
      meaning = trans;
    }
    return {
      name: entry.name,
      pos: pos,
      meaning: meaning,
      trans: trans,
    };
  });

  // 为每个词估计词频
  words.forEach((w, i) => {
    w.freq = estimateFreq(i, words.length);
  });
}

function estimateFreq(rank, total) {
  if (rank <= 10) return 10 + (10 - rank);
  if (rank <= 30) return 7 + Math.floor((30 - rank) / 5);
  if (rank <= 60) return 4 + Math.floor((60 - rank) / 10);
  if (rank <= 120) return 3 + Math.floor((120 - rank) / 60);
  return 2 + Math.floor((total - rank) / total);
}

// 导航
function setupNavigation() {
  $$('.nav-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const mode = btn.dataset.mode;
      state.currentMode = mode;
      $$('.nav-btn').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      $$('.mode').forEach((m) => m.classList.remove('active'));
      $(`#mode-${mode}`).classList.add('active');
      if (mode === 'practice') initPractice();
      if (mode === 'quiz') initQuiz();
    });
  });
}

// ========== 浏览模式 ==========
function setupBrowse() {
  $('#search-input').addEventListener('input', () => {
    state.currentPage = 1;
    renderBrowse();
  });
  $('#filter-pos').addEventListener('change', () => {
    state.currentPage = 1;
    renderBrowse();
  });
  $('#filter-freq').addEventListener('change', () => {
    state.currentPage = 1;
    renderBrowse();
  });
}

function renderBrowse() {
  const query = $('#search-input').value.toLowerCase().trim();
  const posFilter = $('#filter-pos').value;
  const freqFilter = $('#filter-freq').value;

  state.filteredWords = words.filter((w) => {
    if (query && !w.name.toLowerCase().includes(query) && !w.meaning.includes(query)) return false;
    if (posFilter !== 'all' && w.pos !== posFilter) return false;
    if (freqFilter === 'high' && w.freq < 10) return false;
    if (freqFilter === 'mid' && (w.freq < 4 || w.freq >= 10)) return false;
    if (freqFilter === 'low' && w.freq >= 4) return false;
    return true;
  });

  const total = state.filteredWords.length;
  const totalPages = Math.ceil(total / state.pageSize);
  if (state.currentPage > totalPages) state.currentPage = Math.max(1, totalPages);

  const start = (state.currentPage - 1) * state.pageSize;
  const pageWords = state.filteredWords.slice(start, start + state.pageSize);

  const grid = $('#word-grid');
  grid.innerHTML = pageWords
    .map(
      (w) =>
        `<div class="word-card">
          <span class="freq">频次:${w.freq}</span>
          <div class="word">${w.name}</div>
          <div><span class="pos">${w.pos || ''}</span></div>
          <div class="meaning">${w.meaning}</div>
        </div>`
    )
    .join('');

  $(`#showing-count`).textContent = `显示 ${start + 1}-${Math.min(start + state.pageSize, total)} / ${total}`;
  renderPagination(totalPages);
}

function renderPagination(totalPages) {
  const pag = $('#pagination');
  if (totalPages <= 1) {
    pag.innerHTML = '';
    return;
  }

  let html = '';
  html += `<button ${state.currentPage <= 1 ? 'disabled' : ''} data-page="${state.currentPage - 1}">‹</button>`;

  const pages = [];
  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    pages.push(1);
    if (state.currentPage > 3) pages.push('...');
    for (let i = Math.max(2, state.currentPage - 1); i <= Math.min(totalPages - 1, state.currentPage + 1); i++) {
      pages.push(i);
    }
    if (state.currentPage < totalPages - 2) pages.push('...');
    pages.push(totalPages);
  }

  pages.forEach((p) => {
    if (p === '...') {
      html += `<span style="padding:8px">...</span>`;
    } else {
      html += `<button class="${p === state.currentPage ? 'active' : ''}" data-page="${p}">${p}</button>`;
    }
  });

  html += `<button ${state.currentPage >= totalPages ? 'disabled' : ''} data-page="${state.currentPage + 1}">›</button>`;

  pag.innerHTML = html;

  pag.querySelectorAll('button[data-page]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const page = parseInt(btn.dataset.page);
      if (page >= 1 && page <= totalPages) {
        state.currentPage = page;
        renderBrowse();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  });
}

// ========== 练习模式 ==========
function setupPractice() {
  $('#show-meaning-btn').addEventListener('click', showPracticeMeaning);
  $('#next-btn').addEventListener('click', nextPracticeWord);
  $('#known-btn').addEventListener('click', () => markPracticeWord(true));
  $('#unknown-btn').addEventListener('click', () => markPracticeWord(false));
  $('#practice-range').addEventListener('change', initPractice);
}

function initPractice() {
  const range = $('#practice-range').value;
  if (range === 'all') {
    state.practiceList = words.slice().sort(() => Math.random() - 0.5);
  } else if (range === 'high') {
    state.practiceList = words
      .filter((w) => w.freq >= 10)
      .sort(() => Math.random() - 0.5);
  } else {
    state.practiceList = words
      .slice()
      .reverse()
      .slice(0, 200)
      .sort(() => Math.random() - 0.5);
  }
  state.practiceIndex = 0;
  showPracticeWord();
}

function showPracticeWord() {
  if (state.practiceIndex >= state.practiceList.length) {
    state.practiceIndex = 0;
    state.practiceList.sort(() => Math.random() - 0.5);
  }

  const w = state.practiceList[state.practiceIndex];
  $('#practice-word').textContent = w.name;
  $('#practice-meaning').textContent = w.trans;
  $('#practice-meaning').style.display = 'none';
  $('#practice-counter').textContent = `${state.practiceIndex + 1} / ${state.practiceList.length}`;
  $('#practice-progress').style.width = `${(state.practiceIndex / state.practiceList.length) * 100}%`;

  $('#show-meaning-btn').style.display = '';
  $('#next-btn').style.display = 'none';
  $('#known-btn').style.display = 'none';
  $('#unknown-btn').style.display = 'none';
}

function showPracticeMeaning() {
  $('#practice-meaning').style.display = '';
  $('#show-meaning-btn').style.display = 'none';
  $('#known-btn').style.display = '';
  $('#unknown-btn').style.display = '';
  $('#next-btn').style.display = '';
}

function nextPracticeWord() {
  state.practiceIndex++;
  showPracticeWord();
}

function markPracticeWord(known) {
  if (known) {
    state.practiceKnown.add(state.practiceList[state.practiceIndex].name);
  }
  state.practiceIndex++;
  showPracticeWord();
}

// ========== 测试模式 ==========
function setupQuiz() {
  $('#quiz-next-btn').addEventListener('click', nextQuizQuestion);
}

function initQuiz() {
  state.quizIndex = 0;
  state.quizCorrect = 0;
  state.quizTotal = 0;
  state.quizAnswered = false;

  state.quizQuestions = generateQuizQuestions(20);
  showQuizQuestion();
}

function generateQuizQuestions(count) {
  const shuffled = words.slice().sort(() => Math.random() - 0.5);
  const selected = shuffled.slice(0, Math.min(count, shuffled.length));

  return selected.map((w) => {
    const others = words
      .filter((x) => x.name !== w.name)
      .sort(() => Math.random() - 0.5)
      .slice(0, 3);
    const options = [
      ...others.map((o) => ({ text: o.trans, correct: false })),
      { text: w.trans, correct: true },
    ];
    options.sort(() => Math.random() - 0.5);
    return { word: w.name, options: options };
  });
}

function showQuizQuestion() {
  if (state.quizIndex >= state.quizQuestions.length) {
    showQuizResult();
    return;
  }

  state.quizAnswered = false;
  const q = state.quizQuestions[state.quizIndex];

  $('#quiz-question').textContent = `"${q.word}" 的中文释义是？`;
  $('#quiz-counter').textContent = `${state.quizIndex + 1}/${state.quizQuestions.length}`;
  $('#quiz-progress').style.width = `${(state.quizIndex / state.quizQuestions.length) * 100}%`;
  $('#quiz-score').textContent = `得分: ${state.quizCorrect}/${state.quizTotal}`;
  $('#quiz-feedback').style.display = 'none';
  $('#quiz-next-btn').style.display = 'none';

  const optionsHtml = q.options
    .map(
      (opt, i) =>
        `<button class="quiz-option" data-index="${i}">${String.fromCharCode(65 + i)}. ${opt.text}</button>`
    )
    .join('');
  $('#quiz-options').innerHTML = optionsHtml;

  $('#quiz-options').querySelectorAll('.quiz-option').forEach((btn) => {
    btn.addEventListener('click', () => selectQuizAnswer(parseInt(btn.dataset.index)));
  });
}

function selectQuizAnswer(index) {
  if (state.quizAnswered) return;
  state.quizAnswered = true;

  const q = state.quizQuestions[state.quizIndex];
  const correct = q.options[index].correct;

  if (correct) state.quizCorrect++;
  state.quizTotal++;

  $$('#quiz-options .quiz-option').forEach((btn, i) => {
    btn.style.pointerEvents = 'none';
    if (q.options[i].correct) btn.classList.add('correct');
    if (i === index && !correct) btn.classList.add('wrong');
  });

  const feedback = $('#quiz-feedback');
  if (correct) {
    feedback.className = 'quiz-feedback correct';
    feedback.textContent = `✓ 正确！`;
  } else {
    feedback.className = 'quiz-feedback wrong';
    feedback.textContent = `✗ 正确答案: ${q.options.find((o) => o.correct).text}`;
  }
  feedback.style.display = '';

  $('#quiz-score').textContent = `得分: ${state.quizCorrect}/${state.quizTotal}`;
  $('#quiz-next-btn').style.display = '';
}

function nextQuizQuestion() {
  state.quizIndex++;
  showQuizQuestion();
}

function showQuizResult() {
  const pct = state.quizTotal > 0 ? Math.round((state.quizCorrect / state.quizTotal) * 100) : 0;
  let msg = '';
  if (pct >= 90) msg = '太棒了！';
  else if (pct >= 70) msg = '不错！';
  else if (pct >= 50) msg = '继续加油！';
  else msg = '多练习几遍吧！';

  $('#quiz-question').textContent = `${msg} 最终得分`;
  $('#quiz-options').innerHTML = `<div style="grid-column:1/-1;padding:30px;font-size:2.5em;font-weight:700;color:#d97757;">${state.quizCorrect} / ${state.quizTotal} (${pct}%)</div>`;
  $('#quiz-feedback').style.display = 'none';
  $('#quiz-next-btn').textContent = '再来一轮 →';
  $('#quiz-next-btn').style.display = '';
  $('#quiz-next-btn').onclick = initQuiz;
}
