const state = {
  lessons: [],
  roadmap: [],
  cardsByLessonId: {},
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
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`Không tải được ${path}`);
    return await response.json();
  } catch (error) {
    console.warn(`Lỗi khi tải ${path}:`, error);
    return null;
  }
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
      ${state.cardsByLessonId[lesson.id] ? '<span class="badge badge-success">Bản non-tech</span>' : ''}
    </button>
  `).join('');
}

window.checkAnswer = function(lessonId, questionIndex, optionIndex, correctIndex, explanation) {
  const containerId = `quiz-${lessonId.replace(/[^a-zA-Z0-9]/g, '-')}-${questionIndex}`;
  const container = document.getElementById(containerId);
  if (!container) return;

  const isCorrect = optionIndex === correctIndex;
  const buttons = container.querySelectorAll('button.quiz-option');
  
  buttons.forEach((btn, idx) => {
    btn.disabled = true;
    if (idx === correctIndex) {
      btn.classList.add('correct');
    } else if (idx === optionIndex && !isCorrect) {
      btn.classList.add('incorrect');
    }
  });

  const feedback = container.querySelector('.quiz-feedback');
  feedback.innerHTML = `<strong>${isCorrect ? '✅ Đúng!' : '❌ Sai rồi.'}</strong> ${escapeHtml(explanation)}`;
  feedback.style.display = 'block';
  feedback.className = `quiz-feedback ${isCorrect ? 'feedback-correct' : 'feedback-incorrect'}`;
};

function renderLessonDetail(lesson) {
  if (!lesson) {
    els.lessonDetail.innerHTML = '<p class="empty-state">Chọn một lesson để xem chi tiết.</p>';
    return;
  }

  const card = state.cardsByLessonId[lesson.id];
  let nontechHtml = '';

  if (card) {
    nontechHtml = `
      <h3>Học kiểu non-tech</h3>
      <div class="nontech-card-real">
        <h4>Tóm tắt ngắn gọn</h4>
        <p>${escapeHtml(card.plain_language_summary_vi)}</p>
        
        <h4>Vì sao cần hiểu?</h4>
        <p>${escapeHtml(card.why_it_matters_vi)}</p>
        
        <h4>Ẩn dụ đời thường</h4>
        <p>${escapeHtml(card.daily_life_analogy_vi)}</p>
        
        <h4>Mô hình tư duy</h4>
        <p>${escapeHtml(card.mental_model_vi)}</p>
        
        <h4>Ví dụ tối giản</h4>
        <p><code>${escapeHtml(card.minimal_example_vi)}</code></p>
        
        <h4>Dùng trong app AI thật</h4>
        <p>${escapeHtml(card.real_app_use_vi)}</p>
        
        <h4>Hiểu sai thường gặp</h4>
        <ul>
          ${(card.common_misunderstandings_vi || []).map(item => `<li>${escapeHtml(item)}</li>`).join('')}
        </ul>
        
        <h4>Nguồn tham chiếu</h4>
        <ul class="citation-list">
          ${(card.source_citations || []).map(cit => `<li><strong>${escapeHtml(cit.heading)}:</strong> "${escapeHtml(cit.quote)}" <br><small>(${escapeHtml(card.source_doc_path)})</small></li>`).join('')}
        </ul>

        <h4>Kiểm tra hiểu (Quiz)</h4>
        <div class="quiz-container">
          ${(card.check_questions || []).map((q, qIndex) => {
            const containerId = `quiz-${card.lesson_id.replace(/[^a-zA-Z0-9]/g, '-')}-${qIndex}`;
            return `
              <div class="quiz-question" id="${containerId}">
                <p><strong>Câu ${qIndex + 1}:</strong> ${escapeHtml(q.question)}</p>
                <div class="quiz-options">
                  ${q.options.map((opt, optIndex) => `
                    <button class="quiz-option" onclick="checkAnswer('${escapeHtml(card.lesson_id)}', ${qIndex}, ${optIndex}, ${q.correct}, '${escapeHtml(q.explanation)}')">
                      ${escapeHtml(opt)}
                    </button>
                  `).join('')}
                </div>
                <div class="quiz-feedback" style="display: none;"></div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  } else {
    const nontechBlocks = [
      'Nói như người thường',
      'Vấn đề thật nếu không hiểu khái niệm này',
      'Minh họa trực quan',
      'Code tối giản',
      'Dùng trong app AI thật',
    ];
    nontechHtml = `
      <h3>Học kiểu non-tech</h3>
      <div class="nontech-grid">
        ${nontechBlocks.map((block) => `<div class="nontech-card"><strong>${escapeHtml(block)}</strong><span class="detail-muted">Phase A mới dựng khung. Phase B sẽ tạo nội dung.</span></div>`).join('')}
      </div>
    `;
  }

  els.lessonDetail.innerHTML = `
    <p class="eyebrow">Chi tiết bài học</p>
    <h2>${escapeHtml(lesson.title)}</h2>
    <p class="detail-muted">${escapeHtml(lesson.doc_path)}</p>
    <div class="badges">
      <span class="badge">${escapeHtml(lesson.phase)}</span>
      <span class="badge">${escapeHtml(lesson.lesson)}</span>
      <span class="badge">${escapeHtml(lesson.time || 'Chưa có thời lượng')}</span>
      <span class="badge">${escapeHtml(lesson.type || 'Chưa có type')}</span>
      ${card ? `<span class="badge badge-success">Bản non-tech: ${escapeHtml(card.review_status)}</span>` : ''}
    </div>
    
    ${nontechHtml}

    <div class="detail-grid" style="margin-top: 2rem;">
      <div class="detail-box"><small>Languages</small>${escapeHtml((lesson.languages || []).join(', ') || 'Chưa khai báo')}</div>
      <div class="detail-box"><small>Prerequisites</small>${escapeHtml((lesson.prerequisites || []).join(', ') || 'Không có / chưa khai báo')}</div>
      <div class="detail-box"><small>Headings</small>${escapeHtml((lesson.headings || []).length)} mục</div>
      <div class="detail-box"><small>Code files</small>${escapeHtml((lesson.code_files || []).length)} file</div>
    </div>
    
    <h3>Headings trong lesson gốc</h3>
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
    const [lessonIndex, roadmapIndex, cardsData] = await Promise.all([
      loadJson('data/lessons.json'),
      loadJson('data/roadmap_12_weeks.json'),
      loadJson('data/nontech-cards/cards.demo.json')
    ]);
    
    if (lessonIndex) state.lessons = lessonIndex.lessons || [];
    if (roadmapIndex) state.roadmap = roadmapIndex.weeks || [];
    
    if (cardsData && cardsData.cards) {
      cardsData.cards.forEach(card => {
        state.cardsByLessonId[card.lesson_id] = card;
      });
    }

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
