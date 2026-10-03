/** Starting cash and certificate limit from §2.4.4 and §6.5.2. */
const playerRules = {
  '2': { cash: '£1 200', limit: '25' }, '3': { cash: '£800', limit: '18' },
  '4': { cash: '£600', limit: '13' }, '5': { cash: '£480', limit: '11' },
  '6': { cash: '£400', limit: '10' }, '7': { cash: '£345', limit: '9' },
  '8': { cash: '£300', limit: '8' }
};

/** Phase effects in the standard three-permit game; OR counts take effect after the next SR. */
const phaseRules = {
  A: { ors: '1 OR после SR', detail: 'Старт: жёлтые тайлы; до 3 поездов каждого типа. Поезда A стоят £100.' },
  B: { ors: '2 OR после следующего SR', detail: 'Появляются зелёные тайлы и поезда B за £200. Текущий набор OR не удлиняется посреди игры.' },
  C: { ors: '2 OR после SR', detail: 'Поезда A без warranty ржавеют; оффборды переходят на среднее значение. Поезда C стоят £280.' },
  D: { ors: '3 OR после следующего SR', detail: 'Доступны russet тайлы и поезда D за £360. Текущий набор OR сохраняет прежнюю длину.' },
  E: { ors: '3 OR после SR', detail: 'Поезда B без warranty ржавеют; максимум 2 поезда каждого типа. Оффборды дают высшее значение. Поезда E стоят £500.' },
  F: { ors: '3 OR после SR', detail: 'Поезда C без warranty ржавеют; поезда F стоят £600.' },
  G: { ors: '3 OR после SR', detail: 'Поезда D без warranty ржавеют; теперь максимум 3 поезда суммарно. Поезда G стоят £700.' },
  H: { ors: '3 OR после SR', detail: 'Поезда H за £800 доступны без ограничения. Первый купленный H запускает подготовку финала через LNER.' }
};

const storageKey = '18xx-1862-reference-v1';
const state = { tab: 'overview', players: '4', phase: 'A', checked: {} };

/**
 * Restore only recognized values from this browser's local storage. Broken or
 * disabled storage leaves the built-in defaults available for offline reading.
 */
function restoreState() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (!saved || typeof saved !== 'object') return;
    if (['overview', 'parliament', 'stock', 'operating', 'trains', 'end'].includes(saved.tab)) state.tab = saved.tab;
    if (playerRules[saved.players]) state.players = saved.players;
    if (phaseRules[saved.phase]) state.phase = saved.phase;
    if (saved.checked && typeof saved.checked === 'object') {
      for (const input of document.querySelectorAll('[data-check]')) {
        state.checked[input.dataset.check] = saved.checked[input.dataset.check] === true;
      }
    }
  } catch (_error) {
    // The reference remains usable when browser persistence is unavailable.
  }
}

/** Save the current reading position and OR checklist without interrupting private mode. */
function saveState() {
  try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_error) { /* Optional persistence. */ }
}

/**
 * Select a static tab panel and keep focus semantics in sync with the visible
 * content. Unknown panel identifiers are ignored.
 * @param {string} name - One of the fixed panel ids in the document.
 */
function showTab(name) {
  const panel = document.getElementById(name);
  if (!panel || !panel.classList.contains('panel')) return;
  state.tab = name;
  for (const item of document.querySelectorAll('.panel')) {
    const active = item.id === name;
    item.hidden = !active;
    item.classList.toggle('active', active);
  }
  for (const tab of document.querySelectorAll('[role="tab"]')) {
    const active = tab.dataset.tab === name;
    tab.classList.toggle('active', active);
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
  }
  saveState();
}

/**
 * Display starting cash and the initial certificate limit for a supported
 * player count; the later LNER recalculation remains described in the SR tab.
 * @param {string} count - Player count from the settings selector.
 */
function applyPlayers(count) {
  if (!playerRules[count]) return;
  state.players = count;
  document.getElementById('player-count').value = count;
  document.getElementById('starting-cash').textContent = playerRules[count].cash;
  document.getElementById('certificate-limit').textContent = playerRules[count].limit;
  saveState();
}

/**
 * Show the major rule changes for a chosen train phase in the quick phase card.
 * @param {string} phase - A through H, matching the official train bands.
 */
function applyPhase(phase) {
  if (!phaseRules[phase]) return;
  state.phase = phase;
  document.getElementById('phase').value = phase;
  document.getElementById('phase-name').textContent = phase;
  document.getElementById('phase-ors').textContent = phaseRules[phase].ors;
  document.getElementById('phase-detail').textContent = phaseRules[phase].detail;
  saveState();
}

/** Count checked OR actions and update the accessible progress text and bar. */
function updateProgress() {
  let done = 0;
  let total = 0;
  for (const input of document.querySelectorAll('[data-check]')) {
    input.checked = state.checked[input.dataset.check] === true;
    total += 1;
    if (input.checked) done += 1;
  }
  document.getElementById('progress-label').textContent = `${done} из ${total} шагов отмечено`;
  document.getElementById('progress-fill').style.width = `${Math.round(done / total * 100)}%`;
}

/**
 * Handle tabs and the reset action through a single delegated listener.
 * @param {MouseEvent} event - Click event originating in the document.
 */
function handleClick(event) {
  const target = event.target instanceof Element ? event.target : null;
  if (!target) return;
  const tab = target.closest('[data-tab]');
  if (tab) { showTab(tab.dataset.tab); return; }
  if (target.closest('#reset-progress')) {
    state.checked = {};
    updateProgress();
    saveState();
  }
}

/**
 * Handle selectors and known checklist boxes without interpreting user text.
 * @param {Event} event - Change event from a browser form control.
 */
function handleChange(event) {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  if (target.id === 'player-count') applyPlayers(target.value);
  else if (target.id === 'phase') applyPhase(target.value);
  else if (target.matches('[data-check]')) {
    state.checked[target.dataset.check] = target.checked;
    updateProgress();
    saveState();
  }
}

/**
 * Support the arrow-key, Home, and End navigation expected of an ARIA tablist.
 * @param {KeyboardEvent} event - Keydown event inside the section tablist.
 */
function handleTabKeys(event) {
  if (!(event.target instanceof Element) || !event.target.matches('[role="tab"]')) return;
  const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
  const index = tabs.indexOf(event.target);
  if (index < 0) return;
  let next = index;
  if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
  else if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
  else if (event.key === 'Home') next = 0;
  else if (event.key === 'End') next = tabs.length - 1;
  else return;
  event.preventDefault();
  showTab(tabs[next].dataset.tab);
  tabs[next].focus();
}

/** Initialize the reference after the deferred script is loaded by the browser. */
function initialize() {
  restoreState();
  applyPlayers(state.players);
  applyPhase(state.phase);
  showTab(state.tab);
  updateProgress();
  document.addEventListener('click', handleClick);
  document.addEventListener('change', handleChange);
  document.querySelector('[role="tablist"]').addEventListener('keydown', handleTabKeys);
}

initialize();
