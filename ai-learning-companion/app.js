const state = {
  lessons: [],
  roadmap: [],
  cardsByLessonId: {},
  placementQuestions: [],
  learningTracks: {},
  selectedLessonId: null,
  progress: {
    version: 1,
    last_opened_lesson_id: null,
    learner_profile: null,
    lessons: {}
  }
};

const PROGRESS_KEY = 'aiLearningCompanion.progress.v1';

const els = {
  statLessons: document.querySelector('#statLessons'),
  statPhases: document.querySelector('#statPhases'),
  statCodeFiles: document.querySelector('#statCodeFiles'),
  roadmapGrid: document.querySelector('#roadmapGrid'),
  lessonList: document.querySelector('#lessonList'),
  lessonDetail: document.querySelector('#lessonDetail'),
  searchInput: document.querySelector('#searchInput'),
  phaseFilter: document.querySelector('#phaseFilter'),
  
  // B2
  startLearningPanel: document.querySelector('#startLearningPanel'),
  progCompleted: document.querySelector('#progCompleted'),
  progReview: document.querySelector('#progReview'),
  totalLessonsInTrack: document.querySelector('#totalLessonsInTrack'),
  btnStartLearning: document.querySelector('#btnStartLearning'),
  btnResetProgress: document.querySelector('#btnResetProgress'),
  btnTakePlacement: document.querySelector('#btnTakePlacement'),
  recommendedTrackContainer: document.querySelector('#recommendedTrackContainer'),
  trackName: document.querySelector('#trackName'),
  trackDesc: document.querySelector('#trackDesc'),
  
  // B3 Modal
  placementTestModal: document.querySelector('#placementTestModal'),
  btnClosePlacement: document.querySelector('#btnClosePlacement'),
  btnSubmitPlacement: document.querySelector('#btnSubmitPlacement'),
  placementQuestionsContainer: document.querySelector('#placementQuestionsContainer'),
};

// --- Progress Logic (Gate B2) ---
function loadProgress() {
  try {
    const data = localStorage.getItem(PROGRESS_KEY);
    if (data) {
      const parsed = JSON.parse(data);
      if (!parsed.learner_profile) {
        parsed.learner_profile = null; // Migration for B2 to B3
      }
      state.progress = parsed;
    }
  } catch (e) {
    console.warn("Could not load progress from localStorage", e);
  }
}

function saveProgress() {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(state.progress));
    updateDashboard();
    renderLessonList();
  } catch (e) {
    console.warn("Could not save progress to localStorage", e);
  }
}

function resetProgress() {
  if (confirm("Bạn có chắc chắn muốn xóa toàn bộ tiến độ học tập và kết quả kiểm tra điểm bắt đầu trên trình duyệt này? Thao tác này không thể hoàn tác.")) {
    state.progress = {
      version: 1,
      last_opened_lesson_id: null,
      learner_profile: null,
      lessons: {}
    };
    saveProgress();
    if (state.selectedLessonId) selectLesson(state.selectedLessonId);
  }
}

function updateProgressStatus(lessonId, status, quizAttempt = null) {
  if (!state.progress.lessons[lessonId]) {
    state.progress.lessons[lessonId] = {
      status: 'not_started',
      last_opened_at: new Date().toISOString(),
      quiz_attempts: []
    };
  }
  
  state.progress.last_opened_lesson_id = lessonId;
  const lProg = state.progress.lessons[lessonId];
  lProg.last_opened_at = new Date().toISOString();
  
  if (status) {
    lProg.status = status;
    if (status === 'completed') {
      lProg.completed_at = new Date().toISOString();
    }
  }
  
  if (quizAttempt) {
    lProg.quiz_attempts.push(quizAttempt);
  }
  
  saveProgress();
}

function updateDashboard() {
  if (!els.startLearningPanel) return;
  
  const totalCards = Object.keys(state.cardsByLessonId).length;
  if (totalCards === 0) return; // No demo cards loaded
  
  els.startLearningPanel.style.display = 'block';
  
  const profile = state.progress.learner_profile;
  const defaultFirstLesson = "00-setup-and-tooling/01-dev-environment";
  let targetLessonId = state.progress.last_opened_lesson_id;
  let totalInTrack = totalCards;
  let trackLessons = null;
  
  if (profile && profile.recommended_track && state.learningTracks && state.learningTracks[profile.recommended_track]) {
    const track = state.learningTracks[profile.recommended_track];
    trackLessons = track.lessons;
    if (els.recommendedTrackContainer) els.recommendedTrackContainer.style.display = 'block';
    if (els.trackName) els.trackName.textContent = track.name;
    if (els.trackDesc) els.trackDesc.textContent = track.description;
    if (els.btnTakePlacement) els.btnTakePlacement.textContent = "Làm lại kiểm tra";
    
    totalInTrack = track.lessons.length;
    
    // Find next lesson in track
    if (!targetLessonId || !track.lessons.includes(targetLessonId) || state.progress.lessons[targetLessonId]?.status === 'completed') {
      const nextUncompleted = track.lessons.find(id => state.progress.lessons[id]?.status !== 'completed');
      targetLessonId = nextUncompleted || track.lessons[0];
    }
    
    if (state.progress.last_opened_lesson_id) {
       els.btnStartLearning.textContent = "Học tiếp theo track của tôi";
    } else {
       els.btnStartLearning.textContent = "Bắt đầu track của tôi";
    }
  } else {
    if (els.recommendedTrackContainer) els.recommendedTrackContainer.style.display = 'none';
    if (els.btnTakePlacement) els.btnTakePlacement.textContent = "Kiểm tra điểm bắt đầu";
    targetLessonId = targetLessonId || defaultFirstLesson;
    
    if (state.progress.last_opened_lesson_id) {
      els.btnStartLearning.textContent = "Học tiếp bài gần nhất";
    } else {
      els.btnStartLearning.textContent = "Học bài đầu tiên";
    }
  }
  
  let completed = 0;
  let review = 0;
  
  for (const [id, lProg] of Object.entries(state.progress.lessons)) {
    if (trackLessons && !trackLessons.includes(id)) continue;
    
    if (lProg.status === 'completed') completed++;
    if (lProg.status === 'review') review++;
  }
  
  els.progCompleted.textContent = completed;
  els.progReview.textContent = review;
  
  if (els.totalLessonsInTrack) els.totalLessonsInTrack.textContent = totalInTrack;
  
  els.btnStartLearning.onclick = () => {
    // scroll to lesson section
    document.getElementById('lessons').scrollIntoView({ behavior: 'smooth' });
    selectLesson(targetLessonId);
  };
  
  els.btnResetProgress.onclick = resetProgress;
  if (els.btnTakePlacement) els.btnTakePlacement.onclick = openPlacementTest;
}
// ---------------------------------

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
  els.lessonList.innerHTML = lessons.map((lesson) => {
    const hasCard = state.cardsByLessonId[lesson.id];
    const lProg = state.progress.lessons[lesson.id];
    
    let extraBadges = '';
    if (hasCard) {
      extraBadges += `<span class="badge badge-success">Bản non-tech</span> `;
    }
    if (lProg) {
      if (lProg.status === 'completed') extraBadges += `<span class="badge badge-completed">✅ Đã hiểu</span> `;
      if (lProg.status === 'review') extraBadges += `<span class="badge badge-review">⚠️ Cần ôn</span> `;
    }
    
    return `
      <button class="lesson-card ${lesson.id === state.selectedLessonId ? 'active' : ''}" data-lesson-id="${escapeHtml(lesson.id)}">
        <strong>${escapeHtml(lesson.title)}</strong>
        <p>${escapeHtml(lesson.id)}</p>
        <div class="badges" style="margin-top: 8px; margin-bottom: 0;">${extraBadges}</div>
      </button>
    `;
  }).join('');
}

// B2 Quiz Logic
window.submitQuiz = function(lessonId) {
  const card = state.cardsByLessonId[lessonId];
  if (!card) return;
  
  const questions = card.check_questions || [];
  let score = 0;
  const answers = [];
  
  questions.forEach((q, qIndex) => {
    const formName = `q_${lessonId}_${qIndex}`;
    const selected = document.querySelector(`input[name="${formName}"]:checked`);
    
    const container = document.getElementById(`quiz-${lessonId.replace(/[^a-zA-Z0-9]/g, '-')}-${qIndex}`);
    const labels = container.querySelectorAll('.quiz-option-label');
    
    // reset styling
    labels.forEach(l => {
      l.classList.remove('correct', 'incorrect');
      l.querySelector('input').disabled = true; // disable after submit
    });
    
    const selectedVal = selected ? parseInt(selected.value, 10) : -1;
    answers.push(selectedVal);
    
    if (selectedVal === q.correct) {
      score++;
      if (selectedVal >= 0) labels[selectedVal].classList.add('correct');
    } else {
      if (selectedVal >= 0) labels[selectedVal].classList.add('incorrect');
      if (q.correct >= 0) labels[q.correct].classList.add('correct'); // highlight correct one
    }
  });
  
  const feedbackEl = document.getElementById(`quiz-feedback-${lessonId.replace(/[^a-zA-Z0-9]/g, '-')}`);
  const btnSubmit = document.getElementById(`btn-submit-${lessonId.replace(/[^a-zA-Z0-9]/g, '-')}`);
  if (btnSubmit) btnSubmit.disabled = true;
  
  let suggestion = '';
  let newStatus = 'started';
  if (score === questions.length && questions.length > 0) {
    suggestion = "🎉 Xuất sắc! Bạn có thể học bài tiếp theo.";
    newStatus = 'completed';
    feedbackEl.className = 'quiz-feedback feedback-correct';
  } else {
    suggestion = "💡 Nên đọc lại phần giải thích và thử lại (bạn có thể tải lại trang để làm lại).";
    newStatus = 'review';
    feedbackEl.className = 'quiz-feedback feedback-incorrect';
  }
  
  feedbackEl.innerHTML = `<strong>Điểm số: ${score}/${questions.length}</strong><br>${suggestion}`;
  feedbackEl.style.display = 'block';
  
  const attempt = {
    score: score,
    total: questions.length,
    answers: answers,
    at: new Date().toISOString()
  };
  updateProgressStatus(lessonId, newStatus, attempt);
  
  // Re-render detail to show new action buttons state if needed, 
  // but just updating buttons here is cleaner. We'll rely on the re-render.
  renderLessonDetail(state.lessons.find(l => l.id === lessonId));
};

window.markStatus = function(lessonId, status) {
  updateProgressStatus(lessonId, status);
  renderLessonDetail(state.lessons.find(l => l.id === lessonId));
};

function renderLessonDetail(lesson) {
  if (!lesson) {
    els.lessonDetail.innerHTML = '<p class="empty-state">Chọn một lesson để xem chi tiết.</p>';
    return;
  }

  const card = state.cardsByLessonId[lesson.id];
  let nontechHtml = '';

  if (card) {
    // Record start
    const currentStatus = state.progress.lessons[lesson.id]?.status;
    updateProgressStatus(lesson.id, (!currentStatus || currentStatus === 'not_started') ? 'started' : undefined);
    
    const safeId = lesson.id.replace(/[^a-zA-Z0-9]/g, '-');
    const lProg = state.progress.lessons[lesson.id];
    
    nontechHtml = `
      <h3>Học kiểu non-tech</h3>
      <div class="lesson-player">
        
        <div class="player-step">
          <div class="step-header">
            <div class="step-number">1</div>
            <h4 class="step-title">Mục tiêu bài học</h4>
          </div>
          <div class="step-content">
            <p>${escapeHtml(card.plain_language_summary_vi)}</p>
          </div>
        </div>
        
        <div class="player-step">
          <div class="step-header">
            <div class="step-number">2</div>
            <h4 class="step-title">Vì sao cần hiểu?</h4>
          </div>
          <div class="step-content">
            <p>${escapeHtml(card.why_it_matters_vi)}</p>
          </div>
        </div>
        
        <div class="player-step">
          <div class="step-header">
            <div class="step-number">3</div>
            <h4 class="step-title">Ẩn dụ đời thường</h4>
          </div>
          <div class="step-content">
            <p>${escapeHtml(card.daily_life_analogy_vi)}</p>
          </div>
        </div>
        
        <div class="player-step">
          <div class="step-header">
            <div class="step-number">4</div>
            <h4 class="step-title">Mô hình tư duy</h4>
          </div>
          <div class="step-content">
            <p>${escapeHtml(card.mental_model_vi)}</p>
          </div>
        </div>
        
        <div class="player-step">
          <div class="step-header">
            <div class="step-number">5</div>
            <h4 class="step-title">Ví dụ tối giản</h4>
          </div>
          <div class="step-content">
            <code>${escapeHtml(card.minimal_example_vi)}</code>
          </div>
        </div>
        
        <div class="player-step">
          <div class="step-header">
            <div class="step-number">6</div>
            <h4 class="step-title">Dùng trong app AI thật</h4>
          </div>
          <div class="step-content">
            <p>${escapeHtml(card.real_app_use_vi)}</p>
          </div>
        </div>
        
        <div class="player-step">
          <div class="step-header">
            <div class="step-number">7</div>
            <h4 class="step-title">Hiểu sai thường gặp</h4>
          </div>
          <div class="step-content">
            <ul>
              ${(card.common_misunderstandings_vi || []).map(item => `<li>${escapeHtml(item)}</li>`).join('')}
            </ul>
          </div>
        </div>
        
        <div class="player-step">
          <div class="step-header">
            <div class="step-number">8</div>
            <h4 class="step-title">Kiểm tra hiểu (Quiz)</h4>
          </div>
          <div class="step-content">
            <div class="quiz-form">
              ${(card.check_questions || []).map((q, qIndex) => {
                const containerId = `quiz-${safeId}-${qIndex}`;
                return `
                  <div class="quiz-question" id="${containerId}">
                    <p><strong>Câu ${qIndex + 1}:</strong> ${escapeHtml(q.question)}</p>
                    <div class="quiz-options">
                      ${q.options.map((opt, optIndex) => `
                        <label class="quiz-option-label">
                          <input type="radio" name="q_${escapeHtml(card.lesson_id)}_${qIndex}" value="${optIndex}">
                          <span>${escapeHtml(opt)}</span>
                        </label>
                      `).join('')}
                    </div>
                  </div>
                `;
              }).join('')}
              
              <div class="quiz-actions">
                <button id="btn-submit-${safeId}" class="button primary" onclick="submitQuiz('${escapeHtml(card.lesson_id)}')">Nộp bài kiểm tra</button>
                <div id="quiz-feedback-${safeId}" class="quiz-feedback" style="display: none;"></div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="player-step">
          <div class="step-header">
            <div class="step-number">9</div>
            <h4 class="step-title">Nguồn tham chiếu</h4>
          </div>
          <div class="step-content">
            <ul class="citation-list">
              ${(card.source_citations || []).map(cit => `<li><strong>${escapeHtml(cit.heading)}:</strong> "${escapeHtml(cit.quote)}" <br><small>(${escapeHtml(card.source_doc_path)})</small></li>`).join('')}
            </ul>
          </div>
        </div>
        
        <div class="player-actions">
           <button class="button ${lProg?.status === 'completed' ? 'primary' : 'secondary'}" onclick="markStatus('${escapeHtml(card.lesson_id)}', 'completed')">✅ Đánh dấu đã hiểu</button>
           <button class="button ${lProg?.status === 'review' ? 'primary' : 'secondary'}" onclick="markStatus('${escapeHtml(card.lesson_id)}', 'review')">⚠️ Cần ôn lại</button>
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

// --- B3 Placement Test Logic ---
function openPlacementTest() {
  if (els.placementTestModal) els.placementTestModal.style.display = 'flex';
  renderPlacementTest();
}

function closePlacementTest() {
  if (els.placementTestModal) els.placementTestModal.style.display = 'none';
}

function renderPlacementTest() {
  if (!els.placementQuestionsContainer) return;
  
  if (!state.placementQuestions.length) {
    els.placementQuestionsContainer.innerHTML = '<p>Không tải được câu hỏi.</p>';
    return;
  }
  
  els.placementQuestionsContainer.innerHTML = state.placementQuestions.map((q, index) => {
    return `
      <div class="placement-question">
        <h4>Câu ${index + 1}: ${escapeHtml(q.text)}</h4>
        <div class="quiz-options">
          ${q.options.map(opt => `
            <label class="quiz-option-label" style="font-weight: normal;">
              <input type="radio" name="place_${q.id}" value="${escapeHtml(opt.id)}">
              <span>${escapeHtml(opt.text)}</span>
            </label>
          `).join('')}
        </div>
      </div>
    `;
  }).join('');
}

function submitPlacementTest() {
  if (!state.placementQuestions || state.placementQuestions.length === 0) {
    alert("Chưa tải được câu hỏi kiểm tra.");
    return;
  }

  const TRACK_TIE_BREAK_ORDER = ['work_ai_user', 'workflow_operator', 'ai_engineer_from_scratch'];
  const scores = { work_ai_user: 0, workflow_operator: 0, ai_engineer_from_scratch: 0 };
  let allAnswered = true;
  
  state.placementQuestions.forEach(q => {
    const selected = document.querySelector(`input[name="place_${q.id}"]:checked`);
    if (!selected) {
      allAnswered = false;
    } else {
      const opt = q.options.find(o => o.id === selected.value);
      if (opt && opt.scores) {
        for (const [track, score] of Object.entries(opt.scores)) {
          scores[track] = (scores[track] || 0) + score;
        }
      }
    }
  });
  
  if (!allAnswered) {
    alert("Vui lòng trả lời tất cả các câu hỏi để có kết quả chính xác nhất!");
    return;
  }
  
  let bestTrack = TRACK_TIE_BREAK_ORDER[0];
  let maxScore = -1;
  
  for (const track of TRACK_TIE_BREAK_ORDER) {
    if (scores[track] > maxScore) {
      maxScore = scores[track];
      bestTrack = track;
    }
  }
  
  state.progress.learner_profile = {
    placement_completed: true,
    recommended_track: bestTrack,
    placement_score: scores,
    completed_at: new Date().toISOString()
  };
  
  saveProgress();
  closePlacementTest();
  document.getElementById('startLearningPanel').scrollIntoView({ behavior: 'smooth' });
}

function bindEvents() {
  els.searchInput.addEventListener('input', renderLessonList);
  els.phaseFilter.addEventListener('change', renderLessonList);
  els.lessonList.addEventListener('click', (event) => {
    const button = event.target.closest('[data-lesson-id]');
    if (button) selectLesson(button.dataset.lessonId);
  });
  if (els.btnClosePlacement) els.btnClosePlacement.addEventListener('click', closePlacementTest);
  if (els.btnSubmitPlacement) els.btnSubmitPlacement.addEventListener('click', submitPlacementTest);
}

async function init() {
  bindEvents();
  loadProgress(); // Load B2 local storage
  
  try {
    const [lessonIndex, roadmapIndex, cardsData, questionsData, tracksData] = await Promise.all([
      loadJson('data/lessons.json'),
      loadJson('data/roadmap_12_weeks.json'),
      loadJson('data/nontech-cards/cards.demo.json'),
      loadJson('data/placement_questions.json'),
      loadJson('data/learning_tracks.json')
    ]);
    
    if (lessonIndex) state.lessons = lessonIndex.lessons || [];
    if (roadmapIndex) state.roadmap = roadmapIndex.weeks || [];
    
    if (cardsData && cardsData.cards) {
      cardsData.cards.forEach(card => {
        state.cardsByLessonId[card.lesson_id] = card;
      });
    }
    
    if (questionsData) state.placementQuestions = questionsData;
    if (tracksData) state.learningTracks = tracksData;

    renderStats();
    renderRoadmap();
    renderPhaseFilter();
    updateDashboard(); // Initial dashboard render
    renderLessonList();
    
    if (state.lessons.length) selectLesson(state.lessons[0].id);
  } catch (error) {
    els.lessonDetail.innerHTML = `<p class="empty-state">${escapeHtml(error.message)}. Hãy chạy scanner trước.</p>`;
  }
}

init();
