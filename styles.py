"""Styling constants for the digital twin Gradio app."""

# One quiet accent family instead of three competing hues.
# Names kept for backward-compat if referenced elsewhere in the app.
GOLD = "#d6cca8"      # primary accent — amber
BLUE = "#6b7280"       # neutral slate, used sparingly (links, secondary states)
PURPLE = "#8a7ca8"     # muted plum, reserved — not used in the UI by default

EXAMPLES = [
    "Tell me about your work as a Senior Performance Tester in the banking sector.",
    "Tell me about yourself. What kind of person are you?",
    "What are your top skills?",
    "What kind of projects have you worked on",
    "How do you handle tight deadlines or high-pressure projects?",
    "Are you open to new opportunities or freelance collaborations?",
    "How can I get in touch with you?",
    "Do you enjoy growing professionally, and are you a fast learner who adapts quickly?",
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@400;500;600&display=swap');

:root {
  --twin-accent: #d6cca8;
  /* Very soft, highly transparent accent */
  --twin-accent-soft: rgba(214, 204, 168, 0.08);
  --twin-accent-soft-strong: rgba(214, 204, 168, 0.12);

  --twin-bg: #0d0e11;
  --twin-surface: #15161a;
  --twin-surface-2: #1a1b20;
  --twin-border: #232429;
  --twin-border-strong: #313239;
  --twin-text: #e9e8e4;
  --twin-muted: #85858d;

  --twin-radius: 20px;
  --twin-radius-sm: 12px;
}

/* Light mode */
body:not(.dark) {
  --twin-bg: #f7f6f2;
  --twin-surface: #ffffff;
  --twin-surface-2: #f1f0eb;
  --twin-border: #e2e0d8;
  --twin-border-strong: #cbc8bc;
  --twin-text: #17171a;
  --twin-muted: #77767a;
  --twin-accent-soft: rgba(214, 204, 168, 0.06);
  --twin-accent-soft-strong: rgba(214, 204, 168, 0.10);
}

footer, .built-with, .show-api, .api-docs { display: none !important; }

html, body, gradio-app { background: var(--twin-bg) !important; }

/* ---------- Layout ---------- */
.gradio-container {
  background: var(--twin-bg) !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  width: 100% !important;
  max-width: 720px !important;
  min-width: 0 !important;
  margin: 0 auto !important;
  padding: 56px 24px 48px !important;
}
.gradio-container .main, .gradio-container .contain, .gradio-container .wrap {
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
}
.gradio-container * { min-width: 0; }

/* ---------- Title ---------- */
.gradio-container h1 {
  position: relative;
  color: var(--twin-text) !important;
  font-family: 'Fraunces', Georgia, serif !important;
  font-size: 27px !important;
  font-weight: 500 !important;
  font-style: normal;
  letter-spacing: -0.01em !important;
  border-left: 0 !important;
  padding-left: 0 !important;
  padding-bottom: 16px !important;
  margin: 0 0 22px !important;
  text-align: left !important;
}

.gradio-container h1::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 1px;
  background: var(--twin-border-strong);
  overflow: hidden;
}
.gradio-container h1::before {
  content: "";
  position: absolute;
  left: 0;
  bottom: 0;
  width: 64px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--twin-accent) 50%, transparent);
  animation: twin-trace 5.5s ease-in-out infinite;
  z-index: 1;
}
@keyframes twin-trace {
  0%   { transform: translateX(-20px); opacity: 0; }
  15%  { opacity: 1; }
  85%  { opacity: 1; }
  100% { transform: translateX(600px); opacity: 0; }
}
@media (prefers-reduced-motion: reduce) {
  .gradio-container h1::before { animation: none; opacity: 0; }
}

/* ---------- Block surfaces ---------- */
.block, .form { background: transparent !important; box-shadow: none !important; }

/* ---------- Hide Chatbot label ---------- */
.chatbot > .block-label,
.chatbot > label,
.chatbot .label-wrap,
.chatbot .block-label,
.chatbot > .label-container {
  display: none !important;
}

/* ---------- Chatbot frame ---------- */
.chatbot, .chatbot.block {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 12px !important;
  min-height: 440px !important;
  box-shadow: none !important;
}
.chatbot .placeholder, .chatbot .placeholder * { color: var(--twin-muted) !important; }

/* ---------- Message rows ---------- */
.message-row,
.message-row > div,
.message-row .role,
.message-wrap, .bubble-wrap {
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
}

/* ---------- Bubble reset ---------- */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble,
.message-row .prose {
  border: 0 !important;
  box-shadow: none !important;
}

/* ---------- User bubble: transparent cloud style ---------- */
.message-row.user-row .message,
.message-row.user-row .message-bubble,
.message-row.user-row .bubble,
.message-row[data-role="user"] .message,
.message-row[data-role="user"] .message-bubble {
  background: rgba(214, 204, 168, 0.07) !important;  /* Light, very transparent background */
  border: 1px solid rgba(214, 204, 168, 0.15) !important; /* Thin, almost invisible border */
  border-radius: 24px !important;                     /* Fully rounded, cloud-like corners */
  color: var(--twin-text) !important;
  width: 100% !important;                             /* Keeps the elongated shape */
  padding: 12px 22px !important;                      /* Soft padding */
  backdrop-filter: blur(8px);                         /* Frosted-glass effect, iOS style */
  -webkit-backdrop-filter: blur(8px);
}

/* Remove any inner box */
.message-row.user-row .message *,
.message-row.user-row .message-bubble *,
.message-row.user-row .bubble *,
.message-row.user-row .prose * {
  background: transparent !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  margin: 0 !important;
}

/* ---------- Assistant bubble ---------- */
.message-row.bot-row .message,
.message-row.bot-row .message-bubble,
.message-row.bot-row .bubble,
.message-row[data-role="assistant"] .message,
.message-row[data-role="assistant"] .message-bubble {
  background: var(--twin-surface-2) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 18px !important;
  color: var(--twin-text) !important;
  padding: 12px 18px !important;
}

/* ---------- Typography ---------- */
.message-row .message,
.message-row .message-bubble,
.message-row .bubble {
  font-size: 14.5px !important;
  line-height: 1.6 !important;
}
.message-row .message p,
.message-row .message-bubble p,
.message-row .bubble p,
.message-row .prose p {
  font-size: 14.5px !important;
  line-height: 1.6 !important;
  margin: 0 0 8px !important;
  color: inherit !important;
}
.message-row .message p:last-child,
.message-row .message-bubble p:last-child,
.message-row .bubble p:last-child,
.message-row .prose p:last-child { margin-bottom: 0 !important; }

.message-row.bot-row .message *,
.message-row.bot-row .message-bubble *,
.message-row.bot-row .bubble * {
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  color: inherit !important;
}
.message-row .message a,
.message-row .message-bubble a {
  color: var(--twin-accent) !important;
  text-decoration: underline;
  text-underline-offset: 2px;
}

/* ---------- Input row ---------- */
.input-row,
.gr-input-row,
.chat-input-row,
form[class*="input"] { align-items: stretch !important; gap: 8px !important; }

textarea, input[type="text"] {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 12px !important;
  color: var(--twin-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 14.5px !important;
  padding: 12px 16px !important;
  line-height: 1.4 !important;
  min-height: 48px !important;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
textarea:focus, input[type="text"]:focus {
  border-color: var(--twin-accent) !important;
  outline: none !important;
  box-shadow: 0 0 0 3px var(--twin-accent-soft) !important;
}
textarea::placeholder, input::placeholder { color: var(--twin-muted) !important; }

/* ---------- Buttons ---------- */
button {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 12px !important;
  background: var(--twin-surface) !important;
  color: var(--twin-text) !important;
  padding: 0 16px !important;
  min-height: 48px !important;
  align-self: stretch !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}
button:hover { border-color: var(--twin-border-strong) !important; }

button.primary,
button[variant="primary"],
button.submit,
button.submit-button,
.submit-button,
button.lg.primary {
  background: var(--twin-accent) !important;
  border: 1px solid var(--twin-accent) !important;
  border-radius: 12px !important;
  color: #1c1a12 !important;
  min-height: 48px !important;
  align-self: stretch !important;
  padding: 0 14px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
button.primary:hover,
button.submit:hover,
.submit-button:hover,
button.lg.primary:hover {
  background: #e3dabb !important;
  border-color: #e3dabb !important;
  color: #1c1a12 !important;
}

button.submit svg,
button.submit-button svg,
.submit-button svg,
button.primary svg,
button[variant="primary"] svg {
  width: 17px !important;
  height: 17px !important;
  margin: 0 auto !important;
  display: block !important;
  align-self: center !important;
  color: #1c1a12 !important;
  fill: currentColor !important;
  stroke: currentColor !important;
}

/* ---------- Examples ---------- */
.examples, .examples-holder, [data-testid="examples"] {
  background: transparent !important;
  padding: 0 !important;
  margin-top: 16px !important;
}
.examples table, .examples-table { background: transparent !important; border: 0 !important; border-spacing: 8px !important; }
.examples button, .example, .examples td button, [data-testid="examples"] button {
  background: var(--twin-surface) !important;
  border: 1px solid var(--twin-border) !important;
  border-radius: 12px !important;
  color: var(--twin-muted) !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  padding: 10px 14px !important;
  text-align: left !important;
  min-height: 0 !important;
  align-self: auto !important;
  display: inline-block !important;
  transition: border-color 0.15s ease, color 0.15s ease;
}
.examples button:hover, .example:hover, [data-testid="examples"] button:hover {
  border-color: var(--twin-accent) !important;
  color: var(--twin-text) !important;
  background: var(--twin-surface) !important;
}

/* ---------- Icon buttons ---------- */
.icon-button, .chatbot .icon-button {
  color: var(--twin-muted) !important;
  background: transparent !important;
  border: 0 !important;
  min-height: 0 !important;
  align-self: auto !important;
  padding: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
}
.icon-button:hover, .chatbot .icon-button:hover { color: var(--twin-accent) !important; }

/* ---------- Scrollbar & Selection ---------- */
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: var(--twin-bg); }
::-webkit-scrollbar-thumb { background: var(--twin-border-strong); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--twin-accent); }
::selection { background: var(--twin-accent-soft-strong); color: var(--twin-text); }

/* ---------- Mobile ---------- */
@media (max-width: 640px) {
  .gradio-container { padding: 36px 14px 36px !important; }
  .gradio-container h1 { font-size: 22px !important; }
}
"""

JS = """
() => {
  document.title = 'Digital Twin';

  const focusInput = () => {
    const areas = document.querySelectorAll('textarea');
    if (areas.length) areas[areas.length - 1].focus();
  };
  setTimeout(focusInput, 300);

  const watchTextarea = (area) => {
    if (area.dataset.twinWatched) return;
    area.dataset.twinWatched = '1';
    let wasDisabled = area.disabled || area.readOnly;
    new MutationObserver(() => {
      const isDisabled = area.disabled || area.readOnly;
      if (wasDisabled && !isDisabled) area.focus();
      wasDisabled = isDisabled;
    }).observe(area, { attributes: true, attributeFilter: ['disabled', 'readonly'] });
  };

  const scan = () => document.querySelectorAll('textarea').forEach(watchTextarea);
  setTimeout(scan, 500);
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
}
"""