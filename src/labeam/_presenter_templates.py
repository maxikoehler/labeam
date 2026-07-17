# ruff: noqa: E501
"""HTML/CSS/JS templates for the presenter view.

Kept in a dedicated module so that the embedded multi-line strings
(which contain HTML, CSS, and JavaScript) are exempt from the
line-length rule (E501) without suppressing it project-wide.
"""

from __future__ import annotations

_PRESENTER_CSS = """\
/* ---- Presenter theme variables ---- */
:root { --p-accent: #009999; }

[data-theme="dark"] {
  --p-bg:           #0d0d1a;
  --p-sidebar-bg:   #0a0a18;
  --p-border:       #1e1e33;
  --p-border-inner: #2a2a44;
  --p-text:         #d0d0e0;
  --p-text-muted:   #8888aa;
  --p-label:        #555577;
  --p-slide-bg:     #1a1a2e;
  --p-input-bg:     #0d0d1f;
  --p-input-text:   #b0b0cc;
  --p-btn-bg:       #1e1e33;
  --p-btn-border:   #2e2e4e;
  --p-clock-color:  #c0c0d8;
  --p-slide-filter: invert(1) hue-rotate(180deg);
}

[data-theme="light"] {
  --p-bg:           #f4f4f6;
  --p-sidebar-bg:   #ffffff;
  --p-border:       #e0e0e6;
  --p-border-inner: #d4d4de;
  --p-text:         #1a1a2a;
  --p-text-muted:   #5a5a6a;
  --p-label:        #9090a0;
  --p-slide-bg:     #f8f8fc;
  --p-input-bg:     #fafafe;
  --p-input-text:   #2a2a3a;
  --p-btn-bg:       #ebebf2;
  --p-btn-border:   #d0d0da;
  --p-clock-color:  #3a3a4a;
  --p-slide-filter: none;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  height: 100%; overflow: hidden;
  font-family: Arial, 'Segoe UI', system-ui, sans-serif;
  background: var(--p-bg); color: var(--p-text);
  font-size: 14px;
  transition: background 0.2s, color 0.2s;
}

/* Root layout */
.root {
  display: grid;
  grid-template-columns: 1fr 340px;
  height: 100vh;
}

/* Left panel — current slide fills it entirely */
.left {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 12px;
  overflow: hidden;
  min-width: 0;
}

.current-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-height: 0;
}

.slide-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--p-label);
}

.slide-preview {
  flex: 1;
  position: relative;
  display: block;
  background: var(--p-slide-bg);
  border: 1px solid var(--p-border-inner);
  border-radius: 6px;
  overflow: hidden;
  min-height: 0;
}

.slide-preview img {
  width: 100%;
  height: auto;
  display: block;
  filter: var(--p-slide-filter);
  transition: filter 0.3s;
}

.slide-preview.current { border-color: var(--p-accent); }

/* Received laser dot inside current-slide preview */
.presenter-laser {
  position: absolute;
  width: 26px; height: 26px;
  border-radius: 50%;
  pointer-events: none;
  opacity: 0;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle,
    rgba(255,110,110,1) 0%, rgba(255,40,40,0.95) 26%,
    rgba(255,0,0,0.65) 44%, rgba(255,0,0,0.12) 68%,
    rgba(255,0,0,0) 100%);
  box-shadow: 0 0 0 2px rgba(255,60,60,0.24), 0 0 22px rgba(255,0,0,0.65);
  transition: opacity 0.15s;
  z-index: 10;
}

/* Navigation bar */
.nav-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  padding: 0 2px;
}

.nav-btn {
  background: var(--p-btn-bg);
  border: 1px solid var(--p-btn-border);
  color: var(--p-text-muted);
  padding: 6px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.15s, color 0.15s;
}
.nav-btn:hover:not(:disabled) { background: var(--p-accent); color: #fff; border-color: var(--p-accent); }
.nav-btn:disabled { opacity: 0.3; cursor: default; }

.slide-counter {
  font-size: 13px;
  color: var(--p-text-muted);
  font-variant-numeric: tabular-nums;
  min-width: 64px;
  text-align: center;
}

.spacer { flex: 1; }

.laser-btn {
  background: var(--p-btn-bg);
  border: 1px solid var(--p-btn-border);
  color: var(--p-text-muted);
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.15s, color 0.15s;
}
.laser-btn.active { background: rgba(200,0,0,0.2); color: #ff7070; border-color: #cc3333; }

/* Sidebar */
.sidebar {
  display: flex;
  flex-direction: column;
  background: var(--p-sidebar-bg);
  border-left: 1px solid var(--p-border);
  overflow: hidden;
  transition: background 0.2s;
}

.sidebar-section {
  padding: 10px 12px;
  border-bottom: 1px solid var(--p-border);
  flex-shrink: 0;
}

/* Time row */
.time-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
}

.clock {
  font-size: 18px;
  font-variant-numeric: tabular-nums;
  color: var(--p-clock-color);
  letter-spacing: 0.04em;
  font-weight: 300;
}

.timer {
  font-size: 18px;
  font-variant-numeric: tabular-nums;
  color: var(--p-accent);
  letter-spacing: 0.04em;
  font-weight: 600;
}

.timer-btn, .theme-btn {
  background: var(--p-btn-bg);
  border: 1px solid var(--p-btn-border);
  color: var(--p-text-muted);
  padding: 3px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.15s;
}
.timer-btn:hover, .theme-btn:hover { background: var(--p-border-inner); color: var(--p-text); }

/* Notes (compact fixed height) */
.notes-wrap {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  padding: 10px 12px;
  gap: 4px;
  border-bottom: 1px solid var(--p-border);
}

.notes-wrap h3, .sidebar-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--p-label);
  flex-shrink: 0;
  margin-bottom: 4px;
}

.notes-wrap textarea {
  height: 110px;
  background: var(--p-input-bg);
  border: 1px solid var(--p-border);
  border-radius: 4px;
  color: var(--p-input-text);
  font-size: 12px;
  line-height: 1.5;
  padding: 6px;
  resize: none;
  outline: none;
  font-family: inherit;
  transition: border-color 0.15s;
}
.notes-wrap textarea:focus { border-color: var(--p-accent); }

.notes-saved {
  font-size: 10px;
  color: #44aa88;
  height: 12px;
  flex-shrink: 0;
  transition: opacity 0.4s;
  opacity: 0;
}
.notes-saved.show { opacity: 1; }

/* Next slide preview in sidebar */
.next-sidebar {
  flex-shrink: 0;
  height: 200px;
  display: flex;
  flex-direction: column;
  padding: 10px 12px;
  gap: 4px;
  border-bottom: 1px solid var(--p-border);
}

.next-preview {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--p-slide-bg);
  border: 1px solid var(--p-border-inner);
  border-radius: 4px;
  overflow: hidden;
  min-height: 0;
}

.next-preview img {
  max-width: 100%; max-height: 100%;
  object-fit: contain;
  display: block;
  filter: var(--p-slide-filter);
  transition: filter 0.3s;
}

/* Slide grid (1 column, scrollable) */
.grid-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 10px 12px;
  min-height: 0;
  overflow: hidden;
}

.slide-grid {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0;
  overflow-y: auto;
  min-height: 0;
  padding-right: 2px;
}

.grid-thumb {
  background: var(--p-slide-bg);
  border: 1px solid var(--p-border-inner);
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  transition: border-color 0.15s;
  width: 100%;
  margin-bottom: 14px;
  flex-shrink: 0;
}

.grid-thumb:last-child { margin-bottom: 0; }
.grid-thumb:hover { border-color: var(--p-text-muted); }
.grid-thumb.active { border-color: var(--p-accent); box-shadow: 0 0 0 2px rgba(0,153,153,0.3); }

.grid-thumb img {
  width: 100%;
  height: auto;
  display: block;
  filter: var(--p-slide-filter);
}

.grid-num {
  display: block;
  text-align: center;
  font-size: 11px;
  font-weight: 500;
  padding: 4px 4px 5px;
  color: var(--p-text-muted);
  background: var(--p-slide-bg);
  border-top: 1px solid var(--p-border-inner);
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--p-border-inner); border-radius: 2px; }
"""

_PRESENTER_JS = """\
(function() {
  var WS_PORT  = {ws_port};
  var TOTAL    = {total};
  var current  = 0;
  var ws, reconnectTimer;

  // DOM refs
  var imgCurrent  = document.getElementById('imgCurrent');
  var imgNext     = document.getElementById('imgNext');
  var counterEl   = document.getElementById('slideCounter');
  var btnPrev     = document.getElementById('btnPrev');
  var btnNext     = document.getElementById('btnNext');
  var laserBtn    = document.getElementById('laserBtn');
  var noteArea    = document.getElementById('noteArea');
  var notesSaved  = document.getElementById('notesSaved');
  var timerEl     = document.getElementById('timer');
  var clockEl     = document.getElementById('clock');
  var timerToggle = document.getElementById('timerToggle');
  var grid        = document.getElementById('slideGrid');
  var nextWrap    = document.getElementById('nextWrap');
  var presLaser   = document.getElementById('presenterLaser');

  // ---- WebSocket ----
  var laserActive = false;

  function connect() {
    ws = new WebSocket('ws://localhost:' + WS_PORT);
    ws.onopen = function() { console.log('[presenter] WS connected'); };
    ws.onmessage = function(e) {
      var msg = JSON.parse(e.data);
      if (msg.type === 'state') {
        applyState(msg.index);
      } else if (msg.type === 'notes') {
        applyNotes(msg.data);
      } else if (msg.type === 'darkmode') {
        applyDarkMode(msg.dark, false);
      } else if (msg.type === 'laser') {
        applyLaser(msg);
      }
    };
    ws.onclose = function() {
      clearTimeout(reconnectTimer);
      reconnectTimer = setTimeout(connect, 2000);
    };
  }

  function send(obj) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(obj));
    }
  }

  // ---- Dark mode ----
  function applyDarkMode(dark, broadcast) {
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    var btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = dark ? '\\u2600' : '\\u263E';
    if (broadcast) send({ type: 'darkmode', dark: dark });
  }

  window.toggleTheme = function() {
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    applyDarkMode(!isDark, true);
  };

  // ---- Received laser display (in current-slide preview) ----
  function applyLaser(msg) {
    if (!presLaser) return;
    if (msg.active) {
      var rect       = imgCurrent.getBoundingClientRect();
      var parentRect = presLaser.parentElement.getBoundingClientRect();
      presLaser.style.left    = (rect.left - parentRect.left + msg.x * rect.width)  + 'px';
      presLaser.style.top     = (rect.top  - parentRect.top  + msg.y * rect.height) + 'px';
      presLaser.style.opacity = '1';
    } else {
      presLaser.style.opacity = '0';
    }
  }

  // ---- Slide state ----
  function applyState(index) {
    current = index;
    imgCurrent.src = '/slide/' + index;
    imgCurrent.alt = 'Slide ' + (index + 1);
    var nextIdx = index + 1;
    if (nextIdx < TOTAL) {
      imgNext.src = '/slide/' + nextIdx;
      imgNext.alt = 'Slide ' + (nextIdx + 1);
      if (nextWrap) nextWrap.style.visibility = 'visible';
    } else {
      if (nextWrap) nextWrap.style.visibility = 'hidden';
    }
    counterEl.textContent = (index + 1) + ' / ' + TOTAL;
    btnPrev.disabled = (index === 0);
    btnNext.disabled = (index === TOTAL - 1);
    noteArea.value = allNotes[String(index)] || '';
    updateGrid(index);
  }

  function goto(index) {
    if (index < 0 || index >= TOTAL) return;
    send({ type: 'goto', index: index });
    if (!timerRunning) startTimer();
  }

  window.gotoSlide = goto;
  window.gotoPrev  = function() { goto(current - 1); };
  window.gotoNext  = function() { goto(current + 1); };

  // ---- Notes ----
  var allNotes = {};
  var noteDebounce;

  function applyNotes(data) {
    allNotes = data || {};
    noteArea.value = allNotes[String(current)] || '';
  }

  noteArea.addEventListener('input', function() {
    clearTimeout(noteDebounce);
    noteDebounce = setTimeout(function() {
      allNotes[String(current)] = noteArea.value;
      send({ type: 'note', index: current, text: noteArea.value });
      notesSaved.classList.add('show');
      setTimeout(function() { notesSaved.classList.remove('show'); }, 1500);
    }, 500);
  });

  // ---- Laser pointer (send from presenter, coords relative to current-slide image) ----
  document.addEventListener('mousemove', function(e) {
    if (!laserActive) return;
    var rect = imgCurrent.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return;
    var x = (e.clientX - rect.left) / rect.width;
    var y = (e.clientY - rect.top)  / rect.height;
    send({
      type: 'laser', active: true,
      x: Math.max(0, Math.min(1, x)),
      y: Math.max(0, Math.min(1, y))
    });
  }, { passive: true });

  window.toggleLaser = function() {
    laserActive = !laserActive;
    laserBtn.classList.toggle('active', laserActive);
    if (!laserActive) send({ type: 'laser', active: false, x: 0, y: 0 });
  };

  // ---- Timer ----
  var timerRunning = false;
  var timerMs      = 0;
  var timerInterval;
  var timerLastTick;

  function startTimer() {
    if (timerRunning) return;
    timerRunning   = true;
    timerLastTick  = Date.now();
    timerToggle.textContent = '\\u23F8';
    timerInterval  = setInterval(tickTimer, 100);
  }

  function pauseTimer() {
    timerRunning = false;
    timerToggle.textContent = '\\u25B6';
    clearInterval(timerInterval);
  }

  function tickTimer() {
    var now  = Date.now();
    timerMs += now - timerLastTick;
    timerLastTick = now;
    var total = Math.floor(timerMs / 1000);
    var h = Math.floor(total / 3600);
    var m = Math.floor((total % 3600) / 60);
    var s = total % 60;
    timerEl.textContent =
      (h > 0 ? pad2(h) + ':' : '') + pad2(m) + ':' + pad2(s);
  }

  function pad2(n) { return n < 10 ? '0' + n : String(n); }

  timerToggle.addEventListener('click', function() {
    if (timerRunning) pauseTimer(); else startTimer();
  });

  // ---- Clock ----
  function updateClock() {
    var d = new Date();
    clockEl.textContent = pad2(d.getHours()) + ':' + pad2(d.getMinutes()) + ':' + pad2(d.getSeconds());
  }
  setInterval(updateClock, 1000);
  updateClock();

  // ---- Slide grid ----
  function buildGrid() {
    grid.innerHTML = '';
    for (var i = 0; i < TOTAL; i++) {
      var thumb = document.createElement('div');
      thumb.className = 'grid-thumb' + (i === 0 ? ' active' : '');
      thumb.id = 'thumb-' + i;
      thumb.dataset.index = i;
      thumb.innerHTML =
        '<img src="/slide/' + i + '" loading="lazy" alt="Slide ' + (i + 1) + '">' +
        '<span class="grid-num">Slide ' + (i + 1) + '</span>';
      thumb.addEventListener('click', (function(idx) {
        return function() { goto(idx); };
      })(i));
      grid.appendChild(thumb);
    }
  }

  function updateGrid(index) {
    var prev = grid.querySelector('.grid-thumb.active');
    if (prev) prev.classList.remove('active');
    var next = document.getElementById('thumb-' + index);
    if (next) {
      next.classList.add('active');
      next.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  // ---- Keyboard ----
  document.addEventListener('keydown', function(e) {
    if (e.target === noteArea) return;
    if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); goto(current + 1); }
    else if (e.key === 'ArrowLeft')              { e.preventDefault(); goto(current - 1); }
    else if (e.key === 'Home')                   { e.preventDefault(); goto(0); }
    else if (e.key === 'End')                    { e.preventDefault(); goto(TOTAL - 1); }
    else if (e.key === 'l' || e.key === 'L')     { window.toggleLaser(); }
    else if (e.key === 'd' || e.key === 'D')     { window.toggleTheme(); }
  });

  // ---- Boot ----
  buildGrid();
  connect();
  // Sync theme button icon with initial data-theme attribute
  var _tb = document.getElementById('themeBtn');
  if (_tb) _tb.textContent = document.documentElement.getAttribute('data-theme') === 'dark'
    ? '\\u2600' : '\\u263E';
})();
"""

_PRESENTER_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Presenter View</title>
  <style>
{css}
  </style>
</head>
<body>
<div class="root">

  <!-- ===== Left panel: current slide ===== -->
  <div class="left">
    <div class="current-wrap">
      <span class="slide-label">Current</span>
      <div class="slide-preview current">
        <img id="imgCurrent" src="/slide/0" alt="Slide 1">
        <div class="presenter-laser" id="presenterLaser"></div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="nav-bar">
      <button class="nav-btn" id="btnPrev" onclick="gotoPrev()" disabled
              title="Previous (&#8592;)">&#8592;</button>
      <button class="nav-btn" id="btnNext" onclick="gotoNext()"
              title="Next (&#8594; / Space)">&#8594;</button>
      <span class="slide-counter" id="slideCounter">1 / {total}</span>
      <div class="spacer"></div>
      <button class="laser-btn" id="laserBtn" onclick="toggleLaser()"
              title="Laser pointer (L)">&#11044; Laser</button>
    </div>
  </div>

  <!-- ===== Right sidebar ===== -->
  <div class="sidebar">

    <!-- Clock + Timer + Theme toggle -->
    <div class="sidebar-section">
      <div class="time-row">
        <span class="clock" id="clock">00:00:00</span>
        <button class="timer-btn" id="timerToggle" title="Start / pause timer">&#9654;</button>
        <span class="timer" id="timer">00:00</span>
        <button class="theme-btn" id="themeBtn" onclick="toggleTheme()"
                title="Toggle dark / light mode (D)">&#9790;</button>
      </div>
    </div>

    <!-- Notes (compact) -->
    <div class="notes-wrap">
      <h3>Notes</h3>
      <textarea id="noteArea" placeholder="Notes for this slide&#8230;"></textarea>
      <span class="notes-saved" id="notesSaved">Saved</span>
    </div>

    <!-- Next slide preview -->
    <div class="next-sidebar" id="nextWrap">
      <span class="sidebar-label">Next</span>
      <div class="next-preview">
        <img id="imgNext" src="/slide/1" alt="Slide 2">
      </div>
    </div>

    <!-- Slide grid (1 column, scrollable) -->
    <div class="grid-section">
      <span class="sidebar-label">Slides</span>
      <div class="slide-grid" id="slideGrid"></div>
    </div>

  </div>
</div>
<script>
{js}
</script>
</body>
</html>
"""
