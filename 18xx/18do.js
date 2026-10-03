/**
 * The five market reset instructions from §6.5.2.8–9 of the 18DO rules.
 * All markup is maintained in this trusted local source; player input is never
 * interpolated into an HTML string.
 */
const marketSteps = [
  { title: 'Переставить пивоварни', text: 'Отсортируйте BEC каждой пивоварни от старшего к младшему. Сравните старший BEC: более высокий тип действует раньше. Если равны — сравните второй. Если и это не решило порядок, сохраните прежний взаимный порядок.', note: 'Сначала полностью закончите ходы всех пивоварен, затем меняйте Brewery Order.' },
  { title: 'Вернуть непроданный спрос', text: 'Все кубики, оставшиеся в жёлтых и оранжевых клетках спроса, верните в общий Stock. Непроданный спрос не переносится напрямую в следующий BR.', note: 'Жёлтые кубики тоже уходят в Stock: сохранится только объём, который действительно был продан.' },
  { title: 'Сделать покупателей постоянными', text: 'Переложите все кубики из белых клеток предложения в жёлтые клетки спроса того же сегмента. Каждый кубик, проданный в этом BR, становится постоянным спросом следующего BR — независимо от того, был покупатель новым или постоянным.', note: 'Цвет спроса прошлого раунда уже не важен; важен факт продажи.' },
  { title: 'Поставить No Demand', text: 'Найдите самый низкий сегмент, в жёлтом спросе которого есть кубики. У каждого более низкого сегмента с пустой жёлтой клеткой поставьте No Demand на его оранжевую клетку, если маркера там ещё нет.', note: 'Существующие маркеры No Demand этим шагом не снимаются.' },
  { title: 'Пополнить новых покупателей', text: 'Оранжевые клетки без No Demand заполните до напечатанного в них количества, начиная с самого высокого сегмента. Сначала берите кубики из Stock. При нехватке берите из спроса самого низкого доступного сегмента. Нельзя брать из жёлтого спроса того же сегмента, который сейчас пополняете.', note: 'Кубики из жёлтого спроса нижнего сегмента могут пополнить только более высокий сегмент.' }
];

const playerLimits = { '3': { certificates: '26', shares: '70%' }, '4': { certificates: '19', shares: '60%' }, '5': { certificates: '18', shares: '60%' } };
const phaseRank = { yellow: 0, green: 1, brown: 2, grey: 3 };
const storageKey = '18xx-18do-reference-v1';
const state = { tab: 'overview', marketStep: 0, variant: 'exp', players: '3', phase: 'yellow', checked: {} };

/**
 * Read the local browser snapshot for this reference sheet. It restores only
 * known settings and boolean checklist values; unavailable storage or malformed
 * data leaves the in-memory defaults intact.
 */
function restoreState() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (!saved || typeof saved !== 'object') return;
    if (['overview', 'stock', 'operating', 'market', 'expert'].includes(saved.tab)) state.tab = saved.tab;
    if (saved.variant === 'hsb' || saved.variant === 'exp') state.variant = saved.variant;
    if (playerLimits[saved.players]) state.players = saved.players;
    if (phaseRank[saved.phase] !== undefined) state.phase = saved.phase;
    if (Number.isInteger(saved.marketStep) && saved.marketStep >= 0 && saved.marketStep < marketSteps.length) state.marketStep = saved.marketStep;
    if (saved.checked && typeof saved.checked === 'object') {
      for (const checkbox of document.querySelectorAll('[data-check]')) {
        state.checked[checkbox.dataset.check] = saved.checked[checkbox.dataset.check] === true;
      }
    }
  } catch (_error) {
    // Private browsing and disabled local storage should not prevent reading rules.
  }
}

/**
 * Persist the current view and checklist for use at the next visit. Storage is
 * optional, so quota and privacy mode errors are intentionally ignored.
 */
function saveState() {
  try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_error) { /* Optional persistence. */ }
}

/**
 * Activate one of the document's existing tab panels and update ARIA selection.
 * The EXP tab is redirected to overview while the HSB variant is selected.
 * @param {string} name - A panel id from the fixed tab list.
 */
function showTab(name) {
  if (name === 'expert' && state.variant !== 'exp') name = 'overview';
  const panel = document.getElementById(name);
  if (!panel || !panel.classList.contains('panel')) return;
  state.tab = name;
  for (const item of document.querySelectorAll('.panel')) {
    const active = item.id === name;
    item.hidden = !active;
    item.classList.toggle('active', active);
  }
  for (const tab of document.querySelectorAll('.tab')) {
    const active = tab.dataset.tab === name;
    tab.classList.toggle('active', active);
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
  }
  saveState();
}

/**
 * Update the one displayed market instruction and its stepper navigation.
 * @param {number} index - Zero-based step index, clamped to the known range.
 */
function showMarketStep(index) {
  state.marketStep = Math.max(0, Math.min(marketSteps.length - 1, index));
  const step = marketSteps[state.marketStep];
  document.getElementById('market-detail').innerHTML = `<p class="eyebrow">Шаг ${state.marketStep + 1} / ${marketSteps.length}</p><h3>${step.title}</h3><p>${step.text}</p><p class="market-warning">${step.note}</p>`;
  document.getElementById('market-position').textContent = `Шаг ${state.marketStep + 1} из ${marketSteps.length}`;
  document.getElementById('market-prev').disabled = state.marketStep === 0;
  document.getElementById('market-next').disabled = state.marketStep === marketSteps.length - 1;
  for (const button of document.querySelectorAll('[data-market-step]')) {
    const active = Number(button.dataset.marketStep) === state.marketStep;
    button.classList.toggle('active', active);
    if (active) button.setAttribute('aria-current', 'step');
    else button.removeAttribute('aria-current');
  }
  saveState();
}

/**
 * Reflect the selected player count in the quick reference numbers.
 * @param {string} count - A supported count of three, four, or five players.
 */
function applyPlayerCount(count) {
  if (!playerLimits[count]) return;
  state.players = count;
  document.getElementById('certificate-limit').textContent = playerLimits[count].certificates;
  document.getElementById('share-limit').textContent = playerLimits[count].shares;
  document.getElementById('player-count').value = count;
  saveState();
}

/**
 * Hide expert-only rules for HSB without losing the selected player count or
 * checklist progress. Expert view is closed if it becomes unavailable.
 * @param {string} variant - Either `hsb` or `exp`.
 */
function applyVariant(variant) {
  if (variant !== 'hsb' && variant !== 'exp') return;
  state.variant = variant;
  document.getElementById('variant').value = variant;
  for (const node of document.querySelectorAll('[data-exp-only]')) {
    if (node.classList.contains('panel')) continue;
    node.hidden = variant !== 'exp';
  }
  if (state.tab === 'expert' && variant === 'hsb') showTab('overview');
  updateProgress();
  saveState();
}

/**
 * Mark SEM cards whose first usable phase has not started. The events remain
 * visible because the rules permit acquiring them before they can be used.
 * @param {string} phase - One of the four color phases in chronological order.
 */
function applyPhase(phase) {
  if (phaseRank[phase] === undefined) return;
  state.phase = phase;
  document.getElementById('phase').value = phase;
  for (const card of document.querySelectorAll('[data-event-phase]')) {
    const locked = phaseRank[card.dataset.eventPhase] > phaseRank[phase];
    card.classList.toggle('phase-locked', locked);
    card.title = locked ? 'Можно взять сейчас, применить с указанной фазы' : '';
  }
  saveState();
}

/**
 * Count the visible OR checklist items and show completion in text and a bar.
 * Hidden EXP steps are excluded from the current variant's denominator.
 */
function updateProgress() {
  let total = 0;
  let done = 0;
  for (const checkbox of document.querySelectorAll('[data-check]')) {
    const visible = !checkbox.closest('[data-exp-only]')?.hidden;
    checkbox.checked = state.checked[checkbox.dataset.check] === true;
    if (!visible) continue;
    total += 1;
    if (checkbox.checked) done += 1;
  }
  document.getElementById('progress-label').textContent = `${done} из ${total} шагов отмечено`;
  document.getElementById('progress-fill').style.width = `${total ? Math.round(done / total * 100) : 0}%`;
}

/**
 * Filter the static SEM reference cards by their first usable phase.
 * @param {string} phase - `all` or the phase value from the filter buttons.
 */
function filterEvents(phase) {
  for (const card of document.querySelectorAll('[data-event-phase]')) {
    card.hidden = phase !== 'all' && card.dataset.eventPhase !== phase;
  }
  for (const button of document.querySelectorAll('[data-filter]')) {
    const active = button.dataset.filter === phase;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  }
}

/**
 * Handle navigation and reset buttons through one delegated click listener.
 * @param {MouseEvent} event - Browser click event from the document.
 */
function handleClick(event) {
  const target = event.target instanceof Element ? event.target : null;
  if (!target) return;
  const tab = target.closest('[data-tab]');
  if (tab) { showTab(tab.dataset.tab); return; }
  const marketButton = target.closest('[data-market-step]');
  if (marketButton) { showMarketStep(Number(marketButton.dataset.marketStep)); return; }
  if (target.closest('#market-prev')) { showMarketStep(state.marketStep - 1); return; }
  if (target.closest('#market-next')) { showMarketStep(state.marketStep + 1); return; }
  if (target.closest('[data-go="market"]')) { showTab('market'); document.getElementById('market-title').scrollIntoView({ behavior: 'smooth' }); return; }
  const filter = target.closest('[data-filter]');
  if (filter) { filterEvents(filter.dataset.filter); return; }
  if (target.closest('#reset-progress')) {
    state.checked = {};
    updateProgress();
    saveState();
  }
}

/**
 * Handle the settings selectors and turn checklist, persisting only supported
 * values and known checkbox keys.
 * @param {Event} event - Browser change event from a form control.
 */
function handleChange(event) {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  if (target.id === 'player-count') applyPlayerCount(target.value);
  else if (target.id === 'variant') applyVariant(target.value);
  else if (target.id === 'phase') applyPhase(target.value);
  else if (target.matches('[data-check]')) {
    state.checked[target.dataset.check] = target.checked;
    updateProgress();
    saveState();
  }
}

/**
 * Move keyboard focus across the visible reference tabs with arrow, Home, and
 * End keys according to the tablist pattern. The hidden EXP tab is skipped.
 * @param {KeyboardEvent} event - Keydown event inside the tablist.
 */
function handleTabKeydown(event) {
  if (!(event.target instanceof Element) || !event.target.matches('[role="tab"]')) return;
  const tabs = [];
  for (const tab of document.querySelectorAll('[role="tab"]')) if (!tab.hidden) tabs.push(tab);
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

/** Initialize the static reference UI and restore the reader's saved settings. */
function initialize() {
  restoreState();
  applyPlayerCount(state.players);
  applyVariant(state.variant);
  applyPhase(state.phase);
  showTab(state.tab);
  showMarketStep(state.marketStep);
  filterEvents('all');
  updateProgress();
  document.addEventListener('click', handleClick);
  document.addEventListener('change', handleChange);
  document.querySelector('[role="tablist"]').addEventListener('keydown', handleTabKeydown);
}

initialize();
