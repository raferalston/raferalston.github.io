"""Короткие функции для описания уроков в tools/lessons_*.py."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def task(title, text='', **kw):
    """Задание.

    level        1/2/3 — сложность
    new          True — новое задание
    mode         'html' — редактор всей страницы (по умолчанию), 'js' — редактор JavaScript
    starter      стартовый код в редакторе
    fixture      (mode='js') HTML, внутри которого выполняется код ученика
    tests        список проверок (см. has/style/dom/io/call/code_has)
    solution     эталонное решение (показывается как ответ, по нему проверяются тесты)
    demo         код примера (скрыт, запускается кнопкой). Для mode='js' — JavaScript
    demo_fixture HTML для примера на JavaScript
    example      ссылка на готовую страницу-образец (открывается в новой вкладке)
    answer_pages старые страницы с ответом-картинкой
    answer_link  ссылка на старую страницу с ответом
    images       картинки к условию
    local        True — задача только для VS Code (большие проекты, свои картинки)
    hint         подсказка (html)
    examples     [(подпись, текст)] — пример работы
    """
    kw.setdefault('answer', kw.get('solution'))
    return dict(type='task', title=title, text=text, **kw)


def sec(title, items, emoji='', id=None):
    return dict(title=title, items=items, emoji=emoji, id=id)


def note(text, cls=''):
    return dict(type='note', text=text, cls=cls)


def html(s):
    return dict(type='html', html=s)


def images(*imgs):
    return dict(type='images', images=list(imgs))


def table(head, rows, caption=''):
    return dict(type='table', head=head, rows=rows, caption=caption)


def steps(*items):
    """Шаги инструкции: строка, (текст, [картинки]) или dict(text=, images=, attrs=, title_attrs=)."""
    return dict(type='steps', steps=list(items))


def code(src, lang=''):
    return dict(type='code', code=src, lang=lang)


def sandbox(src, mode='html', fixture=''):
    return dict(type='sandbox', code=src, mode=mode, fixture=fixture)


def P(*paras):
    return ''.join(f'<p>{p}</p>' for p in paras)


def UL(*items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def C(s):
    """Код внутри текста задания: C('<h1>') → <code>&lt;h1&gt;</code>."""
    return '<code>' + s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + '</code>'


# ---------- проверки ----------
# Проверки выполняются внутри страницы ученика. В коде проверки доступны помощники:
#   $(sel), $$(sel), has(sel), count(sel), text(sel), css(sel, prop), cssIs(sel, prop, value),
#   out() — всё, что вывели console.log/alert/prompt, click(sel), fire(el, type, props), wait(ms),
#   rule(/селектор/, 'свойство'), keyframes(), media(), pixel(canvas, x, y), code — код ученика.
# Проверка возвращает true, если всё хорошо, или строку с объяснением ошибки.

def js_str(s):
    return json.dumps(s, ensure_ascii=False)


def dom(label, js, inputs=None):
    """Произвольная проверка: тело async-функции, которое возвращает true или текст ошибки.
    inputs — ответы на prompt() для этой проверки."""
    t = {'js': js, 'label': label}
    if inputs is not None:
        t['inputs'] = [None if x is None else str(x) for x in inputs]
    return t


def has(sel, label=None, min=1, why=None):
    why = why or (f'Не нашёл элемент {sel}' if min == 1 else f'Нужно хотя бы {min} шт. {sel}')
    return dom(label or f'Есть {sel}' + (f' (не меньше {min})' if min > 1 else ''),
               f'return count({js_str(sel)}) >= {min} || {js_str(why)} + " (сейчас: " + count({js_str(sel)}) + ")";')


def style(sel, prop, value, label=None):
    """Вычисленный стиль элемента равен value (цвета можно писать любым способом: red, #f00, rgb())."""
    return dom(label or f'{sel} {{ {prop}: {value} }}',
               f'if (!has({js_str(sel)})) return "Не нашёл элемент {sel}"; '
               f'return cssIs({js_str(sel)}, {js_str(prop)}, {js_str(value)}) || '
               f'"Сейчас {prop} = " + css({js_str(sel)}, {js_str(prop)});')


def io(inputs, expect=(), reject=(), label=None):
    """Запустить код, отвечая на prompt() значениями inputs (None — «Отмена»), и проверить вывод (console.log, alert, текст prompt)."""
    t = {'inputs': [None if x is None else str(x) for x in inputs], 'expect': list(expect)}
    if reject:
        t['reject'] = list(reject)
    if label:
        t['label'] = label
    return t


def call(expr, want, label=None):
    """Выполнить выражение expr и сравнить результат с want (оба — строки с кодом JavaScript)."""
    t = {'call': expr, 'want': want}
    if label:
        t['label'] = label
    return t


def code_has(pattern, label, why=None, flags=''):
    """В коде ученика есть совпадение с регулярным выражением pattern."""
    return dom(label, f'return new RegExp({js_str(pattern)}, {js_str(flags)}).test(code) || {js_str(why or "В коде не нашёл: " + label)};')


def var_is(name, want, label=None):
    """Переменная name существует и равна want (код JavaScript)."""
    return dom(label or f'{name} === {want}',
               f'if (typeof {name} === "undefined") return "Переменная {name} не создана"; '
               f'return same({name}, {want}) || "Сейчас {name} = " + show({name});')


def read_file(name):
    with open(os.path.join(ROOT, name), encoding='utf-8') as f:
        return f.read()


def body_script(page):
    """JavaScript из старой страницы-ответа (содержимое последнего <script> в <body>)."""
    src = read_file(page)
    scripts = re.findall(r'<script>(.*?)</script>', src, flags=re.S)
    return dedent(scripts[-1]) if scripts else ''


def dedent(s):
    lines = s.strip('\n').splitlines()
    pad = min((len(l) - len(l.lstrip()) for l in lines if l.strip()), default=0)
    return '\n'.join(l[pad:] for l in lines).strip() + '\n'
