"""Уроки 9–16: вёрстка, псевдоклассы, анимации, цвета, SVG, адаптивность, фреймворки, grid."""
from kk_helpers import task, sec, note, images, table, P, UL, dom, has, style, code_has  # noqa: F401
from lessons_1 import page, practice, W3C

# ------------------------------------------------------------------ Урок 9
L9_LAYOUT_START = page('''
<header>Шапка сайта</header>
<div class="middle">
    <aside>Меню</aside>
    <main>Основной контент</main>
</div>
<footer>Подвал</footer>
''', css='''
        body { margin: 0; font-family: sans-serif; }
        header, aside, main, footer { padding: 20px; color: white; }
        header { background-color: #6d4aff; }
        aside { background-color: #ff4d8d; }
        main { background-color: #19b8a6; }
        footer { background-color: #1f1b3d; }
''')

L9 = dict(
    id='l9', file='lesson_9_adv.html', num='9', course='basic',
    short='Вёрстка по макету',
    title='Вёрстка страниц по макету (wireframe)',
    about='Превращаем рисунок-макет в настоящую страницу',
    lead='Настоящие сайты верстают по макету. Учимся смотреть на рисунок и видеть в нём блоки и flex-контейнеры.',
    sections=[
        sec('Задания', emoji='📐', items=[
            note('Прежде чем писать код, <b>обведи на макете прямоугольники</b>: какие блоки стоят в ряд (flex), '
                 'а какие — друг под другом.', 'info'),
            task('Сайт по макету #1', P('Сверстай сайт по макету. Серые прямоугольники — места для картинок.'),
                 level=2, local=True, images=[('img/lesson_9_wireframe.png', 'Макет #1')], answer_link='lesson_9_answer_1.html'),
            task('Сайт по макету #2', P('Сверстай сайт по второму макету.'),
                 level=3, local=True, images=[('img/lesson_9_wireframe_2.png', 'Макет #2')], answer_link='lesson_9_answer_2.html'),
            task('Классический макет', P('Разложи блоки как у большинства сайтов:',
                UL('шапка <code>header</code> — сверху на всю ширину',
                   'под ней в ряд: меню <code>aside</code> слева (ширина <code>200px</code>) и контент <code>main</code> — всё остальное место',
                   'подвал <code>footer</code> — внизу на всю ширину')),
                level=2, new=True, starter=L9_LAYOUT_START,
                hint=P('Оберни <code>aside</code> и <code>main</code> в flex-контейнер (он уже есть — <code>.middle</code>). '
                       'Чтобы <code>main</code> занял остаток, дай ему <code>flex-grow: 1</code>.'),
                tests=[style('.middle', 'display', 'flex'), style('aside', 'width', '200px'),
                       dom('main справа от меню и занимает остаток', 'const a = $("aside").getBoundingClientRect(), m = $("main").getBoundingClientRect(); return (Math.abs(a.top - m.top) < 2 && m.left >= a.right - 1 && Math.abs(m.right - innerWidth) < 2) || "main должен стоять справа от aside и доходить до правого края";'),
                       dom('Шапка и подвал на всю ширину', 'return ["header", "footer"].every(s => Math.abs($(s).getBoundingClientRect().width - innerWidth) < 2) || "header и footer должны быть на всю ширину";')],
                solution=L9_LAYOUT_START.replace('main { background-color: #19b8a6; }', 'main { background-color: #19b8a6; flex-grow: 1; }')
                                        .replace('        footer {', '        .middle { display: flex; }\n        aside { width: 200px; }\n        footer {')),
        ]),
    ],
    links=[('Полезные ссылки', [('Создание макета сайта: wireframe.cc', 'https://wireframe.cc/', 'design')])],
)

# ------------------------------------------------------------------ Урок 10
L10 = dict(
    id='l10', file='lesson_10_adv.html', num='10', course='basic',
    short='Псевдоклассы и псевдоэлементы',
    title='Псевдоклассы и псевдоэлементы',
    about=':hover, :focus, :nth-child, ::before, ::after, формы',
    lead='Псевдоклассы меняют стиль элемента в особых состояниях (наведение, фокус, «каждый второй»), '
         'а псевдоэлементы добавляют на страницу украшения без лишних тегов.',
    sections=[
        sec('Задания', emoji='🪄', items=[
            task('Форма поиска Google', P(
                'Сделай форму поиска, как на картинке. Форма должна по-настоящему искать в Google: '
                '<code>action="https://google.com/search"</code>, у поля — <code>name="q"</code>. '
                'Огонёк 🔥 на кнопке добавь через псевдоэлемент <code>::before</code>.'),
                level=2, images=[('img/lesson_10_homework.png', 'Форма поиска')],
                tests=[has('form[action*="google.com/search"]', 'Форма отправляет запрос в Google'),
                       has('input[name="q"]', 'У поля name="q"'), has('button[type="submit"], input[type="submit"]', 'Есть кнопка отправки'),
                       dom('У кнопки есть ::before с содержимым', 'const b = $("button"); if (!b) return "Сделай кнопку тегом button"; const c = getComputedStyle(b, "::before").content; return (c && c !== "none" && c !== "normal") || "Добавь button::before { content: ... }";'),
                       dom('Скруглённые углы у поля', 'return parseFloat(css("input", "border-top-left-radius")) > 0 || "Добавь input border-radius";')],
                solution='file:lesson_10_homework.html'),
            task('Форма с эффектом :hover', P(
                'Сделай форму, как на образце: при наведении мыши она «приподнимается» и отбрасывает ступенчатую тень.'),
                level=2, example='lesson_10_hover.html',
                tests=[has('form'), has('label', 'Не меньше 2 подписей', min=2), has('input', 'Не меньше 2 полей', min=2),
                       dom('Есть правило form:hover', 'return !!rule(/form:hover/) || "Добавь form:hover";'),
                       dom('При наведении форма сдвигается или получает тень', 'const r = rule(/form:hover/); return (r && (r.style.transform || r.style.boxShadow)) ? true : "Добавь в form:hover transform или box-shadow";')],
                solution='file:lesson_10_hover.html'),
            task('Таблица-зебра', P(
                'Сделай так, чтобы <b>каждая чётная</b> строка таблицы была серой (<code>#eeeeee</code>). '
                'Используй псевдокласс <code>tr:nth-child(even)</code>. А при наведении на строку пусть она становится жёлтой.'),
                level=1, new=True,
                starter=page('<table>\n    <tr><th>Игрок</th><th>Очки</th></tr>\n' +
                             '\n'.join(f'    <tr><td>{n}</td><td>{p}</td></tr>' for n, p in
                                       [('Аня', 120), ('Петя', 95), ('Лиза', 88), ('Миша', 70), ('Оля', 64)]) + '\n</table>', css='''
        table { border-collapse: collapse; font-family: sans-serif; }
        th, td { padding: 8px 20px; border: 1px solid #ccc; }
'''),
                tests=[style('tr:nth-child(2)', 'background-color', '#eeeeee', 'Вторая строка серая'),
                       style('tr:nth-child(4)', 'background-color', '#eeeeee', 'Четвёртая строка серая'),
                       dom('Нечётные строки не серые', 'return !cssIs("tr:nth-child(3)", "background-color", "#eeeeee") || "Третья строка не должна быть серой";'),
                       dom('Есть правило tr:hover', 'return !!rule(/tr:hover/) || "Добавь tr:hover";')],
                solution=page('<table>\n    <tr><th>Игрок</th><th>Очки</th></tr>\n' +
                              '\n'.join(f'    <tr><td>{n}</td><td>{p}</td></tr>' for n, p in
                                        [('Аня', 120), ('Петя', 95), ('Лиза', 88), ('Миша', 70), ('Оля', 64)]) + '\n</table>', css='''
        table { border-collapse: collapse; font-family: sans-serif; }
        th, td { padding: 8px 20px; border: 1px solid #ccc; }
        tr:nth-child(even) { background-color: #eeeeee; }
        tr:hover { background-color: yellow; }
''')),
            task('Звёздочка для обязательных полей', P(
                'Подписям с классом <code>.required</code> добавь красную звёздочку <b>*</b> в конце с помощью '
                'псевдоэлемента <code>::after</code> (<code>content: " *"</code>).'),
                level=2, new=True,
                starter=page('''
<form>
    <label class="required">Имя</label><br>
    <input type="text"><br>
    <label>Город</label><br>
    <input type="text"><br>
    <label class="required">Почта</label><br>
    <input type="email">
</form>
''', css='        /* Пиши стили здесь */\n'),
                tests=[dom('У .required есть звёздочка', 'return getComputedStyle($(".required"), "::after").content.includes("*") || "Добавь .required::after { content: \\" *\\" }";'),
                       dom('Звёздочка красная', 'return cssIs(".required", "color", "red", "::after") || "Сделай звёздочку красной (color: red)";'),
                       dom('У обычной подписи звёздочки нет', 'return !getComputedStyle($$("label")[1], "::after").content.includes("*") || "Звёздочка должна быть только у .required";')],
                solution=page('''
<form>
    <label class="required">Имя</label><br>
    <input type="text"><br>
    <label>Город</label><br>
    <input type="text"><br>
    <label class="required">Почта</label><br>
    <input type="email">
</form>
''', css='''
        .required::after { content: " *"; color: red; }
''')),
            task('Подсветка поля в фокусе', P(
                'Когда пользователь щёлкает по полю ввода, пусть у него появляется рамка цвета <code>#6d4aff</code>. '
                'Используй псевдокласс <code>:focus</code>. Проверь, щёлкнув по полю в результате.'),
                level=1, new=True,
                starter=page('<input type="text" placeholder="Щёлкни по мне">', css='''
        input { padding: 10px; font-size: 18px; border: 2px solid #ccc; border-radius: 8px; outline: none; }
'''),
                tests=[dom('Есть правило input:focus', 'return !!rule(/input:focus/) || "Добавь input:focus";'),
                       dom('В фокусе меняется рамка', 'const r = rule(/input:focus/); if (!r) return "Нет input:focus"; const c = r.style.borderColor || r.style.borderTopColor || r.style.outlineColor; return (c && norm("color", c) === norm("color", "#6d4aff")) || "Цвет рамки в фокусе должен быть #6d4aff";')],
                solution=page('<input type="text" placeholder="Щёлкни по мне">', css='''
        input { padding: 10px; font-size: 18px; border: 2px solid #ccc; border-radius: 8px; outline: none; }
        input:focus { border-color: #6d4aff; }
''')),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Псевдоклассы', 'https://developer.mozilla.org/ru/docs/Web/CSS/%D0%9F%D1%81%D0%B5%D0%B2%D0%B4%D0%BE-%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D1%8B', 'read'),
            ('Псевдоэлементы', 'https://developer.mozilla.org/ru/docs/Web/CSS/Pseudo-elements', 'read'),
        ]),
        practice('Где потренироваться',
                 *[(f'Псевдоклассы #{i}', f'{W3C}pseudo_classes{i}') for i in range(1, 5)],
                 *[(f'Псевдоэлементы #{i}', f'{W3C}pseudo_elements{i}') for i in range(1, 4)],
                 *[(f'Transitions #{i}', f'{W3C}css3_transitions{i}') for i in range(1, 6)]),
    ],
)

# ------------------------------------------------------------------ Урок 11
L11 = dict(
    id='l11', file='lesson_11_adv.html', num='11', course='basic',
    short='Анимация в CSS',
    title='Анимация в CSS',
    about='@keyframes, animation, linear-gradient',
    lead='Заставляем элементы двигаться, пульсировать и вращаться без единой строчки JavaScript.',
    sections=[
        sec('Задания', emoji='🎬', items=[
            note('<b>Шпаргалка:</b> сначала описываем анимацию: <code>@keyframes имя { from {…} to {…} }</code>, '
                 'потом подключаем её к элементу: <code>animation: имя 2s infinite;</code>', 'info'),
            task('Навигационный слайдер', P('Сделай меню из трёх пунктов: при наведении пункт плавно расширяется.'),
                 level=2, example='lesson_11_homework.html',
                 tests=[has('.navbar > *', 'В меню не меньше 3 пунктов', min=3), style('.navbar', 'flex-direction', 'column'),
                        dom('Есть правило :hover для пунктов', 'return !!rule(/:hover/, "width") || "Добавь пунктам :hover с новой шириной";'),
                        dom('Переход плавный', 'return parseFloat(css(".navbar > *", "transition-duration")) > 0 || "Добавь пунктам transition";')],
                 solution='file:lesson_11_homework.html'),
            task('Анимация «Привет мир!»', P('Сделай надпись, которая при загрузке страницы вырастает и получает фон.'),
                 level=2, example='lesson_11_homework_2.html',
                 tests=[dom('Есть @keyframes', 'return keyframes().length > 0 || "Опиши анимацию через @keyframes";'),
                        dom('Анимация подключена к элементу', 'return $$("body *").some(e => getComputedStyle(e).animationName !== "none") || "Подключи анимацию свойством animation";'),
                        dom('Анимация останавливается в конце (forwards)', 'return $$("body *").some(e => getComputedStyle(e).animationFillMode === "forwards") || "Добавь animation-fill-mode: forwards";')],
                 solution='file:lesson_11_homework_2.html'),
            task('Летающие шарики', P('Сделай шесть шариков, которые летят через экран с разной скоростью и задержкой.'),
                 level=3, example='lesson_11_homework_3.html',
                 hint=P('У каждого шарика своя длительность и задержка: <code>span:nth-child(2) { animation: fly 12s 1.75s infinite; }</code>'),
                 tests=[has('span', 'Не меньше 6 шариков', min=6),
                        dom('Шарики анимированы бесконечно', 'return $$("span").every(e => getComputedStyle(e).animationIterationCount === "infinite") || "Все шарики должны летать бесконечно (infinite)";'),
                        dom('У шариков разная длительность', 'return new Set($$("span").map(e => getComputedStyle(e).animationDuration)).size >= 3 || "Сделай шарикам разную длительность анимации";'),
                        style('span', 'border-top-left-radius', '50%', 'Шарики круглые')],
                 solution='file:lesson_11_homework_3.html'),
            task('Бьющееся сердце', P(
                'Сделай сердечко ❤️, которое бесконечно «бьётся»: увеличивается до <code>scale(1.3)</code> и обратно. '
                'Назови анимацию <code>beat</code>, длительность — <code>1s</code>.'),
                level=1, new=True,
                starter=page('<div class="heart">❤️</div>', css='''
        body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .heart { font-size: 100px; }
'''),
                tests=[dom('Есть @keyframes beat', 'return keyframes().some(k => k.name === "beat") || "Не нашёл @keyframes beat";'),
                       style('.heart', 'animation-name', 'beat'), style('.heart', 'animation-duration', '1s'),
                       style('.heart', 'animation-iteration-count', 'infinite'),
                       dom('Внутри анимации есть scale', 'const k = keyframes().find(k => k.name === "beat"); return (k && /scale/.test(k.cssText)) || "Используй transform: scale(...) внутри @keyframes";')],
                solution=page('<div class="heart">❤️</div>', css='''
        body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .heart { font-size: 100px; animation: beat 1s infinite; }
        @keyframes beat {
            0% { transform: scale(1); }
            50% { transform: scale(1.3); }
            100% { transform: scale(1); }
        }
''')),
            task('Спиннер загрузки', P(
                'Сделай круглый индикатор загрузки: блок <code>.loader</code> с рамкой, у которой одна сторона цветная, '
                'бесконечно вращается (<code>rotate(360deg)</code>) с равномерной скоростью (<code>linear</code>).'),
                level=2, new=True,
                starter=page('<div class="loader"></div>', css='''
        .loader {
            width: 60px;
            height: 60px;
            border: 8px solid #eee;
            border-top-color: #6d4aff;
            border-radius: 50%;
        }
'''),
                tests=[dom('Есть анимация вращения', 'return keyframes().some(k => /rotate/.test(k.cssText)) || "Опиши @keyframes с transform: rotate(360deg)";'),
                       style('.loader', 'animation-iteration-count', 'infinite'), style('.loader', 'animation-timing-function', 'linear')],
                solution=page('<div class="loader"></div>', css='''
        .loader {
            width: 60px;
            height: 60px;
            border: 8px solid #eee;
            border-top-color: #6d4aff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
''')),
            task('Градиентный фон', P(
                'Сделай у <code>body</code> фон-градиент из двух цветов с помощью <code>linear-gradient()</code>, '
                'а у кнопки <code>.btn</code> — градиент слева направо (<code>to right</code>).'),
                level=1, new=True,
                starter=page('<h1>Градиенты</h1>\n<button class="btn">Красивая кнопка</button>', css='''
        body { height: 100vh; margin: 0; font-family: sans-serif; }
        .btn { border: 0; color: white; padding: 16px 32px; font-size: 18px; border-radius: 30px; }
'''),
                tests=[dom('У body градиент', 'return /linear-gradient/.test(css("body", "background-image")) || "Задай body background: linear-gradient(...)";'),
                       dom('У кнопки градиент слева направо', 'return /linear-gradient\\((to right|90deg)/.test(css(".btn", "background-image")) || "Сделай у .btn linear-gradient(to right, ...)";')],
                solution=page('<h1>Градиенты</h1>\n<button class="btn">Красивая кнопка</button>', css='''
        body { height: 100vh; margin: 0; font-family: sans-serif; background: linear-gradient(#ffd23f, #ff4d8d); }
        .btn { border: 0; color: white; padding: 16px 32px; font-size: 18px; border-radius: 30px;
               background: linear-gradient(to right, #6d4aff, #19b8a6); }
''')),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Анимация в CSS', 'https://developer.mozilla.org/ru/docs/Web/CSS/animation', 'read'),
            ('Как установить картинку на фон', 'https://developer.mozilla.org/ru/docs/Web/CSS/background-image', 'read'),
            ('Онлайн-редактор анимации #1', 'https://keyframes.app/animate/', 'tool'),
            ('Онлайн-редактор анимации #2', 'https://animista.net/', 'tool'),
            ('Пример современной анимации загрузки', 'assets/animation_example.html', 'lesson'),
            ('Свойство linear-gradient()', 'https://developer.mozilla.org/ru/docs/Web/CSS/linear-gradient', 'read'),
            ('Генератор градиентов', 'https://cssgradient.io/', 'tool'),
        ]),
        practice('Где потренироваться', *[(f'Анимация #{i}', f'{W3C}css3_animations{i}') for i in range(1, 7)]),
    ],
)

# ------------------------------------------------------------------ Урок 12
PALETTE = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']

L12 = dict(
    id='l12', file='lesson_12_adv.html', num='12', course='basic',
    short='Цвета в веб-дизайне',
    title='Цветовые палитры в веб-дизайне',
    about='HEX, RGB, HSL, прозрачность, готовые палитры',
    lead='Хороший сайт — это не только код, но и красивые цвета. Учимся подбирать палитру и записывать цвета по-разному.',
    sections=[
        sec('Задания', emoji='🌈', items=[
            task('Заполни таблицу CSS-свойств', P(
                'Скачай <a href="https://docs.google.com/spreadsheets/d/17tqfTcntuSlIiJL486Dr0agYHCUEYaAeacU57I7Pl_w/edit?usp=sharing" '
                'target="_blank" rel="noopener">таблицу</a> и заполни значения CSS-свойств.'),
                level=1, editor=False),
            task('Изучи сайты с удачными цветами', P(
                'Посмотри <a href="https://visme.co/blog/website-color-schemes/" target="_blank" rel="noopener">подборку сайтов с цветовыми решениями</a>. '
                'Выбери 3 понравившиеся палитры и подумай, какую возьмёшь для своего сайта.'),
                level=1, editor=False),
            task('138 CSS-заданий', P(
                'Прорешай упражнения на <a href="https://www.w3schools.com/css/exercise.asp" target="_blank" rel="noopener">w3schools</a> — '
                'хотя бы по одному на каждую тему, которую мы прошли.'),
                level=2, editor=False),
            task('Своя палитра', P(
                'Сделай полоску из пяти блоков <code>.color</code>, покрашенных в цвета палитры: ' +
                ', '.join(f'<code>{c}</code>' for c in PALETTE) + '. Внутри каждого блока напиши его HEX-код.'),
                level=1, new=True,
                starter=page('<div class="palette">\n' + '\n'.join('    <div class="color"></div>' for _ in PALETTE) + '\n</div>', css='''
        .palette { display: flex; }
        .color { flex: 1; height: 150px; color: white; font-family: monospace; padding: 10px; }
'''),
                tests=[style(f'.color:nth-child({i + 1})', 'background-color', c, f'Блок {i + 1} — {c}') for i, c in enumerate(PALETTE)] +
                      [dom('В блоках написаны коды', 'return $$(".color").every(e => /#[0-9a-f]{6}/i.test(e.textContent)) || "Напиши в каждом блоке его HEX-код";')],
                solution=page('<div class="palette">\n' + '\n'.join(f'    <div class="color" style="background-color: {c}">{c}</div>' for c in PALETTE) + '\n</div>', css='''
        .palette { display: flex; }
        .color { flex: 1; height: 150px; color: white; font-family: monospace; padding: 10px; }
''')),
            task('Один цвет — три записи', P(
                'Покрась три квадрата в <b>один и тот же</b> цвет, но запиши его тремя способами: '
                '<code>.hex</code> — HEX-кодом, <code>.rgb</code> — через <code>rgb()</code>, <code>.hsl</code> — через <code>hsl()</code>. '
                'Возьми цвет <code>#ff6347</code>.'),
                level=2, new=True,
                hint=P('Перевести цвет можно в DevTools: щёлкни по квадратику цвета с зажатым <kbd>Shift</kbd>. '
                       'Или воспользуйся любым онлайн-конвертером.'),
                starter=page('<div class="box hex">HEX</div>\n<div class="box rgb">RGB</div>\n<div class="box hsl">HSL</div>', css='''
        .box { width: 120px; height: 120px; display: inline-block; color: white; }
'''),
                tests=[style('.hex', 'background-color', '#ff6347'), style('.rgb', 'background-color', '#ff6347'),
                       style('.hsl', 'background-color', '#ff6347'), code_has(r'rgb\(', 'В коде есть rgb()'), code_has(r'hsl\(', 'В коде есть hsl()')],
                solution=page('<div class="box hex">HEX</div>\n<div class="box rgb">RGB</div>\n<div class="box hsl">HSL</div>', css='''
        .box { width: 120px; height: 120px; display: inline-block; color: white; }
        .hex { background-color: #ff6347; }
        .rgb { background-color: rgb(255, 99, 71); }
        .hsl { background-color: hsl(9, 100%, 64%); }
''')),
            task('Полупрозрачная плашка', P(
                'Положи на картинку плашку <code>.caption</code> с белым текстом и <b>полупрозрачным</b> чёрным фоном: '
                '<code>rgba(0, 0, 0, 0.5)</code>. Картинка должна просвечивать!'),
                level=2, new=True,
                starter=page('<div class="photo">\n    <div class="caption">Ночное небо</div>\n</div>', css='''
        .photo { width: 400px; height: 260px; background-image: url('img/night.jpg'); background-size: cover; position: relative; }
        .caption { position: absolute; bottom: 0; left: 0; right: 0; padding: 16px; font-size: 22px; }
'''),
                tests=[style('.caption', 'background-color', 'rgba(0, 0, 0, 0.5)'), style('.caption', 'color', 'white')],
                solution=page('<div class="photo">\n    <div class="caption">Ночное небо</div>\n</div>', css='''
        .photo { width: 400px; height: 260px; background-image: url('img/night.jpg'); background-size: cover; position: relative; }
        .caption { position: absolute; bottom: 0; left: 0; right: 0; padding: 16px; font-size: 22px;
                   color: white; background-color: rgba(0, 0, 0, 0.5); }
''')),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Готовые цветовые палитры #1', 'https://colorhunt.co/', 'design'),
            ('Готовые цветовые палитры #2', 'https://colorsinspo.com/', 'design'),
            ('Игра для изучения HEX-цветов', 'http://www.hexinvaders.com/', 'game'),
            ('Выбор цветовой палитры #1', 'https://www.canva.com/colors/color-wheel/', 'design'),
            ('Выбор цветовой палитры #2', 'https://paletton.com/', 'design'),
            ('Готовые цветовые решения для сайта', 'https://color.romanuke.com/', 'design'),
            ('4 рекомендации к выбору цвета', 'https://spyserp.com/ru/blog/website-colors-2018', 'read'),
        ]),
        practice('Где потренироваться', *[(f'Цвета #{i}', f'{W3C}css3_colors{i}') for i in range(1, 5)]),
    ],
)

# ------------------------------------------------------------------ Урок 13
L13 = dict(
    id='l13', file='lesson_13_adv.html', num='13', course='basic',
    short='Параллакс и SVG',
    title='Параллакс и SVG-графика',
    about='background-attachment: fixed, svg, circle, rect',
    lead='Делаем эффект глубины при прокрутке и рисуем векторную графику прямо в HTML.',
    sections=[
        sec('Задания', emoji='🌌', items=[
            task('Звездопад', P(
                'Создай сайт, как на анимации: фон с ночным небом стоит на месте при прокрутке (параллакс), '
                'а сверху падают звёзды. Картинки: <a href="img/night.jpg" target="_blank">img/night.jpg</a> и '
                '<a href="img/night_flip.jpg" target="_blank">img/night_flip.jpg</a>.'),
                level=3, images=[('img/l13_a1.gif', 'Пример')],
                tests=[dom('Есть фон с background-attachment: fixed', 'return $$("body *").some(e => getComputedStyle(e).backgroundAttachment === "fixed") || "Добавь блоку с фоном background-attachment: fixed";'),
                       dom('Фон растянут (cover)', 'return $$("body *").some(e => getComputedStyle(e).backgroundSize === "cover") || "Добавь background-size: cover";'),
                       has('.star', 'Не меньше 3 звёзд', min=3),
                       dom('Звёзды падают (анимация)', 'return $$(".star").every(e => getComputedStyle(e).animationName !== "none") || "Добавь звёздам анимацию";')],
                solution='file:lesson_13_homework.html'),
            task('SVG-смайлик', P(
                'Нарисуй смайлик тегом <code>&lt;svg width="200" height="200"&gt;</code>: жёлтое лицо и два глаза — '
                'это три <code>&lt;circle&gt;</code>, а улыбку сделай через <code>&lt;path&gt;</code> или <code>&lt;line&gt;</code>.'),
                level=2, new=True,
                starter=page('<svg width="200" height="200">\n    <circle cx="100" cy="100" r="90" fill="gold" />\n</svg>'),
                hint=P('Улыбка-дуга: <code>&lt;path d="M 60 120 Q 100 160 140 120" stroke="black" stroke-width="6" fill="none" /&gt;</code>'),
                tests=[has('svg'), has('svg circle', 'Не меньше 3 кругов', min=3), has('svg path, svg line, svg polyline', 'Есть улыбка (path или line)')],
                solution=page('''
<svg width="200" height="200">
    <circle cx="100" cy="100" r="90" fill="gold" />
    <circle cx="70" cy="80" r="12" fill="black" />
    <circle cx="130" cy="80" r="12" fill="black" />
    <path d="M 60 120 Q 100 160 140 120" stroke="black" stroke-width="6" fill="none" />
</svg>
''')),
            task('Параллакс-блок', P(
                'Сделай блок <code>.parallax</code> высотой <code>400px</code> с картинкой <code>img/night.jpg</code> на фоне. '
                'Фон должен стоять на месте при прокрутке (<code>background-attachment: fixed</code>) и заполнять блок '
                '(<code>background-size: cover</code>). Прокрути результат!'),
                level=1, new=True,
                starter=page('<p class="text">Прокручивай вниз...</p>\n<div class="parallax"></div>\n<p class="text">А теперь вверх!</p>', css='''
        body { margin: 0; font-family: sans-serif; }
        .text { height: 400px; font-size: 30px; padding: 20px; }
'''),
                tests=[style('.parallax', 'height', '400px'), style('.parallax', 'background-attachment', 'fixed'),
                       style('.parallax', 'background-size', 'cover'),
                       dom('Фон — картинка night.jpg', 'return /night\\.jpg/.test(css(".parallax", "background-image")) || "Добавь background-image: url(\'img/night.jpg\')";')],
                solution=page('<p class="text">Прокручивай вниз...</p>\n<div class="parallax"></div>\n<p class="text">А теперь вверх!</p>', css='''
        body { margin: 0; font-family: sans-serif; }
        .text { height: 400px; font-size: 30px; padding: 20px; }
        .parallax { height: 400px; background-image: url('img/night.jpg'); background-attachment: fixed; background-size: cover; background-position: center; }
''')),
        ]),
        sec('Полезные генераторы SVG', emoji='🛠️', items=[
            note('<a href="https://getwaves.io/" target="_blank" rel="noopener">Волны</a> · '
                 '<a href="https://icomoon.io/app/#/select" target="_blank" rel="noopener">Иконки</a> · '
                 '<a href="https://editor.method.ac/" target="_blank" rel="noopener">Редактор SVG</a> · '
                 '<a href="https://www.smashingmagazine.com/2015/05/why-the-svg-filter-is-awesome/" target="_blank" rel="noopener">Возможности SVG-фильтров</a>', 'info'),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Как создать параллакс-эффект', 'https://www.w3schools.com/howto/howto_css_parallax.asp', 'read'),
            ('Всё о SVG', 'https://developer.mozilla.org/ru/docs/Web/SVG', 'read'),
            ('Элементы SVG', 'https://developer.mozilla.org/en-US/docs/Web/SVG/Element', 'read'),
            ('11 параллакс-эффектов', 'https://freefrontend.com/css-parallax/', 'read'),
        ]),
        ('Где потренироваться', [('Изучаем flex с помощью игры', 'http://www.flexboxdefense.com/', 'game')]),
    ],
)

# ------------------------------------------------------------------ Урок 14
L14_CARDS = '<div class="cards">\n' + '\n'.join(f'    <div class="card">{e}</div>' for e in '🐶🐱🐰') + '\n</div>'
L14_CARDS_CSS = '''
        body { margin: 0; font-family: sans-serif; }
        .card { flex: 1; font-size: 80px; text-align: center; padding: 30px; margin: 10px; background-color: #efeaff; border-radius: 16px; }
'''

L14 = dict(
    id='l14', file='lesson_14_adv.html', num='14', course='basic',
    short='Адаптивный дизайн',
    title='Адаптивный дизайн и медиазапросы',
    about='@media, flex-wrap, meta viewport',
    lead='Сайт должен хорошо выглядеть и на большом мониторе, и на телефоне. Для этого есть медиазапросы.',
    sections=[
        sec('Задания', emoji='📱', items=[
            note('Проверить адаптивность можно в DevTools: <kbd>F12</kbd> → значок телефона (<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>M</kbd>). '
                 'А здесь — нажми <b>⤢</b> над редактором и меняй ширину окна.', 'info'),
            task('Адаптивный сайт #1', P(
                'Создай сайт, как на анимации: при уменьшении экрана блоки перестраиваются. '
                '<a href="https://i.gyazo.com/98231cdb9232f80bf65f38475e9aadee.mp4" target="_blank" rel="noopener">Смотреть видео</a>.'),
                level=2, local=True, images=[('img/resp.gif', 'Сайт #1')]),
            task('Адаптивный сайт #2', P(
                'Создай второй сайт, как на анимации. '
                '<a href="https://i.gyazo.com/afe8e236a26e6e1e0f688812d861651d.mp4" target="_blank" rel="noopener">Смотреть видео</a>.'),
                level=3, local=True, images=[('img/resp2.gif', 'Сайт #2')]),
            task('Карточки: в ряд или столбиком', P(
                'Три карточки стоят в ряд (<code>display: flex</code> у <code>.cards</code>). Добавь медиазапрос: '
                'если ширина экрана <b>меньше 600px</b> — <code>@media (max-width: 600px)</code> — карточки должны встать '
                'столбиком (<code>flex-direction: column</code>).'),
                level=2, new=True, starter=page(L14_CARDS, css=L14_CARDS_CSS.rstrip() + '\n        .cards { display: flex; }\n'),
                tests=[style('.cards', 'display', 'flex'),
                       dom('Есть @media (max-width: 600px)', 'return media().some(m => /max-width:\\s*600px/.test(m.conditionText || m.media.mediaText)) || "Добавь @media (max-width: 600px)";'),
                       dom('В медиазапросе карточки встают столбиком', 'const m = media().find(m => /max-width:\\s*600px/.test(m.conditionText || m.media.mediaText)); return (m && /flex-direction:\\s*column/.test(m.cssText)) || "Внутри @media сделай .cards { flex-direction: column }";'),
                       dom('На широком экране карточки в ряд', 'const r = $$(".card").map(e => e.getBoundingClientRect().top); return r.every(t => Math.abs(t - r[0]) < 2) || "На широком экране карточки должны стоять в одну строку";')],
                solution=page(L14_CARDS, css=L14_CARDS_CSS.rstrip() + '''
        .cards { display: flex; }
        @media (max-width: 600px) {
            .cards { flex-direction: column; }
        }
''')),
            task('Картинка не вылезает за экран', P(
                'Большая картинка вылезает за край экрана на телефоне. Исправь: у картинки должно быть '
                '<code>max-width: 100%</code>, а в <code>&lt;head&gt;</code> добавь тег '
                '<code>&lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;</code>.'),
                level=1, new=True,
                starter=page('<h1>Моё путешествие</h1>\n<img src="img/night.jpg" alt="Ночное небо">', css='        body { font-family: sans-serif; }\n'),
                tests=[has('meta[name="viewport"]', 'Есть meta viewport'), style('img', 'max-width', '100%'),
                       dom('Картинка не шире страницы', 'return $("img").getBoundingClientRect().right <= innerWidth || "Картинка вылезает за край";')],
                solution=page('<h1>Моё путешествие</h1>\n<img src="img/night.jpg" alt="Ночное небо">', css='''
        body { font-family: sans-serif; }
        img { max-width: 100%; }
''').replace('    <meta charset="UTF-8">', '    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">')),
            task('Прячем меню на телефоне', P(
                'На экранах уже <code>768px</code> меню <code>.menu</code> должно прятаться (<code>display: none</code>), '
                'а вместо него показываться кнопка-бургер <code>.burger</code> (на широком экране она спрятана).'),
                level=3, new=True,
                starter=page('''
<header>
    <b>Логотип</b>
    <nav class="menu"><a href="#">Главная</a> <a href="#">О нас</a> <a href="#">Контакты</a></nav>
    <button class="burger">☰</button>
</header>
''', css='''
        header { display: flex; justify-content: space-between; align-items: center; padding: 16px; background-color: #eee; }
        .burger { display: none; font-size: 24px; }
'''),
                tests=[dom('На широком экране меню видно, а бургер спрятан', 'return (css(".menu", "display") !== "none" && css(".burger", "display") === "none") || "На широком экране должно быть видно меню, а бургер спрятан";'),
                       dom('Есть @media (max-width: 768px)', 'return media().some(m => /max-width:\\s*768px/.test(m.conditionText || m.media.mediaText)) || "Добавь @media (max-width: 768px)";'),
                       dom('В медиазапросе меню прячется, а бургер появляется', 'const m = media().find(m => /max-width:\\s*768px/.test(m.conditionText || m.media.mediaText)); if (!m) return "Нет медиазапроса"; const t = m.cssText; return (/\\.menu[^}]*display:\\s*none/.test(t) && /\\.burger[^}]*display:\\s*(block|inline-block|flex|inline)/.test(t)) || "Внутри @media спрячь .menu и покажи .burger";')],
                solution=page('''
<header>
    <b>Логотип</b>
    <nav class="menu"><a href="#">Главная</a> <a href="#">О нас</a> <a href="#">Контакты</a></nav>
    <button class="burger">☰</button>
</header>
''', css='''
        header { display: flex; justify-content: space-between; align-items: center; padding: 16px; background-color: #eee; }
        .burger { display: none; font-size: 24px; }
        @media (max-width: 768px) {
            .menu { display: none; }
            .burger { display: block; }
        }
''')),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Отзывчивый веб-дизайн', 'https://www.w3schools.com/css/css_rwd_mediaqueries.asp', 'read'),
            ('Медиазапросы', 'https://developer.mozilla.org/ru/docs/Web/CSS/Media_Queries/Using_media_queries', 'read'),
            ('Примеры хорошего веб-дизайна', 'https://www.invisionapp.com/inside-design/examples-responsive-web-design/', 'design'),
        ]),
    ],
)

# ------------------------------------------------------------------ Урок 15
BS = 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'

L15 = dict(
    id='l15', file='lesson_15_adv.html', num='15', course='basic',
    short='CSS-фреймворки: Bootstrap',
    title='CSS-фреймворки: Bootstrap',
    about='Готовые классы, сетка, кнопки, темы Bootswatch',
    lead='Фреймворк — это набор готовых стилей. Подключаешь одну строчку — и получаешь красивые кнопки, сетку и формы.',
    sections=[
        sec('Задания', emoji='🧱', items=[
            task('Познакомься с Bootstrap', P(
                'Открой сайт <a href="https://getbootstrap.com/" target="_blank" rel="noopener">getbootstrap.com</a>, '
                'найди раздел <b>Components</b> и посмотри, какие готовые элементы там есть.',
                'Потом загляни в <a href="https://startbootstrap.com/themes/" target="_blank" rel="noopener">готовые макеты для Bootstrap</a> '
                'и <a href="https://www.bootstrapcdn.com/bootswatch/" target="_blank" rel="noopener">цветовые темы Bootswatch</a>: '
                'чтобы сменить тему, достаточно поменять ссылку на CSS-файл.'),
                level=1, editor=False, images=[('img/bootswatch.png', 'Ссылка на CSS-стиль')]),
            task('Страница на Bootstrap', P('Подключи Bootstrap и собери страницу из готовых классов:',
                UL(f'в <code>&lt;head&gt;</code> — <code>&lt;link rel="stylesheet" href="{BS}"&gt;</code>',
                   'всё содержимое — внутри <code>&lt;div class="container"&gt;</code>',
                   'кнопка с классами <code>btn btn-primary</code>',
                   'ряд <code>row</code> с тремя колонками <code>col</code>',
                   'цветная плашка <code>alert alert-success</code>')),
                level=2, new=True,
                tests=[has('link[href*="bootstrap"]', 'Bootstrap подключён'), has('.container'), has('.btn.btn-primary', 'Кнопка btn btn-primary'),
                       has('.row > .col', 'В ряду три колонки', min=3), has('.alert.alert-success', 'Плашка alert alert-success')],
                solution=page('''
<div class="container">
    <h1>Мой первый сайт на Bootstrap</h1>
    <div class="alert alert-success">Ура, Bootstrap подключён!</div>
    <div class="row">
        <div class="col">Колонка 1</div>
        <div class="col">Колонка 2</div>
        <div class="col">Колонка 3</div>
    </div>
    <button class="btn btn-primary">Нажми меня</button>
</div>
''').replace('    <title>', f'    <link rel="stylesheet" href="{BS}">\n    <title>')),
        ]),
    ],
    links=[
        ('Полезные ссылки', [
            ('Bootstrap', 'https://getbootstrap.com/', 'tool'),
            ('Цветовые решения для Bootstrap', 'https://www.bootstrapcdn.com/bootswatch/', 'design'),
            ('Готовые макеты для Bootstrap', 'https://startbootstrap.com/themes/', 'design'),
            ('CSS-фреймворки', 'https://proglib.io/p/css-frameworks'),
            ('Подробнее о фреймворках', 'https://merehead.com/ru/blog/css-frameworks-2019/'),
        ]),
        ('Что почитать', [('Зачем нужны фреймворки', 'https://webkyrs.info/page/chto-takoe-css-freimvorki-i-zachem-oni-nuzhny', 'read')]),
    ],
)

# ------------------------------------------------------------------ Урок 16
L16_AREAS = page('''
<div class="page">
    <header>Шапка</header>
    <aside>Меню</aside>
    <main>Контент</main>
    <footer>Подвал</footer>
</div>
''', css='''
        body { margin: 0; font-family: sans-serif; }
        .page > * { padding: 20px; color: white; font-size: 20px; }
        header { background-color: #6d4aff; }
        aside { background-color: #ff4d8d; }
        main { background-color: #19b8a6; height: 200px; }
        footer { background-color: #1f1b3d; }
''')

L16 = dict(
    id='l16', file='lesson_16_adv.html', num='16', course='basic',
    short='CSS Grid',
    title='Создаём сайт с помощью CSS Grid',
    about='display: grid, grid-template-columns, grid-template-areas',
    lead='Grid — сетка из строк и колонок. С ней сложные раскладки делаются в пару строк.',
    sections=[
        sec('Задания', emoji='🔲', items=[
            task('Сайт на grid по макету', P(
                'Сверстай сайт по картинке с помощью CSS Grid. Макет можно открыть в '
                '<a href="https://www.figma.com/file/7SfJlaPoNXv55g26YKXzFH/lesson-16-grid?node-id=0%3A1" target="_blank" rel="noopener">Figma</a> '
                'или скачать для <a href="img/mock.xd">Adobe XD</a>.'),
                level=3, local=True, images=[('img/lesson_16.png', 'Сайт на grid')]),
            task('Сетка 3 × 3', P(
                'Расставь 9 клеток <code>.cell</code> сеткой 3 на 3: у <code>.grid</code> — <code>display: grid</code>, '
                '<code>grid-template-columns: repeat(3, 1fr)</code> и промежутки <code>gap: 10px</code>.'),
                level=1, new=True,
                starter=page('<div class="grid">\n' + '\n'.join(f'    <div class="cell">{i}</div>' for i in range(1, 10)) + '\n</div>', css='''
        .cell { background-color: #ffd23f; font-size: 30px; text-align: center; padding: 20px; border-radius: 8px; }
'''),
                tests=[style('.grid', 'display', 'grid'), style('.grid', 'row-gap', '10px', '.grid { gap: 10px }'),
                       dom('По три клетки в ряд', 'const tops = $$(".cell").map(e => Math.round(e.getBoundingClientRect().top)); const rows = {}; tops.forEach(t => rows[t] = (rows[t] || 0) + 1); const c = Object.values(rows); return (c.length === 3 && c.every(x => x === 3)) || "Сейчас в рядах: " + c.join(", ");')],
                solution=page('<div class="grid">\n' + '\n'.join(f'    <div class="cell">{i}</div>' for i in range(1, 10)) + '\n</div>', css='''
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .cell { background-color: #ffd23f; font-size: 30px; text-align: center; padding: 20px; border-radius: 8px; }
''')),
            task('Раскладка через grid-template-areas', P(
                'Разложи страницу по областям: шапка сверху на всю ширину, ниже меню (<code>200px</code>) и контент, '
                'внизу подвал на всю ширину. Используй <code>grid-template-areas</code> и <code>grid-area</code>.'),
                level=2, new=True, starter=L16_AREAS,
                hint='<pre class="code">.page {\n    display: grid;\n    grid-template-columns: 200px 1fr;\n'
                     '    grid-template-areas:\n        "header header"\n        "aside  main"\n        "footer footer";\n}\n'
                     'header { grid-area: header; }</pre>',
                tests=[style('.page', 'display', 'grid'), code_has('grid-template-areas', 'Используется grid-template-areas'),
                       dom('Шапка и подвал на всю ширину', 'return ["header", "footer"].every(s => Math.abs($(s).getBoundingClientRect().width - $(".page").getBoundingClientRect().width) < 2) || "header и footer должны занимать всю ширину";'),
                       dom('Меню слева шириной 200px, контент справа', 'const a = $("aside").getBoundingClientRect(), m = $("main").getBoundingClientRect(); return (Math.abs(a.width - 200) < 2 && Math.abs(a.top - m.top) < 2 && m.left >= a.right - 1) || "aside (200px) должен стоять слева от main";')],
                solution=L16_AREAS.replace('        header { background-color: #6d4aff; }', '''        .page {
            display: grid;
            grid-template-columns: 200px 1fr;
            grid-template-areas:
                "header header"
                "aside main"
                "footer footer";
        }
        header { background-color: #6d4aff; grid-area: header; }''')
                                  .replace('aside { background-color: #ff4d8d; }', 'aside { background-color: #ff4d8d; grid-area: aside; }')
                                  .replace('main { background-color: #19b8a6; height: 200px; }', 'main { background-color: #19b8a6; height: 200px; grid-area: main; }')
                                  .replace('footer { background-color: #1f1b3d; }', 'footer { background-color: #1f1b3d; grid-area: footer; }')),
            task('Большая плитка', P(
                'В галерее из 6 плиток первая плитка <code>.big</code> должна занимать <b>две колонки и две строки</b>: '
                '<code>grid-column: span 2</code> и <code>grid-row: span 2</code>. У сетки 3 колонки по <code>100px</code> '
                'и строки по <code>100px</code>.'),
                level=3, new=True,
                starter=page('<div class="grid">\n    <div class="tile big">★</div>\n' + '\n'.join('    <div class="tile"></div>' for _ in range(5)) + '\n</div>', css='''
        .grid { display: grid; grid-template-columns: repeat(3, 100px); grid-auto-rows: 100px; gap: 8px; }
        .tile { background-color: #19b8a6; border-radius: 8px; }
        .big { background-color: #ff4d8d; font-size: 60px; color: white; display: flex; justify-content: center; align-items: center; }
'''),
                tests=[dom('Большая плитка шириной в две колонки', 'return Math.abs($(".big").getBoundingClientRect().width - 208) < 2 || "Ширина .big = " + $(".big").getBoundingClientRect().width + "px, а нужно 2 колонки (208px)";'),
                       dom('Большая плитка высотой в две строки', 'return Math.abs($(".big").getBoundingClientRect().height - 208) < 2 || "Высота .big = " + $(".big").getBoundingClientRect().height + "px";')],
                solution=page('<div class="grid">\n    <div class="tile big">★</div>\n' + '\n'.join('    <div class="tile"></div>' for _ in range(5)) + '\n</div>', css='''
        .grid { display: grid; grid-template-columns: repeat(3, 100px); grid-auto-rows: 100px; gap: 8px; }
        .tile { background-color: #19b8a6; border-radius: 8px; }
        .big { background-color: #ff4d8d; font-size: 60px; color: white; display: flex; justify-content: center; align-items: center;
               grid-column: span 2; grid-row: span 2; }
''')),
        ]),
        sec('Программы для макетов', emoji='🎨', items=[
            note('<a href="https://www.figma.com/" target="_blank" rel="noopener">Figma</a> и '
                 '<a href="https://www.adobe.com/products/xd.html" target="_blank" rel="noopener">Adobe XD</a> — удобные программы для создания макетов. '
                 'Потренироваться с grid можно в игре <a href="https://cssgridgarden.com/#ru" target="_blank" rel="noopener">CSS Grid Garden</a>.', 'info'),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Документация — CSS Grid', 'https://developer.mozilla.org/ru/docs/Web/CSS/CSS_Grid_Layout', 'read'),
            ('Всё о CSS Grid', 'https://learncssgrid.com/', 'read'),
            ('Grid или Flexbox?', 'http://htmlbook.ru/blog/css-grid-i-flexbox-sravnenie-na-praktike', 'read'),
        ]),
        ('Где потренироваться', [('CSS Grid Garden — тренажёр', 'https://cssgridgarden.com/#ru', 'game')]),
    ],
)

LESSONS = [L9, L10, L11, L12, L13, L14, L15, L16]
