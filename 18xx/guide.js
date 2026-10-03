/* Shared interactive reference for the compact 18xx guides. */
(function () {
  'use strict';

  const SECTION_DEFS = [
    { id: 'overview', label: 'Обзор', eyebrow: 'Перед партией', heading: 'Обзор игры' },
    { id: 'stock', label: 'Stock Round', eyebrow: 'Акции и рынок', heading: 'Stock Round' },
    { id: 'operating', label: 'Operating Round', eyebrow: 'Ход компании', heading: 'Operating Round' },
    { id: 'trains', label: 'Поезда и фазы', eyebrow: 'Развитие игры', heading: 'Поезда и фазы' },
    { id: 'end', label: 'Конец игры', eyebrow: 'Финал', heading: 'Конец игры' }
  ];
  const GUIDE_ORDER = ['1860', '1849', '1822pnw', '1822ca', '1880', '1846'];
  const slug = document.body.dataset.game;
  const guides = window.GUIDES || {};
  const game = guides[slug];
  const root = document.getElementById('guide-root');

  if (!root) return;
  if (!game) {
    root.innerHTML = '<main class="catalog-main"><h1>Памятка недоступна</h1><p>Данные игры не загрузились. Обновите страницу или вернитесь в <a href="index.html">каталог</a>.</p></main>';
    return;
  }

  const storageKey = `18xx-guide-${slug}-v1`;
  const defaultPlayers = game.players.includes(4) ? 4 : game.players[0];
  const state = {
    tab: 'overview',
    players: String(defaultPlayers),
    phase: game.defaultPhase || game.phases[0].id,
    scenario: game.scenario ? game.scenario.default : null,
    checked: {}
  };

  /**
   * Create a DOM element with optional class and plain text. Data rendered through
   * this helper is treated as text, so it cannot alter document structure.
   * @param {string} tag - HTML tag name to create.
   * @param {string} className - Optional CSS class string.
   * @param {string|number} value - Optional text value.
   * @returns {HTMLElement} The detached element.
   */
  function element(tag, className = '', value = '') {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== '') node.textContent = String(value);
    return node;
  }

  /**
   * Insert authored rule text that may contain trusted inline HTML. The catalog
   * data is maintained with this site and must not contain user supplied markup.
   * @param {HTMLElement} node - Destination for a rule paragraph or summary.
   * @param {string} value - Trusted HTML fragment from guides-data.js.
   */
  function setRuleHtml(node, value) {
    node.innerHTML = value || '';
  }

  /**
   * Check whether an authored section id belongs to the five fixed tabs.
   * @param {string} id - Candidate section identifier from storage or an event.
   * @returns {boolean} Whether a matching section exists.
   */
  function hasSection(id) {
    for (const section of SECTION_DEFS) if (section.id === id) return true;
    return false;
  }

  /**
   * Check a candidate phase against this game's authored train phases.
   * @param {string} id - Candidate phase identifier from storage or a selector.
   * @returns {boolean} Whether the phase is available in this game.
   */
  function hasPhase(id) {
    for (const phase of game.phases) if (phase.id === id) return true;
    return false;
  }

  /**
   * Check a candidate scenario without assuming every game has scenarios.
   * @param {string} id - Candidate scenario identifier.
   * @returns {boolean} Whether it is one of the current game's options.
   */
  function hasScenario(id) {
    if (!game.scenario) return false;
    for (const option of game.scenario.options) if (option.id === id) return true;
    return false;
  }

  /**
   * Load recognized reading preferences and OR checkmarks. Storage failures and
   * stale values leave valid defaults in place so the guide remains usable.
   */
  function restoreState() {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
      if (!saved || typeof saved !== 'object') return;
      if (hasSection(saved.tab)) state.tab = saved.tab;
      if (game.players.includes(Number(saved.players))) state.players = saved.players;
      if (hasPhase(saved.phase)) state.phase = saved.phase;
      if (hasScenario(saved.scenario)) state.scenario = saved.scenario;
      if (saved.checked && typeof saved.checked === 'object') {
        for (let index = 0; index < game.orSteps.length; index += 1) {
          state.checked[index] = saved.checked[index] === true;
        }
      }
    } catch (_error) {
      // Private browsing or corrupt storage must not prevent reading the guide.
    }
  }

  /** Persist the current selections and checklist without requiring storage access. */
  function saveState() {
    try {
      localStorage.setItem(storageKey, JSON.stringify(state));
    } catch (_error) {
      // Persistence is optional in private browsing and restricted environments.
    }
  }

  /**
   * Add a single rule card to the requested section, preserving trusted inline
   * emphasis in its body while keeping its heading plain text.
   * @param {HTMLElement} container - Grid receiving the new card.
   * @param {{title:string,body:string}} card - Authored card content.
   * @param {number} index - One-based display order within the section.
   */
  function appendCard(container, card, index) {
    const article = element('article', 'rule-card');
    article.append(element('span', 'card-index', String(index).padStart(2, '0')));
    article.append(element('h3', '', card.title));
    const body = element('p');
    setRuleHtml(body, card.body);
    article.append(body);
    container.append(article);
  }

  /**
   * Build the fixed shell used by every new guide. Gameplay content is populated
   * separately so the same tab, control and checklist behavior applies to all.
   */
  function renderShell() {
    root.innerHTML = `
      <a class="skip-link" href="#content">К содержанию</a>
      <header class="site-header"><a class="brand" href="index.html" aria-label="18xx Памятки — каталог"><span class="brand-tile" aria-hidden="true">18</span><span>18xx <strong>Памятки</strong></span></a><a class="header-caption" href="index.html">← Каталог игр</a><a class="header-source" id="header-source" target="_blank" rel="noopener noreferrer"></a></header>
      <div class="app-shell" id="top">
        <aside class="sidebar" aria-label="Каталог игр"><p class="eyebrow">Каталог / 18xx</p><h2>Игры</h2><nav id="guide-navigation" aria-label="Другие памятки"></nav><p class="sidebar-note" id="sidebar-note"></p><div class="sidebar-line" aria-hidden="true"><span></span><span></span><span></span></div></aside>
        <main id="content"><div class="breadcrumb"><a href="index.html">Каталог</a><span aria-hidden="true">/</span><strong id="breadcrumb-game"></strong></div>
          <section class="hero eastern-hero" aria-labelledby="game-title"><div class="hero-copy"><p class="eyebrow" id="hero-eyebrow"></p><h1 id="game-title"></h1><p id="hero-description"></p><div class="hero-tags" id="hero-tags"></div></div><div class="hero-rail" aria-hidden="true"><div class="rail-track"></div><span class="hex hex-one">SR</span><span class="hex hex-two">OR</span><span class="hex hex-three">18</span></div></section>
          <div class="control-bar" aria-label="Настройки памятки"><label>Игроков <select id="player-count"></select></label><label>Фаза <select id="phase"></select></label><label id="scenario-control" hidden><span id="scenario-label"></span><select id="scenario"></select></label><button id="reset-progress" type="button" class="text-button">↺ Сбросить отметки OR</button></div>
          <section class="quick-strip guide-quick-strip" aria-label="Ключевые числа"><div><span>На руки</span><strong id="starting-cash"></strong></div><div><span>Сертификаты</span><strong id="certificate-limit"></strong></div><div><span>Банк</span><strong id="bank"></strong></div></section>
          <div class="tab-list" role="tablist" aria-label="Разделы памятки" id="guide-tabs"></div><div id="guide-panels"></div>
          <footer class="footer"><p>По <a id="footer-source" target="_blank" rel="noopener noreferrer"></a>. При споре за столом сверяйтесь с полным текстом правил.</p><p id="footer-edition"></p></footer>
        </main>
      </div>`;
    document.title = `${game.title} — интерактивная памятка 18xx`;
    document.getElementById('breadcrumb-game').textContent = game.title;
    const counts = game.players;
    const playerRange = counts.length === 1 ? counts[0] : `${Math.min(...counts)}–${Math.max(...counts)}`;
    document.getElementById('hero-eyebrow').textContent = `Интерактивная памятка · ${playerRange} игроков`;
    const heading = document.getElementById('game-title');
    heading.append(document.createTextNode(`${game.title} `), element('span', '', game.subtitle));
    setRuleHtml(document.getElementById('hero-description'), game.description);
    for (const [label, className] of [[game.edition, 'green'], [game.region, 'yellow'], [game.duration, 'neutral']]) {
      if (label) document.getElementById('hero-tags').append(element('span', `tag ${className}`, label));
    }
    document.getElementById('sidebar-note').textContent = game.description.replace(/<[^>]*>/g, '');
    document.getElementById('footer-edition').textContent = [game.edition, game.duration].filter(Boolean).join(' · ');
    for (const id of ['header-source', 'footer-source']) {
      const source = document.getElementById(id);
      source.href = game.sourceUrl;
      source.textContent = game.sourceLabel || 'Полные правила';
    }
    document.getElementById('header-source').append(document.createTextNode(' ↗'));
  }

  /** Populate the sidebar with direct links to the existing and new game guides. */
  function renderNavigation() {
    const nav = document.getElementById('guide-navigation');
    const links = [
      ['18do.html', '18DO', 'Dortmund'],
      ['1862.html', '1862', 'Eastern Counties']
    ];
    for (const id of GUIDE_ORDER) {
      if (guides[id]) links.push([`${id}.html`, guides[id].title, guides[id].subtitle]);
    }
    for (const [href, title, subtitle] of links) {
      const link = element('a', `game-link${href === `${slug}.html` ? ' active' : ''}`);
      link.href = href;
      if (href === `${slug}.html`) link.setAttribute('aria-current', 'page');
      link.append(element('span', 'game-number', title.replace(/\D/g, '').slice(-2) || '18'));
      const copy = element('span');
      copy.append(element('strong', '', title), element('small', '', subtitle));
      link.append(copy, element('span', '', '↗'));
      link.lastElementChild.setAttribute('aria-hidden', 'true');
      nav.append(link);
    }
  }

  /** Create the player, phase and optional scenario choices supplied by the game. */
  function renderControls() {
    const players = document.getElementById('player-count');
    for (const count of game.players) {
      const option = element('option', '', `${count} игрок${count === 2 || count === 3 || count === 4 ? 'а' : 'ов'}`);
      option.value = String(count);
      players.append(option);
    }
    const phases = document.getElementById('phase');
    for (const phase of game.phases) {
      const option = element('option', '', phase.label);
      option.value = phase.id;
      phases.append(option);
    }
    if (game.scenario) {
      document.getElementById('scenario-control').hidden = false;
      document.getElementById('scenario-label').textContent = game.scenario.label;
      const select = document.getElementById('scenario');
      for (const scenario of game.scenario.options) {
        const option = element('option', '', scenario.label);
        option.value = scenario.id;
        select.append(option);
      }
    }
  }

  /**
   * Build each accessible tab and its panel, then place the game's timeline and
   * rule cards in their named sections.
   */
  function renderSections() {
    const tabs = document.getElementById('guide-tabs');
    const panels = document.getElementById('guide-panels');
    for (const [index, definition] of SECTION_DEFS.entries()) {
      const tab = element('button', 'tab');
      tab.type = 'button';
      tab.id = `tab-${definition.id}`;
      tab.dataset.tab = definition.id;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', definition.id);
      tab.setAttribute('aria-selected', 'false');
      tab.tabIndex = -1;
      tab.append(document.createTextNode(`${String(index + 1).padStart(2, '0')} `), element('span', '', definition.label));
      tabs.append(tab);

      const panel = element('section', 'panel');
      panel.id = definition.id;
      panel.setAttribute('role', 'tabpanel');
      panel.setAttribute('aria-labelledby', tab.id);
      panel.tabIndex = 0;
      panel.hidden = true;
      const head = element('div', 'section-head');
      head.append(element('p', 'eyebrow', definition.eyebrow), element('h2', '', definition.heading));
      const intro = element('p');
      setRuleHtml(intro, game.sections[definition.id].intro);
      head.append(intro);
      panel.append(head);
      if (definition.id === 'overview' && game.timeline.length) {
        const timeline = element('div', 'route-timeline guide-timeline');
        timeline.setAttribute('role', 'list');
        for (const item of game.timeline) {
          const stop = element('div');
          stop.setAttribute('role', 'listitem');
          const text = element('span');
          setRuleHtml(text, item);
          stop.append(text);
          timeline.append(stop);
        }
        panel.append(timeline);
      }
      if (definition.id === 'trains') {
        const phaseCard = element('div', 'phase-card');
        phaseCard.innerHTML = '<div><span class="eyebrow">Выбранная фаза</span><strong id="phase-name"></strong><span id="phase-label"></span></div><p id="phase-detail"></p>';
        panel.append(phaseCard);
      }
      if (definition.id === 'operating') renderChecklist(panel);
      const cards = element('div', 'two-col guide-card-grid');
      for (const [cardIndex, card] of game.sections[definition.id].cards.entries()) appendCard(cards, card, cardIndex + 1);
      panel.append(cards);
      panels.append(panel);
    }
  }

  /**
   * Add the ordered OR checklist and an accessible progress indicator to its
   * panel. The saved keys use step positions within this game's authored list.
   * @param {HTMLElement} panel - Operating Round tab panel.
   */
  function renderChecklist(panel) {
    const heading = element('h3', 'subheading', 'Порядок Operating Round');
    panel.append(heading);
    const list = element('div', 'guide-checklist');
    for (const [index, step] of game.orSteps.entries()) {
      const label = element('label', 'check-step');
      const input = element('input');
      input.type = 'checkbox';
      input.dataset.check = String(index);
      const content = element('span');
      content.append(element('b', '', `${String(index + 1).padStart(2, '0')} · ${step.title}`));
      const detail = element('small');
      setRuleHtml(detail, step.body);
      content.append(detail);
      label.append(input, content);
      list.append(label);
    }
    panel.append(list);
    const progress = element('div', 'progress-line');
    progress.innerHTML = '<span id="progress-label" aria-live="polite"></span><div class="progress-track" id="progress-track" role="progressbar" aria-label="Шаги OR" aria-valuemin="0"><span id="progress-fill"></span></div>';
    panel.append(progress);
  }

  /**
   * Show one panel and synchronize tab selection and keyboard focus order.
   * @param {string} name - A fixed section identifier.
   */
  function showTab(name) {
    if (!hasSection(name)) return;
    state.tab = name;
    for (const panel of document.querySelectorAll('[role="tabpanel"]')) {
      panel.hidden = panel.id !== name;
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
   * Update all three financial figures for player count. Some games vary bank
   * size or certificate limits by player count or selected scenario.
   */
  function updatePlayerRules() {
    document.getElementById('player-count').value = state.players;
    document.getElementById('starting-cash').textContent = game.startingCash[state.players] || '—';
    const scenarioLimits = game.scenario && game.scenario.limitByOption[state.scenario];
    document.getElementById('certificate-limit').textContent = (scenarioLimits && scenarioLimits[state.players]) || game.certificateLimit[state.players] || '—';
    document.getElementById('bank').textContent = (game.bankByPlayers && game.bankByPlayers[state.players]) || game.bank;
    if (game.scenario) document.getElementById('scenario').value = state.scenario;
    saveState();
  }

  /** Show the current phase's label and authored summary in the train panel. */
  function updatePhase() {
    let phase = game.phases[0];
    for (const candidate of game.phases) if (candidate.id === state.phase) phase = candidate;
    state.phase = phase.id;
    document.getElementById('phase').value = phase.id;
    document.getElementById('phase-name').textContent = phase.label;
    document.getElementById('phase-label').textContent = `Фаза ${phase.label}`;
    setRuleHtml(document.getElementById('phase-detail'), phase.summary);
    saveState();
  }

  /** Repaint checkbox values, count completed steps, and expose progress to AT. */
  function updateProgress() {
    const inputs = Array.from(document.querySelectorAll('[data-check]'));
    let done = 0;
    for (const input of inputs) {
      input.checked = state.checked[input.dataset.check] === true;
      if (input.checked) done += 1;
    }
    const total = inputs.length;
    document.getElementById('progress-label').textContent = `${done} из ${total} шагов отмечено`;
    document.getElementById('progress-fill').style.width = `${total ? Math.round(done / total * 100) : 0}%`;
    const track = document.getElementById('progress-track');
    track.setAttribute('aria-valuenow', String(done));
    track.setAttribute('aria-valuemax', String(total));
  }

  /**
   * Handle tab activation and checklist reset using only controls in this guide.
   * @param {MouseEvent} event - Click event bubbling through the guide root.
   */
  function handleClick(event) {
    if (!(event.target instanceof Element)) return;
    const tab = event.target.closest('[data-tab]');
    if (tab) {
      showTab(tab.dataset.tab);
    } else if (event.target.closest('#reset-progress')) {
      state.checked = {};
      updateProgress();
      saveState();
    }
  }

  /**
   * Apply validated selector choices or save a changed OR checkmark.
   * @param {Event} event - Change event from a guide control.
   */
  function handleChange(event) {
    const target = event.target;
    if (!(target instanceof HTMLInputElement || target instanceof HTMLSelectElement)) return;
    if (target.id === 'player-count' && game.players.includes(Number(target.value))) {
      state.players = target.value;
      updatePlayerRules();
    } else if (target.id === 'scenario' && hasScenario(target.value)) {
      state.scenario = target.value;
      updatePlayerRules();
    } else if (target.id === 'phase' && hasPhase(target.value)) {
      state.phase = target.value;
      updatePhase();
    } else if (target.matches('[data-check]')) {
      state.checked[target.dataset.check] = target.checked;
      updateProgress();
      saveState();
    }
  }

  /**
   * Provide arrow, Home and End key movement expected by an ARIA tablist.
   * @param {KeyboardEvent} event - Keydown event originating on a section tab.
   */
  function handleTabKeys(event) {
    if (!(event.target instanceof Element) || !event.target.matches('[role="tab"]')) return;
    const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
    const index = tabs.indexOf(event.target);
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

  /** Render the full guide and restore its saved reading and checklist state. */
  function initialize() {
    restoreState();
    renderShell();
    renderNavigation();
    renderControls();
    renderSections();
    updatePlayerRules();
    updatePhase();
    updateProgress();
    showTab(state.tab);
    root.addEventListener('click', handleClick);
    root.addEventListener('change', handleChange);
    document.getElementById('guide-tabs').addEventListener('keydown', handleTabKeys);
  }

  initialize();
}());
