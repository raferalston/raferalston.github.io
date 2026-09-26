/* КИДКОД · домашние задания по веб-дизайну
 * - тема (светлая/тёмная)
 * - прогресс по заданиям (localStorage)
 * - редактор кода (CodeMirror), живой просмотр страницы и автопроверка
 *   Код ученика выполняется в изолированном iframe (sandbox без allow-same-origin),
 *   поэтому он не может ничего сломать на самой странице с заданиями.
 */
(function () {
  'use strict';

  const CDN = 'https://cdn.jsdelivr.net/npm/';
  const CM_BASE = window.KK_CM_BASE || CDN + 'codemirror@5.65.21/';
  const CHECK_TIMEOUT = 6000;
  const NO_INPUT = 'KK_NO_MORE_INPUT';

  /* ---------- безопасное хранилище ---------- */
  const store = {
    get(key, def) {
      try { const v = localStorage.getItem(key); return v === null ? def : JSON.parse(v); } catch (e) { return def; }
    },
    set(key, val) {
      try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) { /* приватный режим */ }
    },
    del(key) {
      try { localStorage.removeItem(key); } catch (e) { /* ignore */ }
    },
  };

  /* ---------- тема ---------- */
  function applyTheme(t) {
    if (t) document.documentElement.setAttribute('data-theme', t);
    else document.documentElement.removeAttribute('data-theme');
  }
  applyTheme(store.get('kkw:theme', null));

  function currentTheme() {
    const t = document.documentElement.getAttribute('data-theme');
    if (t) return t;
    return window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  /* ---------- прогресс ---------- */
  const Progress = {
    all() { return store.get('kkw:done', {}); },
    has(key) { return !!this.all()[key]; },
    set(key, val) {
      const d = this.all();
      if (val) d[key] = Date.now(); else delete d[key];
      store.set('kkw:done', d);
      document.dispatchEvent(new CustomEvent('kk:progress'));
    },
  };
  window.KKProgress = Progress;

  /* ---------- утилиты ---------- */
  function el(tag, attrs, children) {
    const n = document.createElement(tag);
    if (attrs) for (const k in attrs) {
      if (k === 'class') n.className = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else if (k === 'html') n.innerHTML = attrs[k];
      else if (k.startsWith('on')) n.addEventListener(k.slice(2), attrs[k]);
      else n.setAttribute(k, attrs[k]);
    }
    (children || []).forEach((c) => n.append(c));
    return n;
  }

  function loadScript(src) {
    return new Promise((res, rej) => {
      const s = document.createElement('script');
      s.src = src; s.onload = res; s.onerror = () => rej(new Error('Не удалось загрузить ' + src));
      document.head.append(s);
    });
  }
  function loadCss(href) {
    const l = document.createElement('link');
    l.rel = 'stylesheet'; l.href = href; document.head.append(l);
  }

  /* ================================================================
   * Песочница: код, который выполняется внутри iframe
   * ================================================================ */
  // Эта функция не вызывается на странице: её текст вставляется в iframe.
  function prelude(cfg) {
    var NO_INPUT = 'KK_NO_MORE_INPUT';
    var send = function (m) { m.token = cfg.token; try { parent.postMessage(m, '*'); } catch (e) { /* ignore */ } };
    var output = [];
    var errors = [];
    var inputs = (cfg.inputs || []).slice();
    var testing = cfg.mode === 'test';

    function show(v, depth) {
      depth = depth || 0;
      if (typeof v === 'string') return depth ? JSON.stringify(v) : v;
      if (v === null) return 'null';
      if (v === undefined) return 'undefined';
      if (typeof v === 'function') return 'ƒ ' + (v.name || 'function') + '()';
      if (typeof v === 'number' && Object.is(v, -0)) return '-0';
      if (typeof v !== 'object') return String(v);
      if (depth > 3) return Array.isArray(v) ? '[…]' : '{…}';
      try {
        if (typeof Node !== 'undefined' && v instanceof Node) {
          if (v.nodeType === 1) return '<' + v.tagName.toLowerCase() + (v.id ? '#' + v.id : '') + (v.className && typeof v.className === 'string' ? '.' + v.className.trim().split(/\s+/).join('.') : '') + '>';
          return v.nodeName;
        }
        if (Array.isArray(v)) return '[' + v.map(function (x) { return show(x, depth + 1); }).join(', ') + ']';
        if (v instanceof Error) return v.name + ': ' + v.message;
        if (typeof NodeList !== 'undefined' && (v instanceof NodeList || v instanceof HTMLCollection)) {
          return (v instanceof NodeList ? 'NodeList' : 'HTMLCollection') + '(' + v.length + ') [' + Array.prototype.map.call(v, function (x) { return show(x, depth + 1); }).join(', ') + ']';
        }
        var keys = Object.keys(v);
        return '{' + keys.map(function (k) { return k + ': ' + show(v[k], depth + 1); }).join(', ') + '}';
      } catch (e) { return String(v); }
    }

    function emit(kind, text) {
      output.push(text);
      send({ type: 'log', kind: kind, text: text });
    }

    ['log', 'info', 'warn', 'error', 'debug'].forEach(function (k) {
      var orig = console[k];
      console[k] = function () {
        var text = Array.prototype.map.call(arguments, function (a) { return show(a); }).join(' ');
        emit(k === 'warn' ? 'warn' : k === 'error' ? 'err' : 'out', text);
        try { orig.apply(console, arguments); } catch (e) { /* ignore */ }
      };
    });
    console.clear = function () { send({ type: 'clear' }); };

    var nativeAlert = window.alert, nativePrompt = window.prompt, nativeConfirm = window.confirm;
    window.alert = function (msg) {
      var text = msg === undefined ? '' : show(msg);
      emit('alert', text);
      if (!testing) { try { nativeAlert.call(window, text); } catch (e) { /* ignore */ } }
    };
    function nextInput(msg) {
      if (!inputs.length) throw new Error(NO_INPUT);
      var v = inputs.shift();
      var text = msg === undefined ? '' : show(msg);
      output.push(text);
      send({ type: 'log', kind: 'prompt', text: text, value: v });
      return v;
    }
    window.prompt = function (msg, def) {
      if (testing) return nextInput(msg);
      var v = null;
      try { v = nativePrompt.call(window, msg === undefined ? '' : show(msg), def === undefined ? '' : def); } catch (e) { v = null; }
      send({ type: 'log', kind: 'prompt', text: (msg === undefined ? '' : show(msg)), value: v });
      return v;
    };
    window.confirm = function (msg) {
      if (testing) { var v = nextInput(msg); return /^(true|да|yes|ok|1)$/i.test(String(v)); }
      var r = false;
      try { r = nativeConfirm.call(window, msg === undefined ? '' : show(msg)); } catch (e) { r = false; }
      send({ type: 'log', kind: 'prompt', text: (msg === undefined ? '' : show(msg)), value: r ? 'OK' : 'Отмена' });
      return r;
    };

    function isNoInput(msg) { return String(msg || '').indexOf(NO_INPUT) !== -1; }
    window.addEventListener('error', function (e) {
      var msg = e.message || (e.error && e.error.message) || 'Ошибка';
      if (isNoInput(msg)) { e.preventDefault(); send({ type: 'noinput' }); return; }
      var line = e.lineno ? e.lineno - (cfg.lineOffset || 0) : 0;
      var text = msg + (line > 0 ? ' (строка ' + line + ')' : '');
      errors.push(text);
      send({ type: 'log', kind: 'err', text: '⚠ ' + text });
    });
    window.addEventListener('unhandledrejection', function (e) {
      var msg = e.reason && e.reason.message ? e.reason.message : String(e.reason);
      if (isNoInput(msg)) return;
      errors.push(msg);
      send({ type: 'log', kind: 'err', text: '⚠ ' + msg });
    });

    // Ссылки внутри просмотра не должны уводить с задания
    document.addEventListener('click', function (e) {
      var a = e.target && e.target.closest && e.target.closest('a[href]');
      if (!a) return;
      var href = a.getAttribute('href');
      if (href && href.charAt(0) === '#') {
        e.preventDefault();
        var id = decodeURIComponent(href.slice(1));
        var t = id ? document.getElementById(id) || document.getElementsByName(id)[0] : document.body;
        if (t) t.scrollIntoView({ behavior: 'smooth' }); else window.scrollTo(0, 0);
        return;
      }
      if (!testing && a.target !== '_blank') { e.preventDefault(); send({ type: 'log', kind: 'info', text: '🔗 Ссылка: ' + href }); }
    }, true);

    if (!testing) return;

    /* ---------- помощники для проверок ---------- */
    var H = {};
    H.$ = function (s) { return typeof s === 'string' ? document.querySelector(s) : s; };
    H.$$ = function (s) { return Array.prototype.slice.call(document.querySelectorAll(s)); };
    H.has = function (s) { return !!document.querySelector(s); };
    H.count = function (s) { return document.querySelectorAll(s).length; };
    H.text = function (s) { var e = H.$(s); return e ? e.textContent.replace(/\s+/g, ' ').trim() : ''; };
    H.css = function (s, prop, pseudo) { var e = H.$(s); return e ? getComputedStyle(e, pseudo || null).getPropertyValue(prop).trim() : ''; };
    H.norm = function (prop, value) {
      var d = document.createElement('div');
      d.style.setProperty(prop, value);
      if (!d.style.getPropertyValue(prop)) return String(value).trim();
      d.style.visibility = 'hidden';
      if (!/^(position|display|float)$/.test(prop)) d.style.position = 'absolute';
      if (/^border.*width$/.test(prop)) d.style.borderStyle = 'solid';
      if (/^outline.*width$/.test(prop)) d.style.outlineStyle = 'solid';
      (document.body || document.documentElement).appendChild(d);
      var v = getComputedStyle(d).getPropertyValue(prop).trim();
      d.remove();
      return v;
    };
    H.cssIs = function (s, prop, value, pseudo) {
      var actual = H.css(s, prop, pseudo);
      var want = H.norm(prop, value);
      return actual === want || actual.replace(/\s+/g, '') === want.replace(/\s+/g, '');
    };
    H.px = function (v) { return parseFloat(v) || 0; };
    H.out = function () { return output.join('\n'); };
    H.lines = function () { return output.slice(); };
    H.errors = function () { return errors.slice(); };
    H.wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms || 50); }); };
    H.fire = function (target, type, props) {
      var e = H.$(target);
      if (!e) throw new Error('Не нашёл элемент ' + target);
      var ev;
      if (/^key/.test(type)) ev = new KeyboardEvent(type, Object.assign({ bubbles: true, cancelable: true }, props || {}));
      else if (/^(click|dblclick|mouse|contextmenu)/.test(type)) ev = new MouseEvent(type, Object.assign({ bubbles: true, cancelable: true, view: window }, props || {}));
      else if (/^(input|change|submit)$/.test(type)) ev = new Event(type, { bubbles: true, cancelable: true });
      else ev = new Event(type, Object.assign({ bubbles: true, cancelable: true }, props || {}));
      e.dispatchEvent(ev);
      return ev;
    };
    H.click = function (s) { var e = H.$(s); if (!e) throw new Error('Не нашёл элемент ' + s); e.click(); };
    H.show = function (v) { return show(v, 1); };
    H.same = function (a, b) {
      if (a === b) return true;
      if (typeof a === 'number' && typeof b === 'number') return Math.abs(a - b) < 1e-9 || (isNaN(a) && isNaN(b));
      if (a && b && typeof a === 'object' && typeof b === 'object') {
        if (Array.isArray(a) !== Array.isArray(b)) return false;
        var ka = Object.keys(a), kb = Object.keys(b);
        if (ka.length !== kb.length) return false;
        return ka.every(function (k) { return H.same(a[k], b[k]); });
      }
      return false;
    };
    // все CSS-правила страницы (включая вложенные в @media)
    H.rules = function () {
      var list = [];
      function walk(rules, media) {
        Array.prototype.forEach.call(rules || [], function (r) {
          if (r.cssRules && !r.selectorText && r.type !== 7) walk(r.cssRules, r.media ? r.media.mediaText : media);
          r.kkMedia = media || '';
          list.push(r);
        });
      }
      Array.prototype.forEach.call(document.styleSheets, function (sh) { try { walk(sh.cssRules); } catch (e) { /* чужой CSS */ } });
      return list;
    };
    // правило, у которого селектор подходит под регулярное выражение: rule(/:hover/)
    H.rule = function (re, prop) {
      return H.rules().filter(function (r) {
        return r.selectorText && re.test(r.selectorText) && (!prop || r.style.getPropertyValue(prop));
      })[0] || null;
    };
    H.keyframes = function () { return H.rules().filter(function (r) { return r.type === 7; }); };
    H.media = function () { return H.rules().filter(function (r) { return r.type === 4; }); };
    // цвет пикселя на canvas: [r, g, b, a]
    H.pixel = function (s, x, y) {
      var c = H.$(s || 'canvas');
      if (!c) throw new Error('Не нашёл canvas');
      return Array.prototype.slice.call(c.getContext('2d').getImageData(x, y, 1, 1).data);
    };
    H.code = cfg.code || '';
    window.__kkH = H;

    function normText(s) { return String(s).replace(/\s+/g, ' ').trim().toLowerCase(); }
    var AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
    var names = Object.keys(H);

    async function runTests() {
      var results = [];
      var tests = cfg.tests || [];
      for (var i = 0; i < tests.length; i++) {
        var t = tests[i];
        var r = { label: t.label || '', ok: false };
        try {
          if (t.js) {
            var fn = new AsyncFunction(names.join(','), t.js);
            var v = await fn.apply(null, names.map(function (k) { return H[k]; }));
            if (v === true || v === undefined) r.ok = true;
            else r.msg = typeof v === 'string' ? v : 'Проверка не пройдена';
          } else if (t.call) {
            if (!r.label) r.label = t.call + ' → ' + t.want;
            var got = (0, eval)(t.call);
            if (got && typeof got.then === 'function') got = await got;
            var want = (0, eval)('(' + t.want + ')');
            r.ok = H.same(got, want);
            if (!r.ok) r.msg = 'Ожидалось: ' + show(want, 1) + '\nПолучилось: ' + show(got, 1);
          } else if (t.expect) {
            var text = normText(output.join('\n'));
            var missing = t.expect.filter(function (x) { return text.indexOf(normText(x)) === -1; });
            var extra = (t.reject || []).filter(function (x) { return text.indexOf(normText(x)) !== -1; });
            if (!r.label) {
              r.label = (t.inputs && t.inputs.length ? 'Ввод: ' + t.inputs.map(function (x) { return JSON.stringify(x); }).join(', ') + ' → ' : 'Вывод → ') +
                (t.expect.length ? t.expect.map(function (x) { return JSON.stringify(x); }).join(', ') : 'без ошибок');
            }
            r.ok = !missing.length && !extra.length;
            if (!r.ok) {
              var lines = [];
              if (missing.length) lines.push('В выводе нет: ' + missing.map(function (x) { return JSON.stringify(x); }).join(', '));
              if (extra.length) lines.push('Лишнее в выводе: ' + extra.map(function (x) { return JSON.stringify(x); }).join(', '));
              lines.push('Программа вывела:\n' + (output.length ? output.join('\n') : '(ничего)'));
              r.msg = lines.join('\n');
            }
          }
        } catch (e) {
          r.ok = false;
          r.msg = isNoInput(e.message) ? 'Программа просит больше данных через prompt(), чем ожидалось' : (e.name + ': ' + e.message);
        }
        results.push(r);
      }
      send({ type: 'results', results: results, errors: errors.slice() });
    }

    function start() { setTimeout(runTests, cfg.wait || 150); }
    if (document.readyState === 'complete') start();
    else window.addEventListener('load', start);
  }

  const BASE_STYLE = '<style>html{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}</style>';

  function escScript(code) { return String(code).replace(/<\/script/gi, '<\\/script'); }

  /** Собирает HTML-документ для iframe. mode: 'html' — код это целая страница, 'js' — код это JavaScript. */
  function buildDoc(kind, code, fixture, cfg) {
    let before, after;
    if (kind === 'js') {
      before = '<!DOCTYPE html>\n<html lang="ru"><head><meta charset="UTF-8">' + BASE_STYLE + '%PRELUDE%</head><body>' + (fixture || '') + '\n<script>\n';
      after = '\n</script></body></html>';
    } else {
      before = ''; after = '';
    }
    cfg.lineOffset = 0;
    const tag = (c) => '<script>(' + prelude.toString() + ')(' + JSON.stringify(c).replace(/</g, '\\u003c') + ');</script>';
    if (kind === 'js') {
      const pre = before.replace('%PRELUDE%', () => tag(Object.assign({}, cfg, { lineOffset: 0 })));
      // строка с началом кода ученика — чтобы номера строк в ошибках совпадали с редактором
      const offset = pre.split('\n').length - 1;
      cfg.lineOffset = offset;
      return before.replace('%PRELUDE%', () => tag(cfg)) + escScript(code) + after;
    }
    // целая страница: вставляем подготовку сразу после <!DOCTYPE> или <head>
    const src = String(code);
    const m = src.match(/<head[^>]*>/i) || src.match(/<html[^>]*>/i) || src.match(/<!doctype[^>]*>/i);
    if (m) {
      const at = m.index + m[0].length;
      return src.slice(0, at) + tag(cfg) + src.slice(at);
    }
    return tag(cfg) + src;
  }

  const SANDBOX = 'allow-scripts allow-modals allow-forms allow-popups allow-popups-to-escape-sandbox';
  let tokenSeq = 0;

  /** Запускает страницу в iframe. Возвращает { frame, done } */
  function runFrame(opts) {
    const token = 'kk' + (++tokenSeq) + '_' + Math.random().toString(36).slice(2);
    const cfg = { token, mode: opts.test ? 'test' : 'run', inputs: opts.inputs || [], tests: opts.tests || [], code: opts.code, wait: opts.wait };
    const doc = buildDoc(opts.kind, opts.code, opts.fixture, cfg);
    const frame = el('iframe', { sandbox: SANDBOX, title: 'Результат', class: opts.test ? 'kk-test-frame' : 'web-frame' });
    let finish;
    const done = new Promise((resolve) => { finish = resolve; });
    let timer = null;
    let noinput = false;
    function onMsg(e) {
      const m = e.data;
      if (!m || m.token !== token || e.source !== frame.contentWindow) return;
      if (m.type === 'log' && opts.onLog) opts.onLog(m);
      else if (m.type === 'clear' && opts.onClear) opts.onClear();
      else if (m.type === 'noinput') { noinput = true; if (opts.onNoInput) opts.onNoInput(); }
      else if (m.type === 'results') { cleanup(); finish({ results: m.results, errors: m.errors, noinput }); }
    }
    function cleanup() {
      window.removeEventListener('message', onMsg);
      clearTimeout(timer);
      if (opts.test) frame.remove();
    }
    window.addEventListener('message', onMsg);
    if (opts.test) {
      timer = setTimeout(() => { cleanup(); finish({ timeout: true }); }, opts.timeout || CHECK_TIMEOUT);
    }
    frame.srcdoc = doc;
    (opts.parent || document.body).append(frame);
    return { frame, done, stop: () => { cleanup(); frame.remove(); finish({ stopped: true }); } };
  }

  /** Прогоняет все проверки задания. Проверки с разным вводом запускаются в отдельных iframe. */
  async function runChecks(kind, code, fixture, tests) {
    const groups = new Map();
    tests.forEach((t, i) => {
      const k = JSON.stringify(t.inputs || []);
      if (!groups.has(k)) groups.set(k, []);
      groups.get(k).push(i);
    });
    const results = new Array(tests.length);
    let errors = [];
    for (const [k, idx] of groups) {
      const r = await runFrame({ kind, code, fixture, test: true, inputs: JSON.parse(k), tests: idx.map((i) => tests[i]) }).done;
      if (r.timeout) {
        return { results: [{ ok: false, label: 'Время выполнения', msg: 'Страница работает слишком долго — возможно, бесконечный цикл.' }] };
      }
      idx.forEach((i, j) => { results[i] = r.results[j]; });
      errors = errors.concat(r.errors || []);
    }
    const uniq = Array.from(new Set(errors));
    if (uniq.length) results.unshift({ ok: false, label: 'Код работает без ошибок', msg: uniq.join('\n') });
    return { results };
  }

  /* ---------- редактор ---------- */
  let cmPromise = null;
  function loadCodeMirror() {
    if (!cmPromise) {
      loadCss(CM_BASE + 'lib/codemirror.css');
      cmPromise = loadScript(CM_BASE + 'lib/codemirror.js')
        .then(() => Promise.all([
          loadScript(CM_BASE + 'mode/xml/xml.js'),
          loadScript(CM_BASE + 'mode/javascript/javascript.js'),
          loadScript(CM_BASE + 'mode/css/css.js'),
          loadScript(CM_BASE + 'addon/edit/matchbrackets.js'),
          loadScript(CM_BASE + 'addon/edit/closebrackets.js'),
          loadScript(CM_BASE + 'addon/fold/xml-fold.js'),
        ]))
        .then(() => Promise.all([
          loadScript(CM_BASE + 'mode/htmlmixed/htmlmixed.js'),
          loadScript(CM_BASE + 'addon/edit/closetag.js'),
          loadScript(CM_BASE + 'addon/edit/matchtags.js'),
        ]))
        .then(() => window.CodeMirror)
        .catch(() => null);
    }
    return cmPromise;
  }

  function makeEditor(host, value, lang, onChange, onRun) {
    // Сначала — простой textarea (работает сразу), потом улучшаем до CodeMirror.
    const ta = el('textarea', { class: 'web-textarea', spellcheck: 'false', autocapitalize: 'off', 'aria-label': lang === 'js' ? 'Редактор JavaScript' : 'Редактор HTML' });
    ta.value = value;
    host.append(ta);
    const api = {
      get: () => ta.value,
      set: (v) => { ta.value = v; },
      focus: () => ta.focus(),
    };
    ta.addEventListener('input', () => onChange(ta.value));
    ta.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); onRun(); }
      else if (e.key === 'Tab' && !e.shiftKey) {
        e.preventDefault();
        ta.setRangeText('    ', ta.selectionStart, ta.selectionEnd, 'end');
        onChange(ta.value);
      }
    });
    const fit = () => { ta.style.height = 'auto'; ta.style.height = Math.max(140, ta.scrollHeight + 4) + 'px'; };
    ta.addEventListener('input', fit);
    requestAnimationFrame(fit);

    loadCodeMirror().then((CM) => {
      if (!CM) return;
      const cm = CM.fromTextArea(ta, {
        mode: lang === 'js' ? 'javascript' : 'htmlmixed', lineNumbers: true, indentUnit: 4, tabSize: 4,
        matchBrackets: true, autoCloseBrackets: true, autoCloseTags: lang !== 'js', matchTags: lang !== 'js',
        viewportMargin: Infinity, lineWrapping: false,
        extraKeys: {
          Tab: (c) => (c.somethingSelected() ? c.indentSelection('add') : c.replaceSelection('    ', 'end')),
          'Shift-Tab': (c) => c.indentSelection('subtract'),
          'Ctrl-Enter': () => onRun(), 'Cmd-Enter': () => onRun(),
          'Ctrl-/': 'toggleComment',
        },
      });
      cm.on('change', () => onChange(cm.getValue()));
      api.get = () => cm.getValue();
      api.set = (v) => cm.setValue(v);
      api.focus = () => cm.focus();
      host.classList.add('has-cm');
    });
    return api;
  }

  /* ---------- консоль ---------- */
  function makeConsole(host) {
    const pre = el('div', { class: 'web-out', 'aria-live': 'polite' });
    host.append(pre);
    const ICON = { alert: '🔔', prompt: '❓', warn: '⚠', info: 'ℹ' };
    return {
      clear() { pre.textContent = ''; },
      get empty() { return !pre.childNodes.length; },
      add(m) {
        const line = el('div', { class: 'web-line k-' + m.kind });
        if (ICON[m.kind]) line.append(el('span', { class: 'ico', text: ICON[m.kind] }));
        line.append(el('span', { class: 'txt', text: m.text }));
        if (m.kind === 'prompt') line.append(el('span', { class: 'val', text: m.value === null ? '(отмена)' : String(m.value) }));
        pre.append(line);
        pre.scrollTop = pre.scrollHeight;
      },
      info(text) { this.add({ kind: 'sys', text }); },
    };
  }

  /* ---------- блок с кодом ---------- */
  function setupWebBox(box) {
    const mode = box.dataset.mode || 'html';
    const isDemo = mode.startsWith('demo');
    const kind = mode === 'js' || mode === 'demo-js' ? 'js' : 'html';
    const srcEl = box.querySelector('textarea[data-role="code"]');
    const fixEl = box.querySelector('textarea[data-role="fixture"]');
    const initial = srcEl ? srcEl.value.replace(/\s+$/, '') + '\n' : '';
    const fixture = fixEl ? fixEl.value : '';
    const key = box.dataset.key;
    const tests = box.dataset.tests ? JSON.parse(box.dataset.tests) : null;
    const draftKey = key ? 'kkw:code:' + key : null;
    let code = draftKey ? store.get(draftKey, initial) : initial;
    const livePreview = kind === 'html' && !isDemo;
    const showFrame = kind === 'html' || !!fixture.trim();

    const bar = el('div', { class: 'web-bar' });
    const titleText = box.dataset.title || (isDemo ? 'Пример работы' : kind === 'js' ? 'Твой код · JavaScript' : 'Твой код · HTML + CSS');
    const title = el('span', { class: 'web-title', text: titleText });
    const status = el('span', { class: 'web-status' });
    const btns = el('div', { class: 'web-btns' });
    bar.append(title, status, btns);

    const runBtn = el('button', { class: 'btn btn-run', type: 'button' });
    runBtn.innerHTML = isDemo ? '<span aria-hidden="true">▶</span> Запустить пример'
      : kind === 'js' ? '<span aria-hidden="true">▶</span> Запустить' : '<span aria-hidden="true">↻</span> Обновить';
    btns.append(runBtn);
    let checkBtn = null;
    if (tests && !isDemo) {
      checkBtn = el('button', { class: 'btn btn-check', type: 'button' });
      checkBtn.innerHTML = '<span aria-hidden="true">✓</span> Проверить';
      btns.append(checkBtn);
    }
    let openBtn = null;
    if (showFrame) {
      openBtn = el('button', { class: 'btn btn-ghost btn-icon', type: 'button', title: 'Открыть в новой вкладке', 'aria-label': 'Открыть в новой вкладке' });
      openBtn.textContent = '⤢';
      btns.append(openBtn);
    }
    let resetBtn = null;
    if (!isDemo) {
      resetBtn = el('button', { class: 'btn btn-ghost btn-icon', type: 'button', title: 'Вернуть исходный код', 'aria-label': 'Вернуть исходный код' });
      resetBtn.textContent = '↺';
      btns.append(resetBtn);
    }

    box.textContent = '';
    box.append(bar);

    let editor = null;
    if (!isDemo) {
      const edHost = el('div', { class: 'web-editor' });
      box.append(edHost);
      editor = makeEditor(edHost, code, kind, (v) => {
        code = v;
        if (draftKey) { if (v === initial) store.del(draftKey); else store.set(draftKey, v); }
        if (livePreview) schedule();
      }, () => run());
      box.append(el('div', { class: 'web-hint', text: livePreview ? 'Просмотр обновляется сам · Ctrl + Enter — обновить' : 'Ctrl + Enter — запустить' }));
    }

    const viewHost = el('div', { class: 'web-view', hidden: '' });
    const viewBar = el('div', { class: 'web-view-bar' }, [el('span', { text: 'Результат' })]);
    const frameHost = el('div', { class: 'web-frame-host' });
    viewHost.append(viewBar, frameHost);
    box.append(viewHost);
    const conHost = el('div', { class: 'web-console', hidden: '' });
    conHost.append(el('div', { class: 'web-view-bar' }, [el('span', { text: 'Консоль' })]));
    box.append(conHost);
    const con = makeConsole(conHost);
    const testsHost = el('div', { class: 'web-tests', hidden: '' });
    box.append(testsHost);

    let current = null;
    let debounce = null;
    // живой просмотр не запускаем, если в коде есть alert/prompt — иначе окна будут появляться на каждую букву
    function schedule() {
      clearTimeout(debounce);
      if (/\b(alert|prompt|confirm)\s*\(/.test(code)) { status.textContent = 'Нажми «Обновить», чтобы запустить'; return; }
      debounce = setTimeout(() => run(true), 450);
    }

    function run(quiet) {
      const src = editor ? editor.get() : initial;
      if (current) current.stop();
      con.clear();
      conHost.hidden = kind !== 'js';
      if (!quiet) testsHost.hidden = true;
      viewHost.hidden = !showFrame;
      const r = runFrame({
        kind, code: src, fixture, parent: frameHost,
        onLog: (m) => { con.add(m); conHost.hidden = false; },
        onClear: () => con.clear(),
      });
      current = r;
      if (kind === 'js' && !showFrame) r.frame.classList.add('is-hidden');
      frameHost.querySelectorAll('iframe').forEach((f) => { if (f !== r.frame) f.remove(); });
      status.textContent = '';
      if (kind === 'js') {
        r.frame.addEventListener('load', () => {
          setTimeout(() => { if (con.empty && !showFrame) con.info('Программа ничего не вывела. Используй console.log() или alert().'); }, 400);
        });
      }
    }

    async function check() {
      const src = editor.get();
      testsHost.hidden = false;
      testsHost.textContent = '';
      runBtn.disabled = checkBtn.disabled = true;
      box.classList.add('is-busy');
      status.textContent = 'Проверяю…';
      let r;
      try { r = await runChecks(kind, src, fixture, tests); } catch (e) { r = { results: [{ ok: false, label: 'Запуск', msg: e.message }] }; }
      runBtn.disabled = checkBtn.disabled = false;
      box.classList.remove('is-busy');
      status.textContent = '';
      showResults(r);
    }

    function showResults(r) {
      testsHost.textContent = '';
      const results = r.results;
      const passed = results.filter((x) => x.ok).length;
      const all = passed === results.length;
      const head = el('div', { class: 'web-tests-head ' + (all ? 'ok' : 'fail') });
      head.innerHTML = all
        ? '<span class="big">🎉</span> Все проверки пройдены! Задание решено.'
        : `<span class="big">🧐</span> Пройдено ${passed} из ${results.length}. Почти! Исправь и проверь снова.`;
      testsHost.append(head);
      const ul = el('ul', { class: 'web-tests-list' });
      results.forEach((t) => {
        const li = el('li', { class: t.ok ? 'ok' : 'fail' });
        li.append(el('span', { class: 'mark', text: t.ok ? '✓' : '✗' }), el('span', { class: 'lbl', text: t.label }));
        if (!t.ok && t.msg) li.append(el('pre', { class: 'why', text: t.msg }));
        ul.append(li);
      });
      testsHost.append(ul);
      if (all && key) {
        Progress.set(key, true);
        const task = box.closest('.task');
        if (task) { task.classList.add('just-solved'); setTimeout(() => task.classList.remove('just-solved'), 1600); }
      }
    }

    function openTab() {
      const src = editor ? editor.get() : initial;
      let doc = kind === 'js'
        ? '<!DOCTYPE html>\n<html lang="ru"><head><meta charset="UTF-8"><title>Моя страница</title></head><body>\n' + fixture + '\n<script>\n' + escScript(src) + '\n</script>\n</body></html>'
        : src;
      // относительные пути к картинкам должны работать и в новой вкладке
      const base = '<base href="' + location.href.replace(/[^/]*$/, '') + '">';
      doc = /<head[^>]*>/i.test(doc) ? doc.replace(/<head[^>]*>/i, (m) => m + base) : base + doc;
      const url = URL.createObjectURL(new Blob([doc], { type: 'text/html' }));
      window.open(url, '_blank', 'noopener');
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    }

    runBtn.addEventListener('click', () => run());
    if (checkBtn) checkBtn.addEventListener('click', check);
    if (openBtn) openBtn.addEventListener('click', openTab);
    if (resetBtn) resetBtn.addEventListener('click', () => {
      if (editor.get() !== initial && !confirm('Вернуть исходный код? Твои изменения удалятся.')) return;
      editor.set(initial); code = initial; if (draftKey) store.del(draftKey);
      if (livePreview) run(true);
    });

    // Страница-просмотр для HTML рисуется сразу, когда блок появляется на экране
    if (livePreview) {
      if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver((en) => {
          if (en.some((x) => x.isIntersecting)) { io.disconnect(); if (!current) (/\b(alert|prompt|confirm)\s*\(/.test(code) ? schedule() : run(true)); }
        }, { rootMargin: '200px' });
        io.observe(box);
      } else run(true);
    }

    box._kk = { tests, kind, fixture, initial, check: (src) => runChecks(kind, src, fixture, tests) };
  }

  /* ---------- задания: отметки «готово» ---------- */
  function setupTasks() {
    const tasks = Array.from(document.querySelectorAll('.task[data-task]'));
    tasks.forEach((t) => {
      const key = t.dataset.task;
      const btn = t.querySelector('.done-btn');
      if (btn) btn.addEventListener('click', () => Progress.set(key, !Progress.has(key)));
    });
    function refresh() {
      let done = 0;
      tasks.forEach((t) => {
        const d = Progress.has(t.dataset.task);
        if (d) done++;
        t.classList.toggle('is-done', d);
        const btn = t.querySelector('.done-btn');
        if (btn) {
          btn.setAttribute('aria-pressed', d ? 'true' : 'false');
          btn.querySelector('.lbl').textContent = d ? 'Выполнено' : 'Отметить выполненным';
        }
        const nav = document.querySelector(`.toc a[href="#${t.id}"]`);
        if (nav) nav.classList.toggle('is-done', d);
      });
      document.querySelectorAll('[data-lesson-progress]').forEach((p) => {
        const total = tasks.length;
        p.querySelector('.bar i').style.width = total ? (done / total * 100) + '%' : '0';
        p.querySelector('.cnt').textContent = `${done} из ${total}`;
      });
    }
    document.addEventListener('kk:progress', refresh);
    refresh();
  }

  /* ---------- главная: прогресс по урокам ---------- */
  function setupIndex() {
    const cards = document.querySelectorAll('.lesson-card[data-lesson]');
    if (!cards.length || !window.KK_COURSE) return;
    const map = {};
    window.KK_COURSE.forEach((l) => { map[l.id] = l; });
    function refresh() {
      const done = Progress.all();
      let total = 0, solved = 0;
      cards.forEach((c) => {
        const l = map[c.dataset.lesson];
        if (!l || !l.tasks.length) return;
        const n = l.tasks.filter((k) => done[k]).length;
        total += l.tasks.length; solved += n;
        const bar = c.querySelector('.bar i');
        if (bar) bar.style.width = (n / l.tasks.length * 100) + '%';
        const cnt = c.querySelector('.cnt');
        if (cnt) cnt.textContent = `${n}/${l.tasks.length}`;
        c.classList.toggle('is-complete', n === l.tasks.length);
      });
      const all = document.querySelector('[data-total-progress]');
      if (all) {
        all.querySelector('.bar i').style.width = total ? (solved / total * 100) + '%' : '0';
        all.querySelector('.cnt').textContent = `${solved} из ${total}`;
      }
    }
    document.addEventListener('kk:progress', refresh);
    refresh();

    const filter = document.querySelector('.lesson-search');
    if (filter) filter.addEventListener('input', () => {
      const q = filter.value.trim().toLowerCase();
      cards.forEach((c) => { c.hidden = q && !c.textContent.toLowerCase().includes(q); });
    });
  }

  /* ---------- картинки: увеличение по клику ---------- */
  function setupZoom() {
    const dlg = el('dialog', { class: 'zoom' });
    const img = el('img', { alt: '' });
    dlg.append(img);
    dlg.addEventListener('click', () => dlg.close());
    document.body.append(dlg);
    document.addEventListener('click', (e) => {
      const t = e.target.closest('img.zoomable');
      if (!t || typeof dlg.showModal !== 'function') return;
      img.src = t.currentSrc || t.src; img.alt = t.alt;
      dlg.showModal();
    });
  }

  /* ---------- шапка ---------- */
  function setupHeader() {
    const btn = document.querySelector('.theme-btn');
    if (btn) btn.addEventListener('click', () => {
      const next = currentTheme() === 'dark' ? 'light' : 'dark';
      applyTheme(next); store.set('kkw:theme', next);
    });
    const reset = document.querySelector('.reset-progress');
    if (reset) reset.addEventListener('click', () => {
      if (confirm('Сбросить отметки о выполненных заданиях?')) { store.set('kkw:done', {}); document.dispatchEvent(new CustomEvent('kk:progress')); }
    });
    // Подсветка текущего задания в оглавлении
    const links = document.querySelectorAll('.toc a[href^="#"]');
    if (links.length && 'IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            links.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id));
          }
        });
      }, { rootMargin: '-30% 0px -60% 0px' });
      links.forEach((a) => { const t = document.getElementById(a.getAttribute('href').slice(1)); if (t) io.observe(t); });
    }
  }

  /* ---------- самопроверка: эталонные решения проходят тесты (tools/check_tests.js) ---------- */
  async function selfTest() {
    const report = [];
    for (const box of document.querySelectorAll('.web[data-tests]')) {
      const task = box.closest('.task');
      const sol = task && task.querySelector('pre[data-solution]');
      const name = task ? task.querySelector('h3').textContent : '?';
      if (!sol) { report.push({ task: name, ok: false, msg: 'нет решения' }); continue; }
      const r = await box._kk.check(sol.textContent);
      const bad = r.results.filter((x) => !x.ok);
      // стартовый код не должен сразу проходить проверки
      const s = await box._kk.check(box._kk.initial);
      const starterPasses = s.results.every((x) => x.ok);
      const msg = bad.map((x) => x.label + (x.msg ? ': ' + x.msg : '')).join('\n') + (starterPasses ? '\nстартовый код уже проходит все проверки' : '');
      report.push({ task: name, ok: !bad.length && !starterPasses, msg: msg.trim() });
    }
    return report;
  }
  window.KKWeb = { selfTest, runChecks };

  function init() {
    setupHeader();
    setupTasks();
    setupIndex();
    setupZoom();
    document.querySelectorAll('.web').forEach(setupWebBox);
    if (document.querySelector('.web[data-mode="html"], .web[data-mode="js"]')) loadCodeMirror();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
