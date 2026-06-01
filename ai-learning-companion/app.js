const state = {
  lessons: [],
  roadmap: [],
  selectedLessonId: null,
};

const els = {
  statLessons: document.querySelector('#statLessons'),
  statPhases: document.querySelector('#statPhases'),
  statCodeFiles: document.querySelector('#statCodeFiles'),
  roadmapGrid: document.querySelector('#roadmapGrid'),
  lessonList: document.querySelector('#lessonList'),
  lessonDetail: document.querySelector('#lessonDetail'),
  searchInput: document.querySelector('#searchInput'),
  phaseFilter: document.querySelector('#phaseFilter'),
};

async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Không tải được ${path}`);
  return response.json();
}

function unique(values) {
  return [...new Set(values)].filter(Boolean).sort();
}

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function renderStats() {
  const phases = unique(state.lessons.map((lesson) => lesson.phase));
  const codeFiles = state.lessons.reduce((total, lesson) => total + (lesson.code_files?.length || 0), 0);
  els.statLessons.textContent = state.lessons.length.toLocaleString('vi-VN');
  els.statPhases.textContent = phases.length.toLocaleString('vi-VN');
  els.statCodeFiles.textContent = codeFiles.toLocaleString('vi-VN');
}

function renderRoadmap() {
  els.roadmapGrid.innerHTML = state.roadmap.map((week) => `
    <article class="roadmap-card">
      <div class="week">Tuần ${escapeHtml(week.week)} · ${escapeHtml(week.suggested_hours)} giờ</div>
      <h3>${escapeHtml(week.title_vi)}</h3>
      <p>${escapeHtml(week.nontech_summary_vi)}</p>
      <div class="badges">
        ${(week.focus_phases || []).map((phase) => `<span class="badge">${escapeHtml(phase)}</span>`).join('')}
      </div>
    </article>
  `).join('');
}

function renderPhaseFilter() {
  const phases = unique(state.lessons.map((lesson) => lesson.phase));
  els.phaseFilter.innerHTML = '<option value="">Tất cả phase</option>' + phases
    .map((phase) => `<option value="${escapeHtml(phase)}">${escapeHtml(phase)}</option>`)
    .join('');
}

function filteredLessons() {
  const query = els.searchInput.value.trim().toLowerCase();
  const phase = els.phaseFilter.value;
  return state.lessons.filter((lesson) => {
    const haystack = `${lesson.title} ${lesson.phase} ${lesson.lesson} ${lesson.doc_path}`.toLowerCase();
    return (!query || haystack.includes(query)) && (!phase || lesson.phase === phase);
  });
}

function renderLessonList() {
  const lessons = filteredLessons();
  if (!lessons.length) {
    els.lessonList.innerHTML = '<p class="empty-state">Không tìm thấy lesson phù hợp.</p>';
    return;
  }
  els.lessonList.innerHTML = lessons.map((lesson) => `
    <button class="lesson-card ${lesson.id === state.selectedLessonId ? 'active' : ''}" data-lesson-id="${escapeHtml(lesson.id)}">
      <strong>${escapeHtml(lesson.title)}</strong>
      <p>${escapeHtml(lesson.id)}</p>
    </button>
  `).join('');
}

function renderLessonDetail(lesson) {
  if (!lesson) {
    els.lessonDetail.innerHTML = '<p class="empty-state">Chọn một lesson để xem chi tiết.</p>';
    return;
  }

  const nontechBlocks = [
    'Nói như người thường',
    'Vấn đề thật nếu không hiểu khái niệm này',
    'Minh họa trực quan',
    'Code tối giản',
    'Dùng trong app AI thật',
  ];

  els.lessonDetail.innerHTML = `
    <p class="eyebrow">Chi tiết bài học</p>
    <h2>${escapeHtml(lesson.title)}</h2>
    <p class="detail-muted">${escapeHtml(lesson.doc_path)}</p>
    <div class="badges">
      <span class="badge">${escapeHtml(lesson.phase)}</span>
      <span class="badge">${escapeHtml(lesson.lesson)}</span>
      <span class="badge">${escapeHtml(lesson.time || 'Chưa có thời lượng')}</span>
      <span class="badge">${escapeHtml(lesson.type || 'Chưa có type')}</span>
    </div>
    <div class="detail-grid">
      <div class="detail-box"><small>Languages</small>${escapeHtml((lesson.languages || []).join(', ') || 'Chưa khai báo')}</div>
      <div class="detail-box"><small>Prerequisites</small>${escapeHtml((lesson.prerequisites || []).join(', ') || 'Không có / chưa khai báo')}</div>
      <div class="detail-box"><small>Headings</small>${escapeHtml((lesson.headings || []).length)} mục</div>
      <div class="detail-box"><small>Code files</small>${escapeHtml((lesson.code_files || []).length)} file</div>
    </div>
    <h3>Học kiểu non-tech</h3>
    <div class="nontech-grid">
      ${nontechBlocks.map((block) => `<div class="nontech-card"><strong>${escapeHtml(block)}</strong><span class="detail-muted">Phase A mới dựng khung. Phase B sẽ tạo nội dung.</span></div>`).join('')}
    </div>
    <h3>Headings trong lesson</h3>
    <ul class="list-inline">
      ${(lesson.headings || []).slice(0, 14).map((heading) => `<li>H${escapeHtml(heading.level)} · ${escapeHtml(heading.text)}</li>`).join('') || '<li>Không có heading.</li>'}
    </ul>
    <h3>Code files</h3>
    <ul class="list-inline">
      ${(lesson.code_files || []).slice(0, 14).map((file) => `<li>${escapeHtml(file)}</li>`).join('') || '<li>Không có code file.</li>'}
    </ul>
  `;
}

function selectLesson(id) {
  state.selectedLessonId = id;
  const lesson = state.lessons.find((item) => item.id === id);
  renderLessonList();
  renderLessonDetail(lesson);
}

function bindEvents() {
  els.searchInput.addEventListener('input', renderLessonList);
  els.phaseFilter.addEventListener('change', renderLessonList);
  els.lessonList.addEventListener('click', (event) => {
    const button = event.target.closest('[data-lesson-id]');
    if (button) selectLesson(button.dataset.lessonId);
  });
}

async function init() {
  bindEvents();
  try {
    const [lessonIndex, roadmapIndex] = await Promise.all([
      loadJson('data/lessons.json'),
      loadJson('data/roadmap_12_weeks.json'),
    ]);
    state.lessons = lessonIndex.lessons || [];
    state.roadmap = roadmapIndex.weeks || [];
    renderStats();
    renderRoadmap();
    renderPhaseFilter();
    renderLessonList();
    if (state.lessons.length) selectLesson(state.lessons[0].id);
  } catch (error) {
    els.lessonDetail.innerHTML = `<p class="empty-state">${escapeHtml(error.message)}. Hãy chạy scanner trước.</p>`;
  }
}

init();
