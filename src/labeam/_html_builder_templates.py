# ruff: noqa: E501
"""HTML/CSS/JS templates for the audience and presenter views.

Kept in a dedicated module so that the embedded multi-line strings
(HTML, CSS, JavaScript) are exempt from the line-length rule (E501)
without suppressing it project-wide.
"""

from __future__ import annotations

_CSS = """\
/* ============================================================
   LABEAM PRESENTATION — CSS
   ============================================================ */

:root {
  --si-color-petrol: #009999;
  --si-color-light-petrol: #00C1B6;
  --si-color-bold-green: #00FFB9;
  --si-color-deep-blue: #000028;
  --si-color-bright-sand: #DFDFD9;
  --si-color-deep-blue-80: #333353;
  --si-color-deep-blue-70: #4C4C68;
  --si-color-deep-blue-60-dark-gray: #66667E;
  --si-color-deep-blue-40: #9999A9;
  --si-color-deep-blue-20-soft-gray: #CCCCD4;
  --si-color-deep-blue-10: #E5E5E9;
  --si-color-deep-blue-8: #EBEBEE;
}

:root,
[data-theme="light"] {
  --si-bg-primary: #FFFFFF;
  --si-bg-slide: #FFFFFF;
  --si-text-primary: var(--si-color-deep-blue);
  --si-text-secondary: var(--si-color-deep-blue-70);
  --si-text-muted: var(--si-color-deep-blue-60-dark-gray);
  --si-accent: var(--si-color-petrol);
  --si-accent-light: var(--si-color-light-petrol);
  --si-border: var(--si-color-deep-blue-20-soft-gray);
  --si-shadow: rgba(0,0,40,0.08);
  --si-toc-bg: rgba(255,255,255,0.97);
  --si-progress-bg: #E0E0DE;
  --si-slide-filter: none;
}

[data-theme="dark"] {
  --si-bg-primary: var(--si-color-deep-blue);
  --si-bg-slide: var(--si-color-deep-blue);
  --si-text-primary: var(--si-color-deep-blue-8);
  --si-text-secondary: var(--si-color-deep-blue-40);
  --si-text-muted: var(--si-color-deep-blue-40);
  --si-accent: var(--si-color-light-petrol);
  --si-accent-light: var(--si-color-light-petrol);
  --si-border: var(--si-color-deep-blue-80);
  --si-shadow: rgba(0,0,0,0.3);
  --si-toc-bg: rgba(0,0,40,0.97);
  --si-progress-bg: #23233C;
  --si-slide-filter: invert(1) hue-rotate(180deg);
}

*,
*::before,
*::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  height: 100%;
  overflow: hidden;
  font-family: Arial, 'Segoe UI', system-ui, -apple-system, Helvetica, sans-serif;
  background: var(--si-bg-slide);
  color: var(--si-text-primary);
  transition: background 0.3s, color 0.3s;
}

body.laser-pointer-active,
body.laser-pointer-active * { cursor: none !important; }

.presentation {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* Fixed 1920x1080 canvas — scaled to viewport by JS */
.slide {
  position: absolute;
  top: 0; left: 0;
  width: 1920px;
  height: 1080px;
  transform-origin: top left;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.4s ease, visibility 0.4s;
}

.slide.active {
  opacity: 1;
  visibility: visible;
  z-index: 1;
}

/* SVG image fills the entire slide canvas */
.slide-svg {
  width: 1920px;
  height: 1080px;
  object-fit: contain;
  display: block;
  filter: var(--si-slide-filter);
  transition: filter 0.3s;
}

/* ---- Progress bar ---- */
.progress-track {
  position: fixed;
  bottom: 0; left: 0;
  width: 100%;
  height: 3px;
  background: var(--si-progress-bg);
  z-index: 99;
}

.progress-bar {
  position: fixed;
  bottom: 0; left: 0;
  height: 3px;
  background: var(--si-accent);
  transition: width 0.4s ease;
  z-index: 100;
}

/* ---- Controls ---- */
.ctrl-btn {
  background: rgba(128,128,128,0.12);
  border: 1px solid rgba(128,128,128,0.18);
  color: rgba(128,128,128,0.6);
  width: 34px;
  height: 34px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
  backdrop-filter: blur(4px);
}

.ctrl-btn:hover {
  background: rgba(128,128,128,0.28);
  color: rgba(255,255,255,0.9);
  border-color: rgba(128,128,128,0.35);
}

.ctrl-btn.active {
  background: rgba(255,0,0,0.2);
  color: rgba(255,120,120,0.95);
  border-color: rgba(255,90,90,0.5);
}

.controls-left {
  position: fixed;
  top: 14px; left: 16px;
  display: flex;
  gap: 6px;
  z-index: 50;
}

.controls-right {
  position: fixed;
  top: 14px; right: 16px;
  display: flex;
  gap: 6px;
  align-items: center;
  z-index: 50;
}

.slide-counter {
  font-size: 12px;
  color: rgba(128,128,128,0.5);
  min-width: 44px;
  text-align: center;
  font-variant-numeric: tabular-nums;
  letter-spacing: 0.03em;
}

/* ---- TOC overlay ---- */
.toc-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0,0,40,0.5);
  z-index: 200;
  display: none;
  justify-content: center;
  align-items: center;
}

.toc-overlay.open { display: flex; }

.toc-panel {
  background: var(--si-toc-bg);
  border-radius: 16px;
  padding: 40px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 16px 48px var(--si-shadow);
}

.toc-panel h2 {
  font-size: 1.5rem;
  margin-bottom: 24px;
  color: var(--si-text-primary);
  border-bottom: 2px solid var(--si-accent);
  padding-bottom: 12px;
}

.toc-panel ul { list-style: none; padding: 0; }

.toc-panel li {
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  color: var(--si-text-secondary);
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 12px;
}

.toc-panel li:hover {
  background: rgba(128,128,128,0.1);
  color: var(--si-accent);
}

.toc-panel li .toc-num {
  color: var(--si-accent);
  font-weight: 600;
  min-width: 28px;
}

/* ---- Keyboard hint ---- */
.keyboard-hint {
  position: fixed;
  bottom: 60px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(30,30,50,0.85);
  border: 1px solid rgba(128,128,128,0.2);
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 13px;
  color: rgba(220,220,220,0.85);
  z-index: 50;
  opacity: 0;
  transition: opacity 0.5s;
  pointer-events: none;
  white-space: nowrap;
}

.keyboard-hint.show { opacity: 1; }

kbd {
  background: rgba(60,60,80,0.9);
  padding: 2px 7px;
  border-radius: 4px;
  border: 1px solid rgba(128,128,128,0.3);
  font-family: inherit;
  font-size: 12px;
  color: #ddd;
}

/* ---- Laser pointer ---- */
.laser-pointer {
  position: fixed;
  top: 50%; left: 50%;
  width: 26px; height: 26px;
  border-radius: 50%;
  pointer-events: none;
  z-index: 260;
  opacity: 0;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(255,110,110,1) 0%,
    rgba(255,40,40,0.95) 26%,
    rgba(255,0,0,0.65) 44%,
    rgba(255,0,0,0.12) 68%,
    rgba(255,0,0,0) 100%
  );
  box-shadow: 0 0 0 2px rgba(255,60,60,0.24), 0 0 22px rgba(255,0,0,0.65);
  transition: opacity 0.15s ease;
}

body.laser-pointer-active .laser-pointer { opacity: 1; }

@media print {
  .slide {
    page-break-after: always;
    position: relative;
    opacity: 1;
    visibility: visible;
  }
  .controls-left, .controls-right, .toc-overlay,
  .progress-bar, .progress-track, .keyboard-hint, .laser-pointer {
    display: none !important;
  }
}
"""

_JS = """\
(function () {
  // ---- Meta fill ----
  var cfg = window.PRESENTATION_CONFIG || {};
  function fill(sel, val) {
    document.querySelectorAll(sel).forEach(function(el) { el.textContent = val || ''; });
  }
  fill('.meta-title',          cfg.title);
  fill('.meta-classification', cfg.classification);
  fill('.meta-year',           cfg.year);
  fill('.meta-author',         cfg.author);
  fill('.meta-department',     cfg.department);
  fill('.meta-date',           cfg.date);
})();

(function () {
  // ---- Responsive scaling ----
  var SLIDE_W = 1920, SLIDE_H = 1080;
  function scaleSlides() {
    var scaleX = window.innerWidth  / SLIDE_W;
    var scaleY = window.innerHeight / SLIDE_H;
    var scale  = Math.min(scaleX, scaleY);
    var offX   = (window.innerWidth  - SLIDE_W * scale) / 2;
    var offY   = (window.innerHeight - SLIDE_H * scale) / 2;
    document.querySelectorAll('.slide').forEach(function(s) {
      s.style.transform = 'translate(' + offX + 'px,' + offY + 'px) scale(' + scale + ')';
    });
  }
  window.addEventListener('resize', scaleSlides);
  scaleSlides();
})();

(function () {
  var slides  = document.querySelectorAll('.slide');
  var total   = slides.length;
  var current = 0;

  // ---- Navigation (no loop) ----
  function showSlide(index) {
    if (index < 0 || index >= total) return;
    slides[current].classList.remove('active');
    current = index;
    slides[current].classList.add('active');
    updateUI();
    if (!window._remoteNav && window._wsAudienceSend) {
      window._wsAudienceSend({ type: 'goto', index: current });
    }
  }

  function nextSlide() { showSlide(current + 1); }
  function prevSlide() { showSlide(current - 1); }

  function updateUI() {
    document.getElementById('slideCounter').textContent = (current + 1) + ' / ' + total;
    document.getElementById('progressBar').style.width = ((current + 1) / total * 100) + '%';
  }

  // ---- Laser pointer ----
  var laserPointer = document.getElementById('laserPointer');
  var laserBtn     = document.getElementById('laserBtn');

  document.addEventListener('mousemove', function(e) {
    if (!document.body.classList.contains('laser-pointer-active')) return;
    laserPointer.style.left = e.clientX + 'px';
    laserPointer.style.top  = e.clientY + 'px';
  }, { passive: true });

  window.toggleLaserPointer = function(forceOff) {
    var enable = forceOff ? false : !document.body.classList.contains('laser-pointer-active');
    document.body.classList.toggle('laser-pointer-active', enable);
    laserBtn.classList.toggle('active', enable);
    laserBtn.setAttribute('aria-pressed', String(enable));
  };

  // ---- Theme toggle ----
  window.toggleTheme = function() {
    var html  = document.documentElement;
    var isDark = html.getAttribute('data-theme') === 'dark';
    html.setAttribute('data-theme', isDark ? 'light' : 'dark');
    document.getElementById('themeBtn').textContent = isDark ? '\\u263E' : '\\u2600';
    if (window._wsAudienceSend) {
      window._wsAudienceSend({ type: 'darkmode', dark: !isDark });
    }
  };

  // ---- TOC ----
  function buildTOC() {
    var list = document.getElementById('tocList');
    var tocData = window.PRESENTATION_TOC || [];
    slides.forEach(function(slide, i) {
      var title = 'Slide ' + (i + 1);
      for (var j = 0; j < tocData.length; j++) {
        if (tocData[j][0] === i) { title = tocData[j][1]; break; }
      }
      var li = document.createElement('li');
      li.innerHTML = '<span class="toc-num">' + (i + 1) + '</span>' + title;
      li.onclick = (function(idx) { return function() { showSlide(idx); closeTOC(); }; })(i);
      list.appendChild(li);
    });
  }

  window.toggleTOC = function() {
    document.getElementById('tocOverlay').classList.toggle('open');
  };
  window.closeTOC = function() {
    document.getElementById('tocOverlay').classList.remove('open');
  };
  window.closeTOCOnBackdrop = function(e) {
    if (e.target === document.getElementById('tocOverlay')) closeTOC();
  };

  // ---- Keyboard shortcuts ----
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === ' ')  { e.preventDefault(); nextSlide(); }
    else if (e.key === 'ArrowLeft')               { e.preventDefault(); prevSlide(); }
    else if (e.key === 'ArrowUp')               { e.preventDefault(); nextSlide(); }
    else if (e.key === 'ArrowDown')               { e.preventDefault(); prevSlide(); }
    else if (e.key === 'PageUp')               { e.preventDefault(); nextSlide(); }
    else if (e.key === 'PageDown')               { e.preventDefault(); prevSlide(); }
    else if (e.key === 'Home')                    { e.preventDefault(); showSlide(0); }
    else if (e.key === 'End')                     { e.preventDefault(); showSlide(total - 1); }
    else if (e.key === 'b' || e.key === 'B')      { toggleLaserPointer(); }
    else if (e.key === 't' || e.key === 'T')      { toggleTOC(); }
    else if (e.key === 'd' || e.key === 'D')      { toggleTheme(); }
    else if (e.key === 'l' || e.key === 'L')      { toggleLaserPointer(); }
    else if (e.key === 'Escape') {
      closeTOC();
      if (document.body.classList.contains('laser-pointer-active')) toggleLaserPointer(true);
    }
  });

  // ---- Touch / swipe ----
  var touchStartX = 0;
  document.addEventListener('touchstart', function(e) {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });
  document.addEventListener('touchend', function(e) {
    var diff = e.changedTouches[0].screenX - touchStartX;
    if (Math.abs(diff) > 50) { diff < 0 ? nextSlide() : prevSlide(); }
  }, { passive: true });

  // ---- Expose for button onclick and WS audience sync ----
  window.nextSlide = nextSlide;
  window.prevSlide = prevSlide;
  window.showSlide = showSlide;

  // ---- Init ----
  updateUI();
  buildTOC();

  var hint = document.getElementById('keyHint');
  setTimeout(function() { hint.classList.add('show'); },    500);
  setTimeout(function() { hint.classList.remove('show'); }, 4500);
})();
"""

_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_escaped}</title>
  <script>
    window.PRESENTATION_CONFIG = {{
      title:          {title_js},
      classification: {classification_js},
      year:           {year_js},
      author:         {author_js},
      department:     {department_js},
      date:           {date_js}
    }};
    window.PRESENTATION_TOC = {toc_js};
  </script>
  <style>
{css}
  </style>
</head>
<body>

  <!-- Laser pointer -->
  <div class="laser-pointer" id="laserPointer"></div>

  <!-- Top-left controls: TOC, Prev, Next -->
  <div class="controls-left">
    <button class="ctrl-btn" onclick="toggleTOC()" title="Table of contents (T)" aria-label="Table of contents">&#8801;</button>
    <button class="ctrl-btn" onclick="prevSlide()" title="Previous slide (&#8592;)" aria-label="Previous slide">&#8592;</button>
    <button class="ctrl-btn" onclick="nextSlide()" title="Next slide (&#8594; / Space)" aria-label="Next slide">&#8594;</button>
  </div>

  <!-- Top-right controls: counter, laser, theme -->
  <div class="controls-right">
    <span class="slide-counter" id="slideCounter">1 / 1</span>
    <button class="ctrl-btn" id="laserBtn" onclick="toggleLaserPointer()" title="Laser pointer (L)" aria-label="Laser pointer" aria-pressed="false">&#11044;</button>
    <button class="ctrl-btn" id="themeBtn" onclick="toggleTheme()" title="Toggle dark / light mode (D)" aria-label="Toggle theme">&#9790;</button>
  </div>

  <!-- Progress -->
  <div class="progress-track"></div>
  <div class="progress-bar" id="progressBar" style="width:0"></div>

  <!-- TOC overlay -->
  <div class="toc-overlay" id="tocOverlay" onclick="closeTOCOnBackdrop(event)">
    <div class="toc-panel">
      <h2>Contents</h2>
      <ul id="tocList"></ul>
    </div>
  </div>

  <!-- Slides -->
  <div class="presentation" id="presentation">
{slides_html}
  </div>

  <!-- Keyboard hint -->
  <div class="keyboard-hint" id="keyHint">
    <kbd>&#8592;</kbd><kbd>&#8594;</kbd> navigate &nbsp;|&nbsp;
    <kbd>T</kbd> contents &nbsp;|&nbsp;
    <kbd>L</kbd> laser &nbsp;|&nbsp;
    <kbd>D</kbd> dark mode
  </div>

  <script>
{js}
  </script>
</body>
</html>
"""

_WS_AUDIENCE_JS = """\
(function() {
  var WS_PORT = WS_PORT_PLACEHOLDER;
  var SLIDE_W = 1920, SLIDE_H = 1080;
  var ws, reconnectTimer;
  window._remoteNav = false;

  function send(obj) {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(obj));
    }
  }
  window._wsAudienceSend = send;

  function connect() {
    ws = new WebSocket('ws://localhost:' + WS_PORT);
    ws.onmessage = function(e) {
      var msg = JSON.parse(e.data);
      if (msg.type === 'state' && window.showSlide) {
        window._remoteNav = true;
        window.showSlide(msg.index);
        window._remoteNav = false;
      } else if (msg.type === 'laser') {
        _handleWsLaser(msg);
      } else if (msg.type === 'darkmode') {
        _handleWsDarkMode(msg.dark);
      }
    };
    ws.onclose = function() {
      clearTimeout(reconnectTimer);
      reconnectTimer = setTimeout(connect, 2000);
    };
  }

  function _handleWsLaser(msg) {
    var laser = document.getElementById('laserPointer');
    if (!laser) return;
    if (msg.active) {
      var scale = Math.min(window.innerWidth / SLIDE_W, window.innerHeight / SLIDE_H);
      var offX = (window.innerWidth  - SLIDE_W * scale) / 2;
      var offY = (window.innerHeight - SLIDE_H * scale) / 2;
      laser.style.left    = (offX + msg.x * SLIDE_W * scale) + 'px';
      laser.style.top     = (offY + msg.y * SLIDE_H * scale) + 'px';
      laser.style.opacity = '1';
    } else {
      laser.style.opacity = '0';
    }
  }

  function _handleWsDarkMode(dark) {
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    var btn = document.getElementById('themeBtn');
    if (btn) btn.textContent = dark ? '\\u2600' : '\\u263E';
  }

  // Laser sending from audience (normalised to 1920x1080 canvas)
  document.addEventListener('mousemove', function(e) {
    if (!document.body.classList.contains('laser-pointer-active')) return;
    var scale = Math.min(window.innerWidth / SLIDE_W, window.innerHeight / SLIDE_H);
    var offX  = (window.innerWidth  - SLIDE_W * scale) / 2;
    var offY  = (window.innerHeight - SLIDE_H * scale) / 2;
    var x = (e.clientX - offX) / (SLIDE_W * scale);
    var y = (e.clientY - offY) / (SLIDE_H * scale);
    send({ type: 'laser', active: true,
           x: Math.max(0, Math.min(1, x)),
           y: Math.max(0, Math.min(1, y)) });
  }, { passive: true });

  // Wrap toggleLaserPointer to send 'laser off' when deactivated
  if (window.toggleLaserPointer) {
    var _origToggle = window.toggleLaserPointer;
    window.toggleLaserPointer = function(forceOff) {
      _origToggle(forceOff);
      if (forceOff || !document.body.classList.contains('laser-pointer-active')) {
        send({ type: 'laser', active: false, x: 0, y: 0 });
      }
    };
  }

  connect();
})();
"""
