const state = {
  lessons: [],
  roadmap: [],
  cardsByLessonId: {},
  placementQuestions: [],
  learningTracks: {},
  localTutorChunks: [],
  localTutorReady: false,
  selectedLessonId: null,
  aiTutorProxyUrl: 'http://127.0.0.1:8080/api/tutor/ask',
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

  // B4 Local Tutor
  tutorQuestion: document.querySelector('#tutorQuestion'),
  btnTutorSearch: document.querySelector('#btnTutorSearch'),
  tutorAnswer: document.querySelector('#tutorAnswer'),
  tutorResults: document.querySelector('#tutorResults'),
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

    <div class="ai-tutor-panel" style="margin-top: 2rem;">
      <div class="section-heading" style="margin-bottom: 12px;">
        <p class="eyebrow">Gia sư AI local</p>
        <h3 style="margin-top: 0;">Hỏi gia sư AI</h3>
        <p class="detail-muted">Hỏi một câu ngắn về bài đang học. Nếu proxy chưa chạy, app sẽ dùng Gia sư local hiện có.</p>
        <p class="privacy-warning" style="color: #f87171; font-size: 0.85em; margin-top: 6px;">Không nhập API key vào trình duyệt. API key chỉ được cấu hình trong local proxy trên máy của bạn.</p>
      </div>
      
      <div class="ai-tutor-controls">
        <textarea id="aiTutorQuestion-${lesson.id.replace(/[^a-zA-Z0-9]/g, '-')}" class="ai-tutor-question" rows="2" placeholder="Nhập câu hỏi của bạn..."></textarea>
        
        <div class="privacy-mode-grid">
          <label class="privacy-mode-card">
            <input type="radio" name="privacy_${lesson.id.replace(/[^a-zA-Z0-9]/g, '-')}" value="local_only" checked>
            <div class="privacy-text">
              <strong>Chỉ tìm trong máy — không gửi ra AI</strong>
              <small>An toàn nhất. Proxy chỉ dùng tìm kiếm local/fallback, không gọi provider AI.</small>
            </div>
          </label>
          <label class="privacy-mode-card">
            <input type="radio" name="privacy_${lesson.id.replace(/[^a-zA-Z0-9]/g, '-')}" value="public_curriculum_only">
            <div class="privacy-text">
              <strong>Hỏi AI bằng nội dung bài học công khai</strong>
              <small>Chỉ gửi câu hỏi và phần curriculum được truy xuất. Không gửi tiến độ học cá nhân.</small>
            </div>
          </label>
          <label class="privacy-mode-card">
            <input type="radio" name="privacy_${lesson.id.replace(/[^a-zA-Z0-9]/g, '-')}" value="learner_context_allowed">
            <div class="privacy-text">
              <strong>Cho AI biết tiến độ học tóm tắt của tôi</strong>
              <small>Chỉ gửi tóm tắt: bài hiện tại, track, bài đã hoàn thành, điểm quiz rút gọn.</small>
            </div>
          </label>
        </div>
        
        <div class="ai-tutor-actions">
          <button class="button primary" onclick="askAiTutor('${escapeHtml(lesson.id)}')">Hỏi gia sư AI</button>
        </div>
        <div id="aiTutorResult-${lesson.id.replace(/[^a-zA-Z0-9]/g, '-')}" class="ai-tutor-result" style="display: none;"></div>
      </div>
    </div>

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

// --- B4 Local Tutor Logic ---
const TUTOR_SYNONYMS = {
  rag: ['retrieval', 'truy xuất', 'tài liệu', 'nguồn', 'hỏi đáp'],
  prompt: ['prompting', 'câu lệnh', 'viết lệnh'],
  api: ['api key', 'key', 'mật khẩu', 'token', 'bảo mật'],
  embedding: ['vector', 'biểu diễn số', 'nhúng'],
  transformer: ['attention', 'chú ý', 'mô hình ngôn ngữ'],
  code: ['không biết code', 'non-tech', 'người mới']
};

function normalizeTutorText(value) {
  return String(value ?? '')
    .toLowerCase()
    .normalize('NFC')
    .replace(/[^\p{L}\p{N}\s/-]/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function tokenizeTutorQuery(query) {
  const normalized = normalizeTutorText(query);
  const tokens = normalized.split(' ').filter(token => token.length >= 2);
  const expanded = [...tokens];
  for (const token of tokens) {
    if (TUTOR_SYNONYMS[token]) expanded.push(...TUTOR_SYNONYMS[token]);
  }
  if (normalized.includes('api key')) expanded.push('api key', 'key', 'bảo mật');
  if (normalized.includes('không biết code')) expanded.push('không biết code', 'non-tech', 'người mới');
  return unique(expanded.map(normalizeTutorText));
}

function scoreTutorChunk(tokens, rawQuery, chunk) {
  const query = normalizeTutorText(rawQuery);
  const title = normalizeTutorText(chunk.title);
  const lessonId = normalizeTutorText(chunk.lesson_id || '');
  const text = normalizeTutorText(chunk.text);
  const section = normalizeTutorText(`${chunk.section || ''} ${chunk.citation_label || ''}`);
  const keywords = (chunk.keywords || []).map(normalizeTutorText);
  const currentTrack = state.progress.learner_profile?.recommended_track;
  let score = 0;

  if (query && (title.includes(query) || lessonId.includes(query))) score += 8;
  for (const token of tokens) {
    if (!token) continue;
    if (keywords.includes(token)) score += 5;
    if (title.includes(token)) score += 4;
    if (text.includes(token)) score += 2;
    if (section.includes(token)) score += 1;
  }
  if (currentTrack && (chunk.track_ids || []).includes(currentTrack)) score += 2;
  if (chunk.source_type === 'nontech_card') score += 2;
  return score;
}

function searchTutor(query) {
  if (!state.localTutorReady || !state.localTutorChunks.length) return [];
  const tokens = tokenizeTutorQuery(query);
  if (!tokens.length) return [];
  return state.localTutorChunks
    .map(chunk => ({ chunk, score: scoreTutorChunk(tokens, query, chunk) }))
    .filter(result => result.score >= 6)
    .sort((a, b) => b.score - a.score || a.chunk.chunk_id.localeCompare(b.chunk.chunk_id))
    .slice(0, 5);
}

function nextLessonForCurrentTrack() {
  const trackId = state.progress.learner_profile?.recommended_track;
  if (!trackId || !state.learningTracks[trackId]) return null;
  const lessonId = state.learningTracks[trackId].lessons.find(id => state.progress.lessons[id]?.status !== 'completed')
    || state.learningTracks[trackId].lessons[0];
  const lesson = state.lessons.find(item => item.id === lessonId);
  return lesson ? { trackId, lesson } : null;
}

function buildTutorAnswer(query, results) {
  if (!state.localTutorReady) {
    return '<p><strong>Chưa tải được chỉ mục gia sư local.</strong></p><p>Hãy chạy tool build index hoặc kiểm tra file <code>data/local_tutor_index.demo.json</code>.</p>';
  }
  if (!results.length) {
    return '<p><strong>Chưa đủ dữ liệu trong local index để trả lời chắc chắn.</strong></p><p>Thử hỏi bằng từ khóa như: RAG, prompt, API key, transformer, hoặc không biết code.</p>';
  }

  const best = results[0].chunk;
  const lesson = best.lesson_id ? state.lessons.find(item => item.id === best.lesson_id) : null;
  const next = nextLessonForCurrentTrack();
  const shortText = best.text.length > 360 ? `${best.text.slice(0, 360)}...` : best.text;
  const lessonButton = lesson
    ? `<button class="button secondary" data-tutor-lesson-id="${escapeHtml(lesson.id)}">Mở bài: ${escapeHtml(lesson.title)}</button>`
    : '';
  const nextText = next
    ? `<p><strong>Nếu theo track hiện tại:</strong> bước tiếp theo phù hợp là <em>${escapeHtml(next.lesson.title)}</em>.</p>`
    : '<p><strong>Gợi ý:</strong> Nếu chưa có track, hãy làm kiểm tra điểm bắt đầu để nhận lộ trình cá nhân.</p>';

  return `
    <p><strong>Mình tìm thấy phần liên quan nhất là:</strong> ${escapeHtml(best.citation_label)}.</p>
    <p><strong>Nói ngắn gọn:</strong> ${escapeHtml(shortText)}</p>
    ${lesson ? `<p><strong>Bài nên mở:</strong> ${escapeHtml(lesson.title)}</p>` : ''}
    ${nextText}
    <p><strong>Nguồn local:</strong> ${escapeHtml(best.source_path)} · ${escapeHtml(best.section)}</p>
    <div class="tutor-actions">${lessonButton}</div>
  `;
}

function renderTutorResults(results) {
  if (!els.tutorResults) return;
  if (!results.length) {
    els.tutorResults.innerHTML = '';
    return;
  }
  els.tutorResults.innerHTML = results.slice(0, 5).map(({ chunk, score }) => `
    <article class="tutor-result-card">
      <div class="badges">
        <span class="badge">score ${escapeHtml(score)}</span>
        <span class="badge">${escapeHtml(chunk.source_type)}</span>
      </div>
      <h3>${escapeHtml(chunk.title)}</h3>
      <p>${escapeHtml(chunk.citation_label)}</p>
      <small>${escapeHtml(chunk.source_path)} · ${escapeHtml(chunk.section)}</small>
    </article>
  `).join('');
}

function runTutorSearch() {
  const query = els.tutorQuestion?.value.trim() || '';
  if (!query) {
    els.tutorAnswer.innerHTML = '<p>Nhập một câu hỏi để tìm trong dữ liệu local.</p>';
    els.tutorResults.innerHTML = '';
    return;
  }
  const results = searchTutor(query);
  els.tutorAnswer.classList.remove('empty-state');
  els.tutorAnswer.innerHTML = buildTutorAnswer(query, results);
  renderTutorResults(results);
}
// ----------------------------

// --- C4 AI Tutor Proxy Integration ---

function getCurrentTrackId() {
  return state.progress.learner_profile?.recommended_track || null;
}

function buildLearnerContextSummary(privacyMode, lessonId) {
  if (privacyMode !== "learner_context_allowed") return undefined;
  
  const completed_lessons = [];
  const quiz_scores = [];
  
  // Extract up to 20 completed lessons and quiz scores
  for (const [id, lProg] of Object.entries(state.progress.lessons)) {
    if (lProg.status === 'completed') {
      completed_lessons.push(id);
    }
    if (lProg.quiz_attempts && lProg.quiz_attempts.length > 0) {
      const latest = lProg.quiz_attempts[lProg.quiz_attempts.length - 1];
      quiz_scores.push({
        lesson_id: id,
        latest_score: latest.score,
        latest_total: latest.total
      });
    }
  }
  
  return {
    current_lesson_id: lessonId,
    track_id: getCurrentTrackId(),
    completed_lessons: completed_lessons.slice(-20),
    quiz_scores: quiz_scores.slice(-20)
  };
}

function buildAiTutorPayload(question, privacyMode, lessonId) {
  const payload = {
    question: question,
    privacy_mode: privacyMode,
    lesson_id: lessonId,
    track_id: getCurrentTrackId()
  };
  
  const learnerContext = buildLearnerContextSummary(privacyMode, lessonId);
  if (learnerContext) {
    payload.learner_context = learnerContext;
  }
  
  return payload;
}

function escapeAiTutorResponseFields(resp) {
  return {
    status: escapeHtml(resp.status),
    answer_text: escapeHtml(resp.answer_text),
    provider_id: escapeHtml(resp.provider_id || resp.used_provider),
    privacy_mode: escapeHtml(resp.privacy_mode),
    citations: (resp.citations || []).map(escapeHtml),
    route_log: (resp.route_log || []).map(log => ({
      provider_id: escapeHtml(log.provider_id),
      status: escapeHtml(log.status),
      reason: escapeHtml(log.reason),
      error_type: escapeHtml(log.error_type)
    }))
  };
}

function runAiTutorLexicalFallback(question, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  const results = searchTutor(question);
  const answerHtml = buildTutorAnswer(question, results);
  
  container.innerHTML = `
    <div class="ai-tutor-fallback">
      <div class="ai-tutor-badge-row" style="margin-bottom: 8px;">
        <span class="badge ai-tutor-badge">Đã trả lời bằng fallback local</span>
      </div>
      <p class="detail-muted" style="margin-top: 8px; margin-bottom: 16px;">Proxy local chưa chạy hoặc không phản hồi. App đã dùng Gia sư local không gọi AI.</p>
      <div class="proxy-start-command">
        <small>Để bật AI Tutor proxy, mở terminal ở repo root và chạy:</small>
        <code>$env:PYTHONPATH="ai-learning-companion"<br>py -m ai_tutor_proxy.server</code>
      </div>
      <div class="ai-tutor-answer-content" style="margin-top: 16px;">
        ${answerHtml}
      </div>
    </div>
  `;
}

function renderAiTutorOfflineFallback(question, error, containerId) {
  const container = document.getElementById(containerId);
  if (container) {
    container.classList.remove('loading');
    container.style.display = 'block';
  }
  runAiTutorLexicalFallback(question, containerId);
}

function renderAiTutorRoute(routeLog) {
  if (!routeLog || routeLog.length === 0) return '';
  const latest = routeLog[routeLog.length - 1];
  const reason = latest.reason || latest.status || latest.error_type || 'unknown';
  return `Đường đi: ${latest.provider_id} · ${reason}`;
}

function renderAiTutorResponse(resp, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  
  container.classList.remove('loading');
  container.style.display = 'block';
  
  const safeResp = escapeAiTutorResponseFields(resp);
  
  let providerLabel = safeResp.provider_id;
  if (providerLabel === 'local_lexical') providerLabel = 'Fallback local';
  else if (providerLabel === 'mock') providerLabel = 'Mock provider — kiểm thử, không gọi API thật';
  else if (providerLabel === 'gemini') providerLabel = 'Provider: Gemini';
  else if (providerLabel === 'openai_compatible') providerLabel = 'Provider: OpenAI-compatible';
  
  const formattedAnswer = safeResp.answer_text.replace(/\n/g, '<br>');
  
  const citationsHtml = safeResp.citations.length > 0 
    ? `<div style="margin-top: 12px;"><small class="detail-muted">Nguồn: ${safeResp.citations.join(', ')}</small></div>` 
    : '';

  container.innerHTML = `
    <div class="ai-tutor-response-box">
      <div class="ai-tutor-badge-row" style="margin-bottom: 12px; display: flex; gap: 8px; flex-wrap: wrap;">
        <span class="badge ai-tutor-badge">${providerLabel}</span>
        <span class="badge ai-tutor-badge">Mode: ${safeResp.privacy_mode}</span>
      </div>
      <div class="ai-tutor-answer-content" style="line-height: 1.6;">
        ${formattedAnswer}
      </div>
      ${citationsHtml}
      <div class="ai-tutor-route" style="margin-top: 12px; font-size: 0.85em; color: var(--muted);">
        ${renderAiTutorRoute(safeResp.route_log)}
      </div>
    </div>
  `;
}

async function askAiTutor(lessonId) {
  const safeId = lessonId.replace(/[^a-zA-Z0-9]/g, '-');
  const questionEl = document.getElementById(`aiTutorQuestion-${safeId}`);
  const containerId = `aiTutorResult-${safeId}`;
  const container = document.getElementById(containerId);
  
  if (!questionEl || !container) return;
  
  const question = questionEl.value.trim();
  if (!question) {
    container.style.display = 'block';
    container.innerHTML = '<p class="ai-tutor-error">Nhập một câu hỏi ngắn trước khi hỏi gia sư.</p>';
    return;
  }
  
  const privacyRadios = document.getElementsByName(`privacy_${safeId}`);
  let privacyMode = 'local_only';
  for (const radio of privacyRadios) {
    if (radio.checked) {
      privacyMode = radio.value;
      break;
    }
  }
  
  if (!['local_only', 'public_curriculum_only', 'learner_context_allowed'].includes(privacyMode)) {
    privacyMode = 'local_only';
  }
  
  container.style.display = 'block';
  container.classList.add('loading');
  container.innerHTML = '<p>Đang xử lý...</p>';
  
  const payload = buildAiTutorPayload(question, privacyMode, lessonId);
  
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);
  
  try {
    const response = await fetch(state.aiTutorProxyUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload),
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (response.status === 400) {
      container.classList.remove('loading');
      container.innerHTML = '<p class="ai-tutor-error">Câu hỏi chưa hợp lệ. Vui lòng nhập lại.</p>';
      return;
    } else if (response.status === 500) {
      container.innerHTML = '<p class="ai-tutor-error" style="margin-bottom: 12px;">Proxy gặp lỗi nội bộ. App đã dùng Gia sư local để không làm gián đoạn bài học.</p>';
      renderAiTutorOfflineFallback(question, new Error('Server 500'), containerId);
      return;
    } else if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    
    const data = await response.json();
    renderAiTutorResponse(data, containerId);
    
  } catch (error) {
    clearTimeout(timeoutId);
    renderAiTutorOfflineFallback(question, error, containerId);
  }
}

// ----------------------------

function bindEvents() {
  els.searchInput.addEventListener('input', renderLessonList);
  els.phaseFilter.addEventListener('change', renderLessonList);
  els.lessonList.addEventListener('click', (event) => {
    const button = event.target.closest('[data-lesson-id]');
    if (button) selectLesson(button.dataset.lessonId);
  });
  if (els.btnClosePlacement) els.btnClosePlacement.addEventListener('click', closePlacementTest);
  if (els.btnSubmitPlacement) els.btnSubmitPlacement.addEventListener('click', submitPlacementTest);
  if (els.btnTutorSearch) els.btnTutorSearch.addEventListener('click', runTutorSearch);
  if (els.tutorQuestion) {
    els.tutorQuestion.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) runTutorSearch();
    });
  }
  if (els.tutorAnswer) {
    els.tutorAnswer.addEventListener('click', (event) => {
      const button = event.target.closest('[data-tutor-lesson-id]');
      if (!button) return;
      document.getElementById('lessons').scrollIntoView({ behavior: 'smooth' });
      selectLesson(button.dataset.tutorLessonId);
    });
  }
}

async function init() {
  bindEvents();
  loadProgress(); // Load B2 local storage
  
  try {
    const [lessonIndex, roadmapIndex, cardsData, questionsData, tracksData, tutorIndex] = await Promise.all([
      loadJson('data/lessons.json'),
      loadJson('data/roadmap_12_weeks.json'),
      loadJson('data/nontech-cards/cards.demo.json'),
      loadJson('data/placement_questions.json'),
      loadJson('data/learning_tracks.json'),
      loadJson('data/local_tutor_index.demo.json')
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
    if (tutorIndex && Array.isArray(tutorIndex.chunks)) {
      state.localTutorChunks = tutorIndex.chunks;
      state.localTutorReady = true;
    } else if (els.tutorAnswer) {
      els.tutorAnswer.innerHTML = 'Chưa tải được chỉ mục gia sư local. Các phần học khác vẫn dùng bình thường.';
    }

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
