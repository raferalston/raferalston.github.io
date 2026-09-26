"""Сборка страниц домашних заданий по веб-дизайну.

Задания, тексты и ссылки лежат в tools/lessons_*.py (список уроков — tools/course.py).
Запуск из корня репозитория:

    python3 tools/build.py

Скрипт перезаписывает index.html, страницы уроков из course.py и assets/course-map.js.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import course  # noqa: E402

ASSET_VER = '1'
LEVELS = {1: 'легко', 2: 'средне', 3: 'сложно'}
COURSES = {
    'basic': ('Начинающий web-дизайнер', 'HTML и CSS: теги, стили, flexbox, анимации, адаптивность и grid.'),
    'js': ('Продвинутый web-дизайнер', 'JavaScript: переменные, массивы, условия, циклы, функции, DOM, игры и canvas.'),
    'project': ('Дизайн-проект', 'Свой сайт-портфолио: макет в Figma, BEM, Sass, адаптивная вёрстка и публикация.'),
}

TG_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#29a9eb" d="M12 0a12 12 0 1 0 0 24 12 12 0 0 0 0-24z"/>'
          '<path fill="#fff" d="M5.4 11.8 16.9 7.4c.5-.2 1 .1.8 1l-2 9.3c-.1.7-.5.8-1.1.5l-3-2.2-1.4 1.4c-.2.2-.3.3-.6.3l.2-3.1 5.6-5'
          'c.2-.2 0-.3-.4-.1l-6.9 4.3-3-.9c-.6-.2-.7-.7.2-1z"/></svg>')
VK_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="#0077ff"/>'
          '<path fill="#fff" d="M12.8 17.3c-5.5 0-8.6-3.8-8.7-10h2.7c.1 4.6 2.1 6.5 3.7 6.9V7.3h2.6v4c1.6-.2 3.2-2 3.8-4h2.5'
          'a7.6 7.6 0 0 1-3.4 5 7.8 7.8 0 0 1 4 5h-2.8a4.9 4.9 0 0 0-4.1-3.6v3.6h-.3z"/></svg>')

LINK_ICONS = {'doc': '📘', 'test': '📝', 'practice': '🏋️', 'read': '📚', 'video': '🎬', 'tool': '🛠️',
              'lesson': '🌐', 'file': '📄', 'game': '🎮', 'design': '🎨'}


def esc(s):
    return html.escape(str(s), quote=True)


def code_of(value):
    """Код можно указать строкой или ссылкой на файл: 'file:flex_example.html'."""
    if value is None:
        return None
    if value.startswith('file:'):
        with open(os.path.join(ROOT, value[5:]), encoding='utf-8') as f:
            return f.read().strip('\n') + '\n'
    return value.strip('\n') + '\n'


def answer_images(page):
    """Картинки из старой страницы с ответом (lesson_X_ans_Y.html)."""
    with open(os.path.join(ROOT, page), encoding='utf-8') as f:
        return re.findall(r'<img[^>]*src="([^"]+)"', f.read())


def src_block(role, text):
    # textarea хранит код как есть: внутри не страшны ни </script>, ни теги
    return f'<textarea class="src" data-role="{role}" hidden>{esc(text)}</textarea>'


def web_box(mode, code, key=None, tests=None, fixture=None, title=None):
    attrs = [f'class="web" data-mode="{mode}"']
    if key:
        attrs.append(f'data-key="{esc(key)}"')
    if tests:
        attrs.append(f'data-tests="{esc(json.dumps(tests, ensure_ascii=False))}"')
    if title:
        attrs.append(f'data-title="{esc(title)}"')
    parts = [f'<div {" ".join(attrs)}>', src_block('code', code)]
    if fixture:
        parts.append(src_block('fixture', fixture))
    parts.append('</div>')
    return ''.join(parts)


# ---------------------------------------------------------------- куски разметки

def head(title, description, extra=''):
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8C%90%3C/text%3E%3C/svg%3E">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
    <link href="assets/kk.css?v={ASSET_VER}" rel="stylesheet">
    <script>try{{var t=localStorage.getItem('kkw:theme');if(t)document.documentElement.setAttribute('data-theme',JSON.parse(t))}}catch(e){{}}</script>{extra}
</head>
<body>
'''


def header():
    return '''<header class="site-header">
    <div class="wrap">
        <a class="logo" href="index.html" aria-label="КИДКОД — на главную">
            <span class="logo-mark">&lt;/&gt;</span>
            <span>КИДКОД<small>домашние задания · Web</small></span>
        </a>
        <nav class="nav" aria-label="Основная навигация">
            <a href="index.html#basic" class="hide-sm">HTML и CSS</a>
            <a href="index.html#js" class="hide-sm">JavaScript</a>
            <a href="index.html#project" class="hide-sm">Проект</a>
            <button class="icon-btn theme-btn" type="button" aria-label="Сменить тему"><span class="moon">🌙</span><span class="sun">☀️</span></button>
        </nav>
    </div>
</header>
'''


def footer():
    return f'''<footer class="site-footer">
    <div class="wrap">
        <div>
            <b>КИДКОД</b> — школа программирования для детей и подростков<br>
            <span>Вопросы по домашке? Пиши преподавателю:</span>
        </div>
        <div class="socials">
            <a href="https://t.me/kidkodschool" target="_blank" rel="noopener">{TG_SVG} Telegram</a>
            <a href="https://vk.com/kidkodschool" target="_blank" rel="noopener">{VK_SVG} ВКонтакте</a>
            <a href="https://kidkod.ru" target="_blank" rel="noopener">🌐 kidkod.ru</a>
        </div>
    </div>
</footer>
<script src="assets/course-map.js?v={ASSET_VER}"></script>
<script src="assets/kk.js?v={ASSET_VER}"></script>
</body>
</html>
'''


def render_links(groups):
    out = []
    for title, items in groups:
        out.append(f'<h3 class="links-title">{esc(title)}</h3>')
        out.append('<div class="links-grid">')
        for item in items:
            label, url = item[0], item[1]
            kind = item[2] if len(item) > 2 else 'doc'
            ext = url.startswith('http')
            host = re.sub(r'^https?://(www\.)?', '', url).split('/')[0] if ext else 'raferalston.github.io'
            target = ' target="_blank" rel="noopener"' if ext or not url.endswith('_adv.html') else ''
            out.append(f'<a class="link-card" href="{esc(url)}"{target}><span class="ico">{LINK_ICONS.get(kind, "🔗")}</span>'
                       f'<span>{label}<small>{esc(host)}</small></span></a>')
        out.append('</div>')
    return '\n'.join(out)


def render_images(imgs, single=False):
    if not imgs:
        return ''
    cls = 'shots single' if single or len(imgs) == 1 else 'shots'
    items = []
    for im in imgs:
        src, alt = (im if isinstance(im, tuple) else (im, 'Иллюстрация к заданию'))
        items.append(f'<img class="zoomable" src="{esc(src)}" alt="{esc(alt)}" loading="lazy">')
    return f'<div class="{cls}">' + ''.join(items) + '</div>'


def render_task(lesson, t, n):
    key = f"{lesson['id']}:{t.get('key', n)}"
    tid = f"task-{n}"
    mode = t.get('mode', lesson.get('mode', 'html'))
    badges = [f'<span class="badge lvl-{t.get("level", 1)}">{LEVELS[t.get("level", 1)]}</span>']
    if t.get('new'):
        badges.append('<span class="badge new">новое</span>')
    if t.get('tests'):
        badges.append('<span class="badge auto">автопроверка</span>')
    if t.get('local'):
        badges.append('<span class="badge local">в VS Code</span>')
    parts = [f'<article class="task" id="{tid}" data-task="{esc(key)}">',
             '<div class="task-head">',
             f'<span class="task-num">{n}</span>',
             f'<div class="task-title"><h3>{t["title"]}</h3><div class="badges">{"".join(badges)}</div></div>',
             '</div>',
             '<div class="task-body">']
    if t.get('text'):
        parts.append(t['text'])
    for label, sample in t.get('examples', []):
        parts.append(f'<p class="sample-label">{esc(label)}</p><pre class="sample">{esc(sample.strip(chr(10)))}</pre>')
    parts.append(render_images(t.get('images')))
    if t.get('local'):
        parts.append('<p class="note info">🖥️ Это большое задание — делай его в <b>VS Code</b> на компьютере '
                     'и открывай страницу в браузере. Не забудь выложить результат на свой сайт на GitHub!</p>')
    if t.get('example'):
        parts.append(f'<p><a class="btn btn-ghost btn-sm" href="{esc(t["example"])}" target="_blank" rel="noopener">'
                     f'👀 {esc(t.get("example_label", "Открыть образец"))}</a></p>')
    demo = code_of(t.get('demo'))
    if demo:
        dmode = 'demo-js' if mode == 'js' else 'demo-html'
        parts.append(web_box(dmode, demo, fixture=code_of(t.get('demo_fixture'))))
    if t.get('hint'):
        parts.append(f'<details class="hint"><summary>Подсказка</summary><div class="inner">{t["hint"]}</div></details>')
    if t.get('editor', not t.get('local')):
        default = '<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <title>Моя страница</title>\n</head>\n<body>\n    \n</body>\n</html>\n' \
            if mode == 'html' else '// Напиши решение здесь\n'
        starter = code_of(t.get('starter')) or default
        parts.append(web_box(mode, starter, key=key, tests=t.get('tests'), fixture=code_of(t.get('fixture'))))
    # ответ
    ans_imgs = []
    for page in t.get('answer_pages', []):
        ans_imgs += answer_images(page)
    ans_imgs += t.get('answer_images', [])
    ans_code = code_of(t.get('answer'))
    ans_link = t.get('answer_link')
    if ans_imgs or ans_code or ans_link:
        inner = []
        if ans_code:
            inner.append(f'<pre class="code" data-solution>{esc(ans_code)}</pre>')
        for src in ans_imgs:
            inner.append(f'<img class="zoomable" src="{esc(src)}" alt="Решение задания" loading="lazy">')
        if ans_link:
            inner.append(f'<p><a href="{esc(ans_link)}" target="_blank" rel="noopener">Открыть готовую страницу с ответом ↗</a></p>')
        parts.append('<details class="answer"><summary>Показать ответ (сначала попробуй сам!)</summary>'
                     f'<div class="inner">{"".join(inner)}</div></details>')
    parts.append('</div>')
    parts.append('<div class="task-foot"><button class="done-btn" type="button" aria-pressed="false">'
                 '<span class="box"></span><span class="lbl">Отметить выполненным</span></button></div>')
    parts.append('</article>')
    return '\n'.join(parts), key, tid


def render_block(b):
    kind = b['type']
    if kind == 'html':
        return b['html']
    if kind == 'note':
        return f'<div class="note {b.get("cls", "")}"><p>{b["text"]}</p></div>'
    if kind == 'images':
        return render_images(b['images'], single=True)
    if kind == 'table':
        head_row = ''.join(f'<th>{h}</th>' for h in b['head'])
        rows = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in b['rows'])
        cap = f'<p class="table-cap">{b["caption"]}</p>' if b.get('caption') else ''
        return f'{cap}<div class="table-wrap"><table class="nice"><thead><tr>{head_row}</tr></thead><tbody>{rows}</tbody></table></div>'
    if kind == 'steps':
        items = []
        for s in b['steps']:
            if isinstance(s, dict):
                text, imgs, attrs, tattrs = s['text'], s.get('images', []), s.get('attrs', ''), s.get('title_attrs', '')
            else:
                text, imgs = (s if isinstance(s, tuple) else (s, []))
                attrs = tattrs = ''
            items.append(f'<li{" " + attrs if attrs else ""}><p{" " + tattrs if tattrs else ""}>{text}</p>{render_images(imgs, single=True)}</li>')
        return '<ol class="steps">' + ''.join(items) + '</ol>'
    if kind == 'code':
        return f'<pre class="code">{esc(code_of(b["code"]))}</pre>'
    if kind == 'sandbox':
        return web_box(b.get('mode', 'html'), code_of(b['code']), fixture=code_of(b.get('fixture')) if b.get('fixture') else None,
                       title='Песочница')
    raise ValueError(kind)


def course_of(lesson):
    return COURSES[lesson['course']][0]


def render_lesson(lesson, prev_l, next_l):
    body, toc, keys = [], [], []
    n = 0
    for sec in lesson['sections']:
        sid = sec.get('id') or f"sec-{len(toc)}"
        emoji = f'<span class="emoji">{sec["emoji"]}</span>' if sec.get('emoji') else ''
        body.append(f'<h2 class="sec-title" id="{sid}">{emoji}{sec["title"]}</h2>')
        toc.append(f'<a class="sec" href="#{sid}">{sec["title"]}</a>')
        for item in sec['items']:
            if item.get('type') == 'task':
                n += 1
                html_, key, tid = render_task(lesson, item, n)
                keys.append(key)
                body.append(html_)
                short = re.sub('<[^>]+>', '', item['title'])
                toc.append(f'<a href="#{tid}"><span class="n">{n}</span><span>{esc(short)}</span></a>')
            else:
                body.append(render_block(item))
    if lesson.get('links'):
        body.append('<h2 class="sec-title" id="links"><span class="emoji">🔗</span>Полезные ссылки</h2>')
        body.append(render_links(lesson['links']))
        toc.append('<a class="sec" href="#links">Полезные ссылки</a>')

    pager = ['<nav class="pager" aria-label="Соседние уроки">']
    if prev_l:
        pager.append(f'<a class="prev" href="{prev_l["file"]}"><small>← Предыдущий</small>Урок {prev_l["num"]}. {esc(prev_l["short"])}</a>')
    if next_l:
        pager.append(f'<a class="next" href="{next_l["file"]}"><small>Следующий →</small>Урок {next_l["num"]}. {esc(next_l["short"])}</a>')
    pager.append('</nav>')

    tasks = [i for s in lesson['sections'] for i in s['items'] if i.get('type') == 'task']
    chips = [f'<span class="chip">📋 Заданий: {n}</span>'] if n else []
    auto = sum(1 for i in tasks if i.get('tests'))
    new = sum(1 for i in tasks if i.get('new'))
    if auto:
        chips.append(f'<span class="chip">✅ С автопроверкой: {auto}</span>')
    if new:
        chips.append(f'<span class="chip">✨ Новых: {new}</span>')

    progress = ''
    if n:
        progress = ('<div class="side-card" data-lesson-progress><h4>Прогресс</h4><div class="bar"><i></i></div>'
                    '<span class="cnt">0 из 0</span> выполнено</div>')
    side = (f'<aside class="side">{progress}'
            f'<div class="side-card"><h4>Содержание</h4><nav class="toc">{"".join(toc)}</nav></div></aside>')

    title = f'Урок {lesson["num"]}. {lesson["short"]} — домашнее задание · КИДКОД'
    page = [head(title, re.sub('<[^>]+>', '', lesson.get('lead', lesson['title'])), lesson.get('head_extra', '')), header(),
            lesson.get('body_extra', ''),
            '<main>',
            '<section class="lesson-hero"><div class="wrap">',
            f'<div class="crumbs"><a href="index.html">Главная</a><span>›</span><a href="index.html#{lesson["course"]}">{course_of(lesson)}</a><span>›</span><span>Урок {lesson["num"]}</span></div>',
            f'<h1>{lesson["title"]}</h1>',
            f'<p class="lead">{lesson.get("lead", "")}</p>',
            f'<div class="chips">{"".join(chips)}</div>',
            '</div></section>',
            '<div class="wrap lesson-layout">', side,
            '<div class="content">', *body, *pager, '</div>',
            '</div>', '</main>', footer()]
    return '\n'.join(page), keys


def render_index(lessons):
    def card(l, i):
        tag = f'<span class="tag">+{l["new_count"]} новых</span>' if l.get('new_count') else ''
        meta = ''
        if l['task_count']:
            meta = f'<div class="meta"><div class="bar"><i></i></div><span class="cnt">0/{l["task_count"]}</span></div>'
        return (f'<a class="lesson-card c{i % 6 + 1}" href="{l["file"]}" data-lesson="{l["id"]}">{tag}'
                f'<span class="num">{l["num"]}</span><h3>{esc(l["short"])}</h3><p>{esc(l.get("about", ""))}</p>{meta}</a>')

    sections = []
    for ci, (cid, (name, about)) in enumerate(COURSES.items()):
        cards = [card(l, i + ci * 2) for i, l in enumerate(x for x in lessons if x['course'] == cid)]
        search = ('<input class="lesson-search" type="search" placeholder="Поиск по урокам…" aria-label="Поиск по урокам">'
                  if ci == 0 else '')
        sections += [f'<div class="section-head" id="{cid}"><div><h2>{name}</h2><p>{about}</p></div>{search}</div>',
                     '<div class="lesson-grid">', *cards, '</div>']

    total_tasks = sum(l['task_count'] for l in lessons)
    total_auto = sum(l['auto_count'] for l in lessons)

    return '\n'.join([
        head('Домашние задания по веб-дизайну · КИДКОД',
             'Домашние задания по HTML, CSS и JavaScript для учеников школы программирования КИДКОД: '
             'редактор кода с живым просмотром прямо в браузере и автопроверка.'),
        header(),
        '<main>',
        '<section class="hero"><div class="blob b1"></div><div class="blob b2"></div><div class="wrap hero-grid"><div>',
        '<span class="eyebrow">🌐 Школа программирования КИДКОД</span>',
        '<h1>Домашние задания по <span class="hl">веб-дизайну</span></h1>',
        f'<p class="lead">{total_tasks} заданий: от первого тега <code>&lt;h1&gt;</code> до flexbox, анимаций, '
        'JavaScript-игр и своего сайта-портфолио. Пиши код прямо на странице и сразу смотри результат. '
        f'{total_auto} задач проверяются автоматически.</p>',
        '<div class="hero-actions"><a class="btn btn-lg" href="lesson_1.html">Начать с урока 1 →</a>'
        '<a class="btn btn-ghost btn-lg" href="#basic">Все уроки</a></div>',
        '<div class="progress-card" data-total-progress><span>Твой прогресс:</span><div class="bar"><i></i></div>'
        '<b class="cnt">0 из 0</b><button class="link-btn reset-progress" type="button">сбросить</button></div>',
        '</div>',
        '<div class="hero-art" aria-hidden="true">'
        '<span class="c">&lt;!-- домашка на сегодня --&gt;</span><br>'
        '<span class="k">&lt;h1</span> <span class="f">class</span>=<span class="s">"hello"</span><span class="k">&gt;</span>Привет, мир!<span class="k">&lt;/h1&gt;</span><br><br>'
        '<span class="k">&lt;style&gt;</span><br>'
        '&nbsp;&nbsp;.hello { <span class="f">color</span>: <span class="s">hotpink</span>; }<br>'
        '<span class="k">&lt;/style&gt;</span><br><br>'
        '<span class="k">&lt;script&gt;</span><br>'
        '&nbsp;&nbsp;<span class="f">alert</span>(<span class="s">"Готово!"</span>)<br>'
        '<span class="k">&lt;/script&gt;</span></div>',
        '</div></section>',
        '<div class="wrap">',
        '<div class="features">',
        '<div class="feature"><div class="ico">👀</div><h3>Живой просмотр</h3><p>Пиши HTML и CSS — страница обновляется прямо во время набора.</p></div>',
        '<div class="feature"><div class="ico">✅</div><h3>Автопроверка</h3><p>Нажми «Проверить» — и сразу узнаешь, всё ли сделано верно.</p></div>',
        '<div class="feature"><div class="ico">💾</div><h3>Всё сохраняется</h3><p>Код и отметки о выполнении хранятся в твоём браузере.</p></div>',
        '<div class="feature"><div class="ico">🔑</div><h3>Ответы и подсказки</h3><p>Застрял? Открой подсказку или посмотри решение.</p></div>',
        '</div>',
        *sections,
        '</div>',
        '</main>',
        footer(),
    ])


def main():
    lessons = course.LESSONS
    course_map = []
    for i, l in enumerate(lessons):
        prev_l = lessons[i - 1] if i > 0 else None
        next_l = lessons[i + 1] if i + 1 < len(lessons) else None
        page, keys = render_lesson(l, prev_l, next_l)
        tasks = [it for s in l['sections'] for it in s['items'] if it.get('type') == 'task']
        for t in tasks:
            if t.get('tests') and not t.get('solution'):
                raise SystemExit(f"{l['file']}: у задания «{t['title']}» есть тесты, но нет solution")
        l['task_count'] = len(keys)
        l['auto_count'] = sum(1 for t in tasks if t.get('tests'))
        l['new_count'] = sum(1 for t in tasks if t.get('new'))
        with open(os.path.join(ROOT, l['file']), 'w', encoding='utf-8') as f:
            f.write(page)
        course_map.append({'id': l['id'], 'file': l['file'], 'tasks': keys})
        print(f"{l['file']}: {len(keys)} заданий ({l['auto_count']} с автопроверкой, {l['new_count']} новых)")

    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(render_index(lessons))
    with open(os.path.join(ROOT, 'assets', 'course-map.js'), 'w', encoding='utf-8') as f:
        f.write('// Сгенерировано tools/build.py — не редактировать вручную\n')
        f.write('window.KK_COURSE = ' + json.dumps(course_map, ensure_ascii=False, indent=1) + ';\n')
    total = sum(l['task_count'] for l in lessons)
    auto = sum(l['auto_count'] for l in lessons)
    print(f'index.html, assets/course-map.js — готово. Всего заданий: {total}, с автопроверкой: {auto}')


if __name__ == '__main__':
    main()
