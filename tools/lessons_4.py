"""Уроки 25–36: DOM и события, таймеры, ООП, canvas, игра, дизайн-проект."""
from kk_helpers import (task, sec, note, html, images, table, steps, P, UL,  # noqa: F401
                        dom, has, style, io, call, code_has, var_is, read_file)
from lessons_1 import page
from lessons_3 import js_lessons

CAPS = 'Всё, что написано ЗАГЛАВНЫМИ буквами, — заранее выбранный элемент'

# ------------------------------------------------------------------ Урок 25
L25_MOUSE = page('''
<h1>Поводи мышкой!</h1>
<script>
    let body = document.querySelector('body')
    body.addEventListener('mousemove', changeColor)

    function changeColor(event) {
        let w = window.innerWidth
        let h = window.innerHeight
        let mouseX = event.clientX / (w / 255)
        let mouseY = event.clientY / (h / 255)
        body.style.backgroundColor = 'rgb(' + mouseX + ',' + mouseY + ', 40)'
    }
</script>
''', css='''
        body { height: 100vh; margin: 0; overflow: hidden; display: flex; justify-content: center; align-items: center; }
        h1 { color: white; font-family: sans-serif; }
''', title='Цвет от мышки')

L25_BOXES_CSS = '''
        body { margin: 0; overflow-x: hidden; display: flex; flex-wrap: wrap; }
        div { width: 50%; height: 50vh; display: flex; justify-content: center; align-items: center;
              font-size: 2em; color: white; cursor: pointer; transition: all ease .25s; }
        .box1 { background-color: #28c7fa; }
        .box2 { background-color: #775ada; }
        .box3 { background-color: #002651; }
        .box4 { background-color: #ff304f; }
'''
L25_BOXES_HTML = '\n'.join(f'<div class="box{i}">Нажми на меня!</div>' for i in range(1, 5))
L25_BOXES = page(L25_BOXES_HTML + '''
<script>
    let boxes = document.getElementsByTagName('div')

    function boxClicked(event) {
        event.target.textContent = 'Больше не нажимай!'
        event.target.style.backgroundColor = 'tomato'
    }

    for (let i = 0; i < boxes.length; i++) {
        boxes[i].addEventListener('click', boxClicked)
    }
</script>
''', css=L25_BOXES_CSS, title='Клики по блокам')

L25_HELLO = page('''
<h1>
    <span>H</span><span>E</span><span>L</span><span>L</span><span>O</span>
</h1>
<script>
    let body = document.querySelector('body')
    let word = document.querySelectorAll('span')
    body.addEventListener('mousemove', changeColor)

    for (let i = 0; i < word.length; i++) {
        word[i].addEventListener('click', changeDirection)
    }

    function changeColor(event) {
        let r = event.clientX / (window.innerWidth / 255)
        let g = event.clientY / (window.innerHeight / 255)
        let b = 80
        for (let i = 0; i < word.length; i++) {
            word[i].style.color = 'rgb(' + r + ',' + g + ',' + b + ')'
            r += r * 0.25
            g += g * 0.25
            b += b * 0.05
        }
    }

    function changeDirection(event) {
        let element = event.target
        if (!element.style.borderBottom) {
            element.style.borderBottom = '15px solid red'
        } else {
            element.style.borderBottom = ''
        }
    }
</script>
''', css='''
        body { height: 100vh; margin: 0; overflow: hidden; display: flex; justify-content: center; align-items: center; }
        span { color: black; font-size: 5em; cursor: pointer; transition: border-bottom ease .15s; }
        span:hover { text-shadow: 1px 1px 0 black, 2px 2px 0 black, 3px 3px 0 black, 4px 4px 0 black; }
''', title='HELLO')

L25 = dict(
    id='l25', file='lesson_25_adv.html', num='25', course='js', mode='html',
    short='DOM, часть 2: события',
    title='Управление элементами на странице. DOM, часть 2',
    about='createElement, append, remove, addEventListener',
    lead='Страница начинает слушать пользователя: клики, движения мыши, нажатия клавиш. А мы создаём и удаляем элементы на лету.',
    sections=[
        sec('Свойства и методы DOM-дерева', emoji='🌳', items=[table(['Как вызвать', 'Что делает'], [
            ['<code>document.createElement(\'TAG\')</code>', 'Создание тега'],
            ['<code>ELEMENT.className</code>', 'Добавление класса к элементу'],
            ['<code>ELEMENT.id</code>', 'Добавление id к элементу'],
            ['<code>ELEMENT.setAttribute(\'NAME\', \'VALUE\')</code>', 'Добавление атрибута к элементу'],
            ['<code>document.createTextNode(\'TEXT\')</code>', 'Создание текста'],
            ['<code>ELEMENT.insertBefore(NEW, REFERENCE)</code>', 'Вставка элемента перед другим'],
            ['<code>ELEMENT.appendChild(NEW)</code>', 'Добавление элемента в структуру'],
            ['<code>ELEMENT.append(NEW)</code>', 'Добавление элемента в конец (после последнего потомка)'],
            ['<code>ELEMENT.removeChild(CHILD)</code>', 'Удаление дочернего элемента'],
            ['<code>ELEMENT.remove()</code>', 'Удаление элемента со страницы'],
            ['<code>ELEMENT.addEventListener(\'EVENT\', FUNCTION)</code>', 'Добавление «прослушки» события'],
        ], caption=CAPS)]),
        sec('Задания', emoji='🖱️', items=[
            note('В этом уроке пишем целую страницу: HTML, CSS и JavaScript в теге <code>&lt;script&gt;</code> перед <code>&lt;/body&gt;</code>. '
                 'Результат можно сразу потрогать мышкой.', 'info'),
            task('Цвет от положения мыши', P(
                'Создай страницу, которая меняет цвет фона в зависимости от положения курсора: '
                'по горизонтали меняется красный канал, по вертикали — зелёный.'),
                level=2, images=[('img/l25_q1.gif', 'Как работает')], answer_link='lesson_25_ans_1.html',
                tests=[dom('Фон меняется при движении мыши', 'fire("body", "mousemove", { clientX: 20, clientY: 20 }); const a = css("body", "background-color"); fire("body", "mousemove", { clientX: 900, clientY: 600 }); const b = css("body", "background-color"); return (a !== b) || "Цвет фона не меняется при движении мыши";'),
                       code_has(r"addEventListener\(\s*['\"]mousemove", 'Используется событие mousemove')],
                solution=L25_MOUSE),
            task('Клик меняет блок', P(
                'Сделай страницу из четырёх цветных блоков. При клике блок меняет текст и становится цвета <code>tomato</code>.'),
                level=2, images=[('img/l25_q3.gif', 'Как работает')], answer_link='lesson_25_ans_3.html',
                starter=page(L25_BOXES_HTML, css=L25_BOXES_CSS, title='Клики по блокам'),
                tests=[dom('После клика меняется текст', 'const d = $$("div")[1]; const t = d.textContent; d.click(); return d.textContent !== t || "Текст блока не изменился";'),
                       dom('После клика блок становится tomato', 'const d = $$("div")[2]; d.click(); await wait(350); return getComputedStyle(d).backgroundColor === norm("background-color", "tomato") || "Цвет блока после клика: " + getComputedStyle(d).backgroundColor;'),
                       dom('Остальные блоки не меняются', 'const d = $$("div")[0]; const t = d.textContent; $$("div")[3].click(); return d.textContent === t || "Клик по одному блоку не должен менять другие";')],
                solution=L25_BOXES),
            task('HELLO: мышь и клики', P(
                'Сделай слово HELLO из отдельных букв. При движении мыши буквы меняют цвет, а по клику буква подчёркивается '
                'красной линией (<code>border-bottom</code>); повторный клик убирает линию.'),
                level=3, images=[('img/l25_q4.gif', 'Как работает')], answer_link='lesson_25_ans_4.html',
                tests=[has('span', '5 букв в span', min=5),
                       dom('Буквы меняют цвет при движении мыши', 'const s = $$("span")[0]; fire("body", "mousemove", { clientX: 30, clientY: 30 }); const a = getComputedStyle(s).color; fire("body", "mousemove", { clientX: 800, clientY: 500 }); return getComputedStyle(s).color !== a || "Цвет букв не меняется";'),
                       dom('Клик подчёркивает букву', 'const s = $$("span")[1]; s.click(); return getComputedStyle(s).borderBottomStyle !== "none" || "После клика у буквы нет border-bottom";'),
                       dom('Повторный клик убирает линию', 'const s = $$("span")[2]; s.click(); s.click(); return getComputedStyle(s).borderBottomStyle === "none" || "После второго клика линия должна исчезнуть";')],
                solution=L25_HELLO),
            task('Игра «Виселица»', P('Создай страницу с игрой «Виселица»: слово загадано, игрок вводит буквы, открываются угаданные.'),
                 level=3, local=True, images=[('img/l25_q2.png', 'Виселица')], answer_link='lesson_25_ans_2.html'),
            task('Счётчик кликов', P(
                'При каждом нажатии на кнопку <code>#plus</code> число в <code>#count</code> увеличивается на 1, '
                'а кнопка <code>#reset</code> сбрасывает его в 0.'),
                level=1, new=True, mode='js',
                fixture='<h1 id="count">0</h1>\n<button id="plus">+1</button>\n<button id="reset">Сброс</button>',
                starter="let count = 0\nlet countText = document.querySelector('#count')\n",
                tests=[dom('Три клика — число 3', 'click("#plus"); click("#plus"); click("#plus"); return text("#count") === "3" || "После трёх кликов: " + text("#count");'),
                       dom('Сброс возвращает 0', 'click("#plus"); click("#reset"); return text("#count") === "0" || "После сброса: " + text("#count");'),
                       dom('После сброса счёт снова идёт с 1', 'click("#reset"); click("#plus"); return text("#count") === "1" || "После сброса и клика: " + text("#count");')],
                solution="let count = 0\nlet countText = document.querySelector('#count')\n\n"
                         "document.querySelector('#plus').addEventListener('click', function () {\n    count++\n    countText.textContent = count\n})\n\n"
                         "document.querySelector('#reset').addEventListener('click', function () {\n    count = 0\n    countText.textContent = count\n})\n"),
            task('Список дел', P('Сделай список дел:',
                UL('по кнопке <code>#add</code> текст из поля <code>#task</code> добавляется в список <code>#list</code> новым <code>&lt;li&gt;</code>',
                   'после добавления поле очищается',
                   'пустую задачу добавлять нельзя',
                   'клик по задаче удаляет её (<code>remove()</code>)')),
                level=2, new=True, mode='js',
                fixture='<input id="task" placeholder="Что нужно сделать?">\n<button id="add">Добавить</button>\n<ul id="list"></ul>',
                starter="let input = document.querySelector('#task')\nlet list = document.querySelector('#list')\n",
                tests=[dom('Задача добавляется', '$("#task").value = "Сделать домашку"; click("#add"); return (count("#list li") === 1 && text("#list li") === "Сделать домашку") || "В списке: " + $$("#list li").map(e => e.textContent).join(", ");'),
                       dom('Поле очищается', '$("#task").value = "Погулять"; click("#add"); return $("#task").value === "" || "Поле не очистилось";'),
                       dom('Пустая задача не добавляется', 'const n = count("#list li"); $("#task").value = ""; click("#add"); return count("#list li") === n || "Пустая задача добавилась";'),
                       dom('Клик по задаче удаляет её', '$("#task").value = "Удали меня"; click("#add"); const n = count("#list li"); $$("#list li").pop().click(); return count("#list li") === n - 1 || "Задача не удалилась по клику";')],
                solution="let input = document.querySelector('#task')\nlet list = document.querySelector('#list')\n\n"
                         "document.querySelector('#add').addEventListener('click', function () {\n    if (input.value === '') {\n        return\n    }\n"
                         "    let li = document.createElement('li')\n    li.textContent = input.value\n    li.addEventListener('click', function () {\n"
                         "        li.remove()\n    })\n    list.append(li)\n    input.value = ''\n})\n"),
            task('Тёмная тема', P(
                'Кнопка <code>#theme</code> включает и выключает тёмную тему: добавляет или убирает у <code>body</code> '
                'класс <code>dark</code> (<code>classList.toggle</code>). Стили для <code>.dark</code> уже есть.'),
                level=1, new=True, mode='js',
                fixture='<style>body { transition: .3s; font-family: sans-serif; } .dark { background-color: #1f1b3d; color: white; }</style>\n'
                        '<h1>Привет!</h1>\n<button id="theme">🌙 Сменить тему</button>',
                tests=[dom('Клик включает тёмную тему', 'click("#theme"); return document.body.classList.contains("dark") || "У body не появился класс dark";'),
                       dom('Второй клик выключает', 'click("#theme"); return !document.body.classList.contains("dark") || "Второй клик должен убрать класс dark";')],
                solution="let button = document.querySelector('#theme')\n\nbutton.addEventListener('click', function () {\n    document.body.classList.toggle('dark')\n})\n"),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Создание элемента', 'https://learn.javascript.ru/modifying-document#sozdanie-elementa', 'read'),
            ('Добавление элемента', 'https://learn.javascript.ru/modifying-document#metody-vstavki', 'read'),
            ('Удаление элемента', 'https://learn.javascript.ru/modifying-document#udalenie-uzlov', 'read'),
            ('Браузерные события', 'https://learn.javascript.ru/introduction-browser-events', 'read'),
            ('События мыши', 'https://learn.javascript.ru/mouse-clicks', 'read'),
            ('События клавиатуры', 'https://learn.javascript.ru/keyboard-events', 'read'),
            ('Отслеживание событий', 'https://developer.mozilla.org/ru/docs/Web/API/EventTarget/addEventListener', 'read'),
        ]),
        js_lessons(25),
    ],
)

# ------------------------------------------------------------------ Урок 26
L26_CLICKER = read_file('lesson_26_ans_1.html').replace('<script src="game.js"></script>',
                                                        '<script>\n' + read_file('game.js').strip() + '\n</script>')

L26_CURSOR = page('''
<div id="ball"></div>
<script>
    let ball = document.querySelector('#ball')
    let body = document.querySelector('body')

    document.addEventListener('mousemove', moveEvent)
    document.addEventListener('click', clickEvent)

    function moveEvent(event) {
        ball.style.top = event.pageY - ball.clientHeight / 2 + 'px'
        ball.style.left = event.pageX - ball.clientWidth / 2 + 'px'
    }

    function clickEvent(event) {
        let dot = document.createElement('div')
        dot.className = 'dot'
        dot.style.top = event.clientY + 'px'
        dot.style.left = event.clientX + 'px'
        body.append(dot)
    }
</script>
''', css='''
        body { height: 100vh; margin: 0; background-color: #f4fa9c; cursor: none; overflow: hidden; }
        #ball { width: 50px; height: 50px; position: fixed; top: 0; left: 0; background-color: #fc5185; border-radius: 50%; z-index: 2; }
        .dot { width: 50px; height: 50px; position: fixed; background-color: #ff004c; border-radius: 50%; transform: translate(-50%, -50%); }
''', title='Курсор-кружок')

L26_PARALLAX = page('''
<div class="parallax">
    <h1 id="text"><span>Text</span> <span>Parallax</span></h1>
    <div id="line"></div>
</div>
<div class="cont"></div>
<script>
    let wordOne = document.querySelector('#text span:nth-child(1)')
    let wordTwo = document.querySelector('#text span:nth-child(2)')
    let line = document.querySelector('#line')
    let linePosition = line.offsetLeft

    window.addEventListener('scroll', function () {
        let scrollY = window.scrollY
        wordOne.style.top = scrollY * 0.25 + 'px'
        wordTwo.style.top = -scrollY * 0.25 + 'px'
        line.style.left = linePosition + scrollY * 0.35 + 'px'
    })
</script>
''', css='''
        body { margin: 0; }
        .parallax { height: 100vh; background-color: #071e3d; display: flex; justify-content: center; align-items: center; position: relative; }
        .cont { height: 2000px; background-color: #278ea5; }
        h1 { color: white; font-size: 4em; font-family: 'Trebuchet MS', Arial, sans-serif; }
        span { position: relative; }
        #line { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400px; height: 10px; background-color: #feff89; }
''', title='Text parallax')

L26_PROGRESS_FIX = ('<div id="progress"></div>\n<h1>Очень длинная статья</h1>\n' +
                    '\n'.join(f'<p>Абзац {i}. Прокручивай страницу, чтобы полоска росла.</p>' for i in range(1, 61)) +
                    '\n<style>body { margin: 0; padding: 10px 20px; font-family: sans-serif; } '
                    '#progress { position: fixed; top: 0; left: 0; height: 6px; width: 0; background: linear-gradient(to right, #19b8a6, #6d4aff); }</style>')

L26 = dict(
    id='l26', file='lesson_26_adv.html', num='26', course='js', mode='html',
    short='DOM, часть 3: координаты',
    title='Управление элементами на странице. DOM, часть 3',
    about='Координаты мыши, прокрутка, размеры элементов',
    lead='Узнаём, где находится мышь, насколько прокручена страница и какого размера элементы — и используем это в эффектах.',
    sections=[
        sec('Методы для управления элементами', emoji='🌳', items=[table(['Как вызвать', 'Что делает'], [
            ['<a href="https://developer.mozilla.org/ru/docs/Web/Events" target="_blank" rel="noopener"><code>ELEMENT.addEventListener(\'EVENT\', FUNCTION)</code></a>', 'Добавление «прослушки» событий'],
            ['<code>ELEMENT.offsetTop</code>, <code>ELEMENT.offsetLeft</code>', 'Расстояние от элемента до края родителя'],
            ['<code>pageYOffset</code>, <code>pageXOffset</code>', 'На сколько пикселей прокручен документ'],
            ['<code>window.scrollY</code>, <code>window.scrollX</code>', 'То же самое, что pageYOffset'],
            ['<code>window.innerHeight</code>, <code>window.innerWidth</code>', 'Размер видимой части экрана'],
            ['<code>event.pageY</code>, <code>event.pageX</code>', 'Позиция курсора мыши'],
            ['<code>ELEMENT.clientHeight</code>, <code>ELEMENT.clientWidth</code>', 'Размер элемента'],
        ])]),
        sec('Задания', emoji='🎯', items=[
            task('Кликер', P(
                'Сделай игру-кликер: счёт растёт с каждым кликом, оставшееся число кликов уменьшается, '
                'каждые 5 кликов меняется цвет фона, а в конце появляется поздравление.'),
                level=2, images=[('img/l26_q1.gif', 'Кликер')], answer_link='lesson_26_ans_1.html',
                tests=[has('#clicker'), has('#count'),
                       dom('Клик увеличивает счёт', 'click("#clicker"); click("#clicker"); return text("#count") === "2" || "Счёт после двух кликов: " + text("#count");'),
                       dom('Каждые 5 кликов меняется фон', 'const a = css("body", "background-color"); for (let i = 0; i < 5; i++) click("#clicker"); await wait(350); return css("body", "background-color") !== a || "Фон не поменялся после 5 кликов";')],
                solution=L26_CLICKER),
            task('Курсор-кружок', P(
                'Замени курсор мыши на кружок <code>#ball</code>, который следует за мышью. '
                'При клике кружок оставляет след — новый кружок на месте клика.'),
                level=2, images=[('img/l26_q2.gif', 'Как работает')], answer_link='lesson_26_ans_2.html',
                tests=[has('#ball'),
                       dom('Кружок следует за мышью', 'fire("body", "mousemove", { clientX: 300, clientY: 200 }); await wait(30); const r = $("#ball").getBoundingClientRect(); return (Math.abs(r.left + r.width / 2 - 300) < 30 && Math.abs(r.top + r.height / 2 - 200) < 30) || "Кружок не переместился к мыши (300, 200)";'),
                       dom('Клик оставляет след', 'const n = document.body.querySelectorAll("*").length; fire("body", "click", { clientX: 100, clientY: 100 }); return document.body.querySelectorAll("*").length > n || "После клика на странице не появился новый элемент";'),
                       style('body', 'cursor', 'none', 'Обычный курсор спрятан')],
                solution=L26_CURSOR),
            task('Параллакс текста', P(
                'При прокрутке страницы одно слово уезжает вниз, другое — вверх, а линия — вправо.'),
                level=3, images=[('img/l26_q3.gif', 'Как работает')], answer_link='lesson_26_ans_3.html',
                tests=[dom('Слова сдвигаются при прокрутке', 'const s = $$("#text span"); const a = s.map(e => e.getBoundingClientRect().top - $("#text").getBoundingClientRect().top); scrollTo(0, 300); window.dispatchEvent(new Event("scroll")); await wait(50); const b = s.map(e => e.getBoundingClientRect().top - $("#text").getBoundingClientRect().top); scrollTo(0, 0); return (a[0] !== b[0] && a[1] !== b[1]) || "Слова не двигаются при прокрутке";'),
                       code_has(r"addEventListener\(\s*['\"]scroll", 'Используется событие scroll')],
                solution=L26_PARALLAX),
            task('Индикатор прокрутки', P(
                'Сверху страницы есть полоска <code>#progress</code>. Сделай так, чтобы при прокрутке её ширина показывала, '
                'какая часть статьи уже прочитана: вверху — 0%, в самом низу — 100%.'),
                level=3, new=True, mode='js', fixture=L26_PROGRESS_FIX,
                starter="let progress = document.querySelector('#progress')\n\nwindow.addEventListener('scroll', function () {\n    \n})\n",
                hint=P('Сколько всего можно прокрутить: <code>document.documentElement.scrollHeight - window.innerHeight</code>. '
                       'Процент: <code>window.scrollY / всего * 100</code>.'),
                tests=[dom('Внизу страницы полоска на всю ширину', 'scrollTo(0, document.documentElement.scrollHeight); window.dispatchEvent(new Event("scroll")); await wait(50); const w = $("#progress").getBoundingClientRect().width; scrollTo(0, 0); return Math.abs(w - innerWidth) < 3 || "Ширина полоски внизу: " + Math.round(w) + "px, а экран — " + innerWidth + "px";'),
                       dom('На середине — примерно половина', 'const max = document.documentElement.scrollHeight - innerHeight; scrollTo(0, max / 2); window.dispatchEvent(new Event("scroll")); await wait(50); const w = $("#progress").getBoundingClientRect().width; scrollTo(0, 0); return Math.abs(w - innerWidth / 2) < innerWidth * 0.05 || "На середине ширина полоски: " + Math.round(w) + "px";')],
                solution="let progress = document.querySelector('#progress')\n\nwindow.addEventListener('scroll', function () {\n"
                         "    let total = document.documentElement.scrollHeight - window.innerHeight\n"
                         "    progress.style.width = window.scrollY / total * 100 + '%'\n})\n"),
            task('Координаты мыши', P(
                'Показывай в блоке <code>#coords</code> координаты мыши в виде <b>X: 120, Y: 45</b> при каждом её движении.'),
                level=1, new=True, mode='js',
                fixture='<div id="coords">Подвигай мышкой</div>\n<style>body { height: 100vh; margin: 0; font: 30px monospace; display: flex; justify-content: center; align-items: center; }</style>',
                tests=[dom('Показываются координаты', 'fire("body", "mousemove", { clientX: 120, clientY: 45 }); return text("#coords") === "X: 120, Y: 45" || "Сейчас в #coords: " + text("#coords");'),
                       dom('Обновляются при движении', 'fire("body", "mousemove", { clientX: 7, clientY: 300 }); return text("#coords") === "X: 7, Y: 300" || "Сейчас в #coords: " + text("#coords");')],
                solution="let coords = document.querySelector('#coords')\n\ndocument.addEventListener('mousemove', function (event) {\n"
                         "    coords.textContent = 'X: ' + event.clientX + ', Y: ' + event.clientY\n})\n"),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Справочник по событиям', 'https://developer.mozilla.org/ru/docs/Web/Events', 'read'),
            ('Введение в браузерные события', 'https://learn.javascript.ru/introduction-browser-events', 'read'),
            ('Координаты', 'https://learn.javascript.ru/coordinates', 'read'),
        ]),
        js_lessons(26),
    ],
)

# ------------------------------------------------------------------ Урок 27
TIMERS = table(['Как вызвать', 'Что делает'], [
    ['<code>setTimeout(function, time, arguments)</code>', 'Вызвать функцию один раз через заданное время (в миллисекундах)'],
    ['<code>setInterval(function, time, arguments)</code>', 'Вызывать функцию снова и снова через заданный интервал'],
    ['<code>clearTimeout(NAME)</code>', 'Отменить однократный вызов'],
    ['<code>clearInterval(NAME)</code>', 'Остановить повторяющийся вызов'],
    ['<code>Math.random() * n</code>', 'Случайное число от 0 до n (не включительно)'],
], caption=CAPS)

L27 = dict(
    id='l27', file='lesson_27_adv.html', num='27', course='js', mode='js',
    short='Интерактивные программы',
    title='Интерактивные программы: таймеры и случайность',
    about='setTimeout, setInterval, Math.random, игры',
    lead='Добавляем в программы время и случайность — и получаем настоящие игры.',
    sections=[
        sec('Функции, которые пригодятся', emoji='⏱️', items=[TIMERS]),
        sec('Задания', emoji='🏴‍☠️', items=[
            task('Pirate Treasure — простой вариант', P('Создай игру «Сокровища пиратов», как на анимации.'),
                 level=3, local=True, images=[('img/l27_q1.gif', 'Pirate Treasure')], answer_link='pirate_treasure_3_easy.html'),
            task('Pirate Treasure — сложный вариант', P('Усложни игру: добавь пирата, который охотится за игроком.'),
                 level=3, local=True, images=[('img/l27_q2.gif', 'Pirate Treasure hard')], answer_link='pirate_treasure_3_hard.html'),
            note('Файлы для игры: <a href="img/map.jpg" download>карта</a>, <a href="img/treasure.png" download>сундук</a>, '
                 '<a href="img/adventurer.png" download>игрок</a>, <a href="img/pirate.png" download>пират</a>, '
                 '<a href="img/heart.png" download>сердце</a> (для следующего задания).', 'info'),
            task('Кнопка с сердечками', P(
                'Создай страницу с кнопкой, которая каждые 2 секунды «подпрыгивает», зазывая нажать. После нажатия за мышью '
                'летят сердечки (<code>img/heart.png</code>), которые исчезают через 1.8 секунды.'),
                level=3, mode='html', images=[('img/l27_q3.gif', 'Как работает')], answer_link='lesson_27_ans_3.html',
                tests=[has('button'),
                       dom('До нажатия сердечки не появляются', 'fire("body", "mousemove", { clientX: 100, clientY: 100 }); return count("span") === 0 || "Сердечки должны появляться только после нажатия";'),
                       dom('После нажатия за мышью появляются сердечки', 'click("button"); fire("body", "mousemove", { clientX: 200, clientY: 200 }); fire("body", "mousemove", { clientX: 210, clientY: 210 }); return count("span") >= 2 || "После нажатия и движения мыши сердечки не появились";'),
                       code_has(r'setTimeout\(', 'Используется setTimeout'), code_has(r'setInterval\(', 'Используется setInterval')],
                solution='file:lesson_27_ans_3.html'),
            task('Обратный отсчёт', P(
                'В заголовке <code>#timer</code> написано 5. Каждую секунду число уменьшается на 1, а когда дойдёт до 0 — '
                'вместо числа появляется <b>Пуск! 🚀</b> и таймер останавливается (<code>clearInterval</code>).'),
                level=2, new=True, fixture='<h1 id="timer">5</h1>\n<style>h1 { font: 80px sans-serif; text-align: center; }</style>',
                starter="let timer = document.querySelector('#timer')\nlet seconds = 5\n",
                tests=[dom('Сразу показано 5', 'return text("#timer") === "5" || "В начале должно быть 5, сейчас: " + text("#timer");'),
                       dom('Через секунду — 4', 'await wait(1000); return text("#timer") === "4" || "Через секунду: " + text("#timer");'),
                       code_has(r'setInterval\(', 'Используется setInterval'), code_has(r'clearInterval\(', 'Таймер останавливается clearInterval'),
                       code_has('Пуск', 'В конце появляется «Пуск! 🚀»')],
                solution="let timer = document.querySelector('#timer')\nlet seconds = 5\n\nlet id = setInterval(function () {\n    seconds--\n"
                         "    if (seconds === 0) {\n        timer.textContent = 'Пуск! 🚀'\n        clearInterval(id)\n    } else {\n        timer.textContent = seconds\n    }\n}, 1000)\n"),
            task('Игральный кубик', P(
                'При нажатии на кнопку <code>#roll</code> в блоке <code>#dice</code> появляется случайное целое число от <b>1 до 6</b>.'),
                level=1, new=True, fixture='<div id="dice">🎲</div>\n<button id="roll">Бросить кубик</button>\n<style>#dice { font-size: 80px; }</style>',
                hint=P('<code>Math.floor(Math.random() * 6) + 1</code> — случайное целое от 1 до 6.'),
                tests=[dom('Выпадают только числа от 1 до 6', 'for (let i = 0; i < 60; i++) { click("#roll"); const v = text("#dice"); if (!/^[1-6]$/.test(v)) return "Выпало: «" + v + "»"; } return true;'),
                       dom('Выпадают разные числа', 'const seen = new Set(); for (let i = 0; i < 60; i++) { click("#roll"); seen.add(text("#dice")); } return seen.size >= 4 || "За 60 бросков выпало всего " + seen.size + " разных чисел";')],
                solution="let dice = document.querySelector('#dice')\n\ndocument.querySelector('#roll').addEventListener('click', function () {\n"
                         "    dice.textContent = Math.floor(Math.random() * 6) + 1\n})\n"),
            task('Сюрприз через 2 секунды', P(
                'Блок <code>#surprise</code> сначала спрятан. Через 2 секунды после загрузки страницы покажи его '
                '(<code>style.display = \'block\'</code>) с помощью <code>setTimeout</code>.'),
                level=1, new=True, fixture='<div id="surprise" style="display: none; font-size: 60px;">🎁 Сюрприз!</div>',
                tests=[dom('Сначала блок спрятан', 'return css("#surprise", "display") === "none" || "Блок должен быть спрятан в начале";'),
                       dom('Через 2 секунды блок виден', 'await wait(2100); return css("#surprise", "display") !== "none" || "Через 2 секунды блок всё ещё спрятан";'),
                       code_has(r'setTimeout\(', 'Используется setTimeout')],
                solution="setTimeout(function () {\n    document.querySelector('#surprise').style.display = 'block'\n}, 2000)\n"),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('setInterval и setTimeout', 'https://learn.javascript.ru/settimeout-setinterval', 'read'),
            ('Выбор случайного числа', 'https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/Math/random', 'read'),
        ]),
        js_lessons(27),
    ],
)

# ------------------------------------------------------------------ Урок 28
L28_MODAL = page('''
<h1>Lorem ipsum dolor sit amet consectetur, adipisicing elit.</h1>
<button id="open">ОТКРЫТЬ ОКНО</button>
<div id="modal">
    <button id="close">ЗАКРЫТЬ ОКНО</button>
</div>
<script>
    let body = document.querySelector('body')
    let modal = document.querySelector('#modal')

    document.querySelector('#close').addEventListener('click', function () {
        modal.remove()
    })
    document.querySelector('#open').addEventListener('click', function () {
        body.append(modal)
    })
</script>
''', css='''
        body { margin: 0; height: 100vh; background-color: #482ff7; color: white; display: flex; flex-direction: column;
               justify-content: center; align-items: center; text-align: center; font-family: sans-serif; }
        #modal { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(131, 24, 131, 0.83);
                 display: flex; justify-content: center; align-items: center; }
        button { border: 0; color: white; font-size: 2em; font-weight: bold; padding: 1em 1.75em; border-radius: 10px; cursor: pointer; }
        #close { background-color: #fc5185; }
        #open { background-color: #22eaaa; }
''', title='Модальное окно')

L28 = dict(
    id='l28', file='lesson_28_adv.html', num='28', course='js', mode='js',
    short='ООП: объекты и классы',
    title='ООП — объектно-ориентированное программирование',
    about='Конструкторы, классы, методы, this',
    lead='Учимся описывать «чертежи» объектов: героев, машин, врагов — и создавать по ним сколько угодно экземпляров.',
    sections=[
        sec('Методы и функции для заданий', emoji='🧰', items=[table(['Как вызвать', 'Что делает'], TIMERS['rows'] + [
            ['<code>ELEMENT.append(OTHER)</code>', 'Добавление элемента OTHER в DOM-дерево'],
            ['<code>ELEMENT.remove()</code>', 'Удаление элемента из DOM-дерева'],
        ], caption=CAPS)]),
        sec('Задания', emoji='🏎️', items=[
            task('Модальное окно', P(
                'Создай <a href="https://www.w3schools.com/bootstrap4/bootstrap_modal.asp" target="_blank" rel="noopener">модальное окно</a>: '
                'кнопка <code>#close</code> убирает окно <code>#modal</code> со страницы, а кнопка <code>#open</code> возвращает его.'),
                level=2, mode='html', images=[('img/l28_q3.gif', 'Модальное окно')], answer_link='lesson_28_ans_1.html',
                tests=[has('#modal'), dom('Кнопка закрытия убирает окно', 'click("#close"); return !has("#modal") || "Окно не исчезло";'),
                       dom('Кнопка открытия возвращает окно', 'if (has("#modal")) click("#close"); click("#open"); return has("#modal") || "Окно не вернулось";')],
                solution=L28_MODAL),
            task('Гонка — простой вариант', P('Создай игру «Гонка», как на анимации. Каждая машина — объект, созданный конструктором.'),
                 level=3, local=True, images=[('img/l28_q1.gif', 'Гонка')], answer_link='race_homework_easy.html'),
            task('Гонка — сложный вариант', P('Усложни «Гонку»: добавь препятствия и счёт.'),
                 level=3, local=True, images=[('img/l28_q2.gif', 'Гонка hard')], answer_link='race_homework_hard.html'),
            task('Конструктор героя', P(
                'Напиши функцию-конструктор <code>Hero(name, hp)</code> (или класс <code>class Hero</code>). '
                'У героя есть свойства <code>name</code> и <code>hp</code> и метод <code>attack(target)</code>, '
                'который отнимает у цели 10 здоровья.'),
                level=2, new=True,
                starter="function Hero(name, hp) {\n    \n}\n\nlet arthur = new Hero('Артур', 100)\nlet goblin = new Hero('Гоблин', 30)\narthur.attack(goblin)\nconsole.log(goblin.hp)\n",
                tests=[call("new Hero('Артур', 100).name", "'Артур'"), call("new Hero('Артур', 100).hp", '100'),
                       dom('attack отнимает 10 здоровья', 'const a = new Hero("A", 100), b = new Hero("B", 50); a.attack(b); a.attack(b); return (b.hp === 30 && a.hp === 100) || "После двух атак у цели " + b.hp + " hp, у атакующего " + a.hp;')],
                solution="function Hero(name, hp) {\n    this.name = name\n    this.hp = hp\n    this.attack = function (target) {\n        target.hp -= 10\n    }\n}\n\n"
                         "let arthur = new Hero('Артур', 100)\nlet goblin = new Hero('Гоблин', 30)\narthur.attack(goblin)\nconsole.log(goblin.hp)\n"),
            task('Класс Car', P('Напиши класс <code>Car</code>:',
                UL('в <code>constructor(brand)</code> сохраняются марка <code>brand</code> и скорость <code>speed = 0</code>',
                   'метод <code>accelerate()</code> увеличивает скорость на 10',
                   'метод <code>brake()</code> уменьшает скорость на 10, но не ниже 0',
                   'метод <code>info()</code> возвращает строку <b>Лада: 20 км/ч</b>')),
                level=3, new=True, starter="class Car {\n    constructor(brand) {\n        \n    }\n}\n\nlet car = new Car('Лада')\ncar.accelerate()\ncar.accelerate()\nconsole.log(car.info())\n",
                tests=[call("new Car('Лада').speed", '0'), call("(() => { const c = new Car('Лада'); c.accelerate(); c.accelerate(); return c.info() })()", "'Лада: 20 км/ч'"),
                       call("(() => { const c = new Car('BMW'); c.accelerate(); c.brake(); c.brake(); return c.speed })()", '0', 'Скорость не бывает меньше 0'),
                       code_has(r'class\s+Car', 'Используется class')],
                solution="class Car {\n    constructor(brand) {\n        this.brand = brand\n        this.speed = 0\n    }\n\n    accelerate() {\n        this.speed += 10\n    }\n\n"
                         "    brake() {\n        this.speed = Math.max(0, this.speed - 10)\n    }\n\n    info() {\n        return this.brand + ': ' + this.speed + ' км/ч'\n    }\n}\n\n"
                         "let car = new Car('Лада')\ncar.accelerate()\ncar.accelerate()\nconsole.log(car.info())\n"),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Конструктор в JavaScript (на русском)', 'https://learn.javascript.ru/constructor-new', 'read'),
            ('Конструктор в JavaScript (на английском)', 'https://www.w3schools.com/js/js_object_constructors.asp', 'read'),
            ('Классы', 'https://learn.javascript.ru/class', 'read'),
        ]),
        js_lessons(28),
    ],
)

# ------------------------------------------------------------------ Урок 29
CANVAS = '<canvas id="canvas" width="400" height="400"></canvas>\n<style>body { background-color: #252423; } canvas { background-color: #fdfff5; border-radius: 5px; }</style>'
CANVAS_START = "let canvas = document.querySelector('#canvas')\nlet ctx = canvas.getContext('2d')\n\n"

L29 = dict(
    id='l29', file='lesson_29_adv.html', num='29', course='js', mode='js',
    short='Canvas: рисуем кодом',
    title='Canvas',
    about='getContext, fillRect, arc, lineTo, рисование циклами',
    lead='Canvas — холст, на котором JavaScript рисует фигуры, линии и текст. На нём делают игры и графики.',
    sections=[
        sec('Методы canvas', emoji='🖌️', items=[table(['Как вызвать', 'Что делает'], [
            ['<code>ctx = canvas.getContext(\'2d\')</code>', 'Получить «кисть» для рисования на холсте'],
            ['<code>ctx.fillRect(x, y, w, h)</code>', 'Закрашенный прямоугольник'],
            ['<code>ctx.fillStyle = \'color\'</code>', 'Цвет заливки фигур'],
            ['<code>ctx.strokeRect(x, y, w, h)</code>', 'Прямоугольник-контур'],
            ['<code>ctx.strokeStyle = \'color\'</code>', 'Цвет контура'],
            ['<code>ctx.clearRect(x, y, w, h)</code>', 'Стереть прямоугольную область'],
            ['<code>ctx.font = \'30px Arial\'</code>', 'Выбор шрифта'],
            ['<code>ctx.fillText(\'Text\', x, y)</code>', 'Закрашенный текст'],
            ['<code>ctx.strokeText(\'Text\', x, y)</code>', 'Текст-контур'],
            ['<code>ctx.beginPath()</code>', 'Начать рисовать свою фигуру'],
            ['<code>ctx.moveTo(x, y)</code>', 'Переместить кисть (не рисуя)'],
            ['<code>ctx.lineTo(x, y)</code>', 'Провести линию до точки'],
            ['<code>ctx.stroke()</code>', 'Обвести путь'],
            ['<code>ctx.fill()</code>', 'Залить фигуру цветом'],
            ['<code>ctx.closePath()</code>', 'Замкнуть фигуру'],
            ['<code>ctx.arc(x, y, radius, startAngle, endAngle)</code>', 'Дуга. Круг: <code>ctx.arc(100, 100, 40, 0, Math.PI * 2)</code>'],
        ])]),
        sec('Задания', emoji='🎨', items=[
            task('Сетка на холсте', P(
                'С помощью canvas и циклов расчерти холст 400 × 400 на вертикальные и горизонтальные линии через каждые 40px '
                'и подпиши номера клеток.'),
                level=2, images=[('img/l29_q1.png', 'Сетка')], answer_link='lesson_29_ans_1.html',
                fixture=CANVAS, starter=CANVAS_START,
                tests=[dom('Есть вертикальные линии', 'return [40, 200, 360].every(x => pixel("#canvas", x, 30)[3] > 0) || "Не вижу вертикальных линий на x = 40, 200, 360";'),
                       dom('Есть горизонтальные линии', 'return [80, 240, 320].every(y => pixel("#canvas", 30, y)[3] > 0) || "Не вижу горизонтальных линий на y = 80, 240, 320";'),
                       dom('Внутри клеток пусто', 'return [[30, 30], [250, 250], [110, 350]].every(([x, y]) => pixel("#canvas", x, y)[3] === 0) || "Клетки должны быть пустыми внутри";'),
                       code_has(r'for\s*\(', 'Линии рисуются в цикле')],
                solution=CANVAS_START + "let step = 40\n\nfor (let i = 1; i < 10; i++) {\n    ctx.beginPath()\n    ctx.moveTo(step * i, 0)\n    ctx.lineTo(step * i, 400)\n    ctx.stroke()\n\n"
                         "    ctx.beginPath()\n    ctx.moveTo(0, step * i)\n    ctx.lineTo(400, step * i)\n    ctx.stroke()\n}\n\nfor (let i = 0; i < 10; i++) {\n"
                         "    ctx.fillText(i, step * i + 4, 12)\n}\n"),
            task('Шахматная доска', P(
                'С помощью canvas и <b>двух вложенных циклов</b> нарисуй шахматную доску 8 × 8 из клеток по 50px. '
                'Левая верхняя клетка — светлая (<code>white</code>), соседняя — тёмная (<code>#333</code>).'),
                level=2, images=[('img/l29_q2.png', 'Шахматная доска')], answer_link='lesson_29_ans_2.html',
                fixture=CANVAS, starter=CANVAS_START,
                hint=P('Клетка тёмная, если <code>(i + j) % 2 === 1</code>.'),
                tests=[dom('Клетки чередуются', 'const dark = (x, y) => pixel("#canvas", x, y)[0] < 128 && pixel("#canvas", x, y)[3] > 0; const cells = [[0,0],[1,0],[0,1],[1,1],[7,7],[6,7],[3,4]]; for (const [i, j] of cells) { const want = (i + j) % 2 === 1; if (dark(i * 50 + 25, j * 50 + 25) !== want) return "Клетка (" + i + ", " + j + ") должна быть " + (want ? "тёмной" : "светлой"); } return true;'),
                       code_has(r'for[\s\S]*for', 'Используются вложенные циклы')],
                solution=CANVAS_START + "for (let i = 0; i < 8; i++) {\n    for (let j = 0; j < 8; j++) {\n        if ((i + j) % 2 === 1) {\n            ctx.fillStyle = '#333'\n"
                         "        } else {\n            ctx.fillStyle = 'white'\n        }\n        ctx.fillRect(i * 50, j * 50, 50, 50)\n    }\n}\n"),
            task('Мир с физикой столкновений', P('Создай «мир», в котором шарики летают и отскакивают от стен и друг от друга.'),
                 level=3, local=True, images=[('img/l29_q3.gif', 'Физика')], answer_link='lesson_29_ans_3.html'),
            task('Свой Paint', P('Создай аналог программы Paint: рисование мышкой, выбор цвета и толщины кисти.'),
                 level=3, local=True, images=[('img/l29_q4.gif', 'Paint')], answer_link='lesson_29_ans_4.html'),
            task('Смайлик на canvas', P('Нарисуй смайлик на холсте 400 × 400:',
                UL('лицо — жёлтый (<code>gold</code>) круг с центром (200, 200) и радиусом 150',
                   'глаза — чёрные круги радиусом 20 в точках (140, 160) и (260, 160)',
                   'улыбка — дуга: <code>ctx.arc(200, 220, 80, 0, Math.PI)</code>')),
                level=1, new=True, fixture=CANVAS, starter=CANVAS_START,
                tests=[dom('Жёлтое лицо', 'const p = pixel("#canvas", 200, 80); return (p[0] > 200 && p[1] > 150 && p[2] < 100) || "В точке (200, 80) должен быть жёлтый цвет";'),
                       dom('Чёрные глаза', 'return [[140, 160], [260, 160]].every(([x, y]) => { const p = pixel("#canvas", x, y); return p[0] < 60 && p[3] > 200; }) || "В точках (140, 160) и (260, 160) должны быть чёрные глаза";'),
                       dom('Есть улыбка', 'const p = pixel("#canvas", 200, 300); return (p[0] < 150 || p[2] > 100) || "Не вижу улыбку в точке (200, 300)";'),
                       code_has(r'\.arc\(', 'Используется arc')],
                solution=CANVAS_START + "ctx.fillStyle = 'gold'\nctx.beginPath()\nctx.arc(200, 200, 150, 0, Math.PI * 2)\nctx.fill()\n\n"
                         "ctx.fillStyle = 'black'\nctx.beginPath()\nctx.arc(140, 160, 20, 0, Math.PI * 2)\nctx.fill()\nctx.beginPath()\n"
                         "ctx.arc(260, 160, 20, 0, Math.PI * 2)\nctx.fill()\n\nctx.lineWidth = 8\nctx.beginPath()\nctx.arc(200, 220, 80, 0, Math.PI)\nctx.stroke()\n"),
            task('Домик', P('Нарисуй домик:',
                UL('стены — коричневый (<code>saddlebrown</code>) прямоугольник: x = 100, y = 200, ширина 200, высота 150',
                   'крыша — красный (<code>red</code>) треугольник с вершинами (100, 200), (200, 100), (300, 200) — используй '
                   '<code>beginPath</code>, <code>moveTo</code>, <code>lineTo</code>, <code>fill</code>',
                   'окно — голубой (<code>skyblue</code>) квадрат 50 × 50 в точке (175, 240)')),
                level=2, new=True, fixture=CANVAS, starter=CANVAS_START,
                tests=[dom('Коричневые стены', 'const p = pixel("#canvas", 120, 330); return (p[0] > 100 && p[1] < 100 && p[2] < 60) || "В точке (120, 330) должна быть коричневая стена";'),
                       dom('Красная крыша', 'const p = pixel("#canvas", 200, 170); return (p[0] > 200 && p[1] < 60 && p[2] < 60) || "В точке (200, 170) должна быть красная крыша";'),
                       dom('Над крышей пусто', 'return pixel("#canvas", 120, 120)[3] === 0 || "В точке (120, 120) должно быть пусто — крыша треугольная";'),
                       dom('Голубое окно', 'const p = pixel("#canvas", 200, 265); return (p[2] > 200 && p[1] > 150) || "В точке (200, 265) должно быть голубое окно";')],
                solution=CANVAS_START + "ctx.fillStyle = 'saddlebrown'\nctx.fillRect(100, 200, 200, 150)\n\nctx.fillStyle = 'red'\nctx.beginPath()\n"
                         "ctx.moveTo(100, 200)\nctx.lineTo(200, 100)\nctx.lineTo(300, 200)\nctx.closePath()\nctx.fill()\n\nctx.fillStyle = 'skyblue'\nctx.fillRect(175, 240, 50, 50)\n"),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('Руководство по canvas', 'https://developer.mozilla.org/ru/docs/Web/API/Canvas_API/Tutorial', 'read'),
            ('Практика canvas #1', 'https://www.w3schools.com/html/html5_canvas.asp', 'practice'),
            ('Практика canvas #2', 'https://www.w3schools.com/graphics/canvas_drawing.asp', 'practice'),
            ('Физическая модель столкновений', 'https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection', 'read'),
        ]),
        js_lessons(29),
    ],
)

# ------------------------------------------------------------------ Уроки 30–31
L30 = dict(
    id='l30', file='lesson_30_31_adv.html', num='30–31', course='js', mode='js',
    short='Создаём игру',
    title='Создание программы: игра на canvas',
    about='Собираем всё изученное в настоящую игру',
    lead='Два урока на одну большую цель — свою игру на canvas.',
    sections=[
        sec('Задания', emoji='🕹️', items=[
            task('Игра «Арканоид»', P(
                'Создай игру, как на анимации: платформа управляется с клавиатуры, мячик отскакивает от стен, платформы и кирпичей.'),
                level=3, local=True, images=[('img/l30_q1.gif', 'Игра')], answer_link='lesson_30_ans_1.html'),
            task('Управление с клавиатуры', P(
                'Первый шаг к игре: квадрат <code>#player</code> должен двигаться стрелками. По нажатию '
                '<kbd>→</kbd> (<code>event.key === \'ArrowRight\'</code>) он сдвигается вправо на 20px, по <kbd>←</kbd> — влево. '
                'Позицию храни в переменной <code>x</code> и меняй <code>player.style.left</code>.'),
                level=2, new=True,
                fixture='<div id="player"></div>\n<style>#player { position: absolute; top: 100px; left: 0; width: 40px; height: 40px; background-color: #ff4d8d; border-radius: 8px; }</style>',
                starter="let player = document.querySelector('#player')\nlet x = 0\n\ndocument.addEventListener('keydown', function (event) {\n    \n})\n",
                tests=[dom('Стрелка вправо сдвигает на 20px', 'fire(document.body, "keydown", { key: "ArrowRight" }); fire(document.body, "keydown", { key: "ArrowRight" }); return Math.round($("#player").getBoundingClientRect().left) === 40 || "После двух нажатий → left = " + Math.round($("#player").getBoundingClientRect().left) + "px";'),
                       dom('Стрелка влево сдвигает обратно', 'const a = $("#player").getBoundingClientRect().left; fire(document.body, "keydown", { key: "ArrowLeft" }); return Math.round(a - $("#player").getBoundingClientRect().left) === 20 || "Стрелка влево не сдвигает на 20px";'),
                       dom('Другие клавиши не двигают', 'const a = $("#player").getBoundingClientRect().left; fire(document.body, "keydown", { key: "a" }); return $("#player").getBoundingClientRect().left === a || "Квадрат не должен двигаться от других клавиш";')],
                solution="let player = document.querySelector('#player')\nlet x = 0\n\ndocument.addEventListener('keydown', function (event) {\n"
                         "    if (event.key === 'ArrowRight') {\n        x += 20\n    } else if (event.key === 'ArrowLeft') {\n        x -= 20\n    }\n"
                         "    player.style.left = x + 'px'\n})\n"),
        ]),
    ],
)

# ------------------------------------------------------------------ Урок 32
L32 = dict(
    id='l32', file='lesson_32_adv.html', num='32', course='js',
    short='Библиотеки и Figma',
    title='Библиотеки для JavaScript. Знакомство с Figma',
    about='Figma, выбор палитры, популярные JS-библиотеки',
    lead='Готовимся к большому проекту: заводим аккаунт в Figma и узнаём, какие готовые библиотеки упрощают жизнь программиста.',
    sections=[
        sec('Задания', emoji='📖', items=[
            task('Создай аккаунт в Figma', P(
                'Зарегистрируйся на <a href="https://figma.com/" target="_blank" rel="noopener">figma.com</a> — '
                'в ней мы будем рисовать макет своего сайта.'),
                level=1, editor=False, images=[('img/figma.png', 'Figma')]),
            task('Обязательно к прочтению', P('Прочитай статьи:',
                UL('<a href="https://developer.mozilla.org/ru/docs/Learn/Getting_started_with_the_web/What_will_your_website_look_like" target="_blank" rel="noopener">Каким должен быть веб-сайт</a>',
                   '<a href="https://webevolution.ru/blog/sajti/cvetovaya-gamma-sajta-rekomendacii-po-podboru/" target="_blank" rel="noopener">Выбор цветовой палитры</a>'),
                'Запиши, о чём будет твой сайт-портфолио и какие цвета ты для него выберешь.'),
                level=1, editor=False),
            task('Популярные библиотеки', P(
                'Посмотри <a href="https://getflywheel.com/layout/best-javascript-libraries-frameworks-2020/" target="_blank" rel="noopener">обзор лучших библиотек и фреймворков</a> '
                'и видео ниже. Выбери одну библиотеку, которая тебе понравилась, и расскажи о ней на уроке.'),
                level=2, editor=False),
            html('<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/qugY8axtvWY" title="Библиотеки JavaScript" '
                 'allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>'),
        ]),
    ],
)

# ------------------------------------------------------------------ Уроки 33–36: дизайн-проект
BOOKS = ('Что почитать', [
    ('Книга «Отзывчивый веб-дизайн»', 'assets/responsive.pdf', 'read'),
    ('Книга «Не заставляйте меня думать»', 'assets/krug.pdf', 'read'),
])

L33 = dict(
    id='l33', file='lesson_33_adv.html', num='33', course='project',
    short='Портфолио: макет',
    title='Создаём сайт-портфолио: макет',
    about='Материалы, Figma, макеты для 1200 / 768 / 576px',
    lead='Начинаем свой главный проект — сайт-портфолио. Сначала собираем материалы и рисуем макет.',
    sections=[
        sec('Где искать материалы для сайта', emoji='🔎', items=[
            table(['Ресурс', 'Что там есть'], [
                ['<a href="https://www.freepik.com/" target="_blank" rel="noopener">Freepik</a>', 'Картинки'],
                ['<a href="https://www.pinterest.ru/" target="_blank" rel="noopener">Pinterest</a>', 'Картинки и идеи'],
                ['<a href="https://material.io/design" target="_blank" rel="noopener">Google Material</a>', 'Иконки'],
                ['<a href="https://icons8.com/" target="_blank" rel="noopener">Icons8</a>', 'Иконки'],
                ['<a href="https://fonts.google.com/" target="_blank" rel="noopener">Google Fonts</a>', 'Шрифты'],
                ['<a href="https://fontflipper.com/upload" target="_blank" rel="noopener">Fontflipper</a>', 'Подбор шрифтов'],
                ['<a href="https://fontjoy.com/" target="_blank" rel="noopener">Fontjoy</a>', 'Сочетания шрифтов'],
                ['<a href="https://patternpad.com/" target="_blank" rel="noopener">Patternpad</a>', 'Паттерны для фона'],
                ['<a href="https://freellustrations.com/" target="_blank" rel="noopener">Freellustrations</a>', 'Бесплатные иллюстрации'],
            ]),
        ]),
        sec('Задания', emoji='🖼️', items=[
            task('Макет для трёх экранов', P(
                'В <a href="https://www.figma.com/" target="_blank" rel="noopener">Figma</a> нарисуй макет своего сайта-портфолио для трёх размеров экрана: '
                '<b>≥ 1200px</b> (компьютер), <b>768px</b> (планшет) и <b>&lt; 576px</b> (телефон).',
                '<a href="assets/adobexd_design.rar" target="_blank" rel="noopener">Материалы для макета</a> — обязательно скачай!'),
                level=3, local=True, images=[('img/adapt.png', 'Разрешения')]),
            task('Изучи готовый макет', P(
                'Открой <a href="https://www.figma.com/file/Jp9SBTYQRIuPLRfPCIni0X/lesson-33?node-id=0%3A1" target="_blank" rel="noopener">готовый макет для больших экранов</a> '
                '(или <a href="assets/lesson33_figma.fig" download>скачай его</a>) и посмотри, как устроены отступы, сетка и шрифты.'),
                level=1, editor=False),
        ]),
    ],
    links=[BOOKS],
)

L34 = dict(
    id='l34', file='lesson_34_adv.html', num='34', course='project', mode='html',
    short='Портфолио: BEM и Sass',
    title='Создаём сайт-портфолио: вёрстка для 1920px',
    about='BEM, Sass, reset CSS',
    lead='Верстаем сайт по макету для большого экрана и учимся держать код в порядке: методология BEM и препроцессор Sass.',
    sections=[
        sec('Ресурсы для создания сайта', emoji='📚', items=[
            note('<a href="https://ru.bem.info/methodology/quick-start/" target="_blank" rel="noopener">BEM — методология</a> · '
                 '<a href="https://sass-scss.ru/guide/" target="_blank" rel="noopener">Sass — препроцессор для CSS</a> · '
                 '<a href="https://gist.github.com/DavidWells/18e73022e723037a50d6" target="_blank" rel="noopener">reset CSS (обнуление стилей)</a>', 'info'),
        ]),
        sec('Примеры вёрстки по BEM', emoji='🧱', items=[images(('img/bem_1.png', 'BEM, пример 1'), ('img/bem_2.png', 'BEM, пример 2'))]),
        sec('Как установить и использовать Sass', emoji='💅', items=[
            images(('img/sass.png', 'Установка Sass'), ('img/sass_1.png', 'Sass, шаг 1'), ('img/sass_2.png', 'Sass, шаг 2')),
        ]),
        sec('Задания', emoji='✍️', items=[
            task('Сверстай сайт для 1920px', P(
                'Сверстай свой сайт-портфолио по макету для экрана 1920px. Называй классы по BEM, стили пиши на Sass. '
                'Как выгрузить картинки из макета — в <a href="lesson_34_tutorial.html" target="_blank">инструкции</a>.'),
                level=3, local=True),
            task('Карточка по BEM', P('Сверстай карточку проекта, называя классы по BEM:',
                UL('блок — <code>card</code>',
                   'элементы — <code>card__image</code>, <code>card__title</code>, <code>card__text</code>, <code>card__button</code>',
                   'модификатор — у кнопки <code>card__button--active</code> другой цвет фона')),
                level=2, new=True,
                tests=[has('.card'), has('.card .card__image', 'Есть card__image внутри card'), has('.card .card__title'), has('.card .card__text'),
                       has('.card .card__button'), has('.card__button.card__button--active', 'Есть модификатор card__button--active'),
                       dom('У модификатора свой фон', 'const btns = $$(".card__button"); const act = $(".card__button--active"); const plain = btns.find(b => !b.classList.contains("card__button--active")); if (!plain) return "Сделай ещё одну кнопку без модификатора, чтобы было видно разницу"; return getComputedStyle(act).backgroundColor !== getComputedStyle(plain).backgroundColor || "У card__button--active должен быть другой фон";')],
                solution=page('''
<div class="card">
    <img class="card__image" src="img/lesson_6.jpg" alt="Проект">
    <h3 class="card__title">Мой первый сайт</h3>
    <p class="card__text">Сайт о космосе на HTML и CSS.</p>
    <button class="card__button">Подробнее</button>
    <button class="card__button card__button--active">Открыть</button>
</div>
''', css='''
        .card { width: 260px; padding: 16px; border-radius: 16px; background-color: #f6f4ff; font-family: sans-serif; }
        .card__image { width: 100%; border-radius: 12px; }
        .card__title { margin: 12px 0 4px; }
        .card__text { color: #555; }
        .card__button { border: 0; padding: 10px 16px; border-radius: 8px; background-color: #ddd; }
        .card__button--active { background-color: #6d4aff; color: white; }
''')),
        ]),
    ],
    links=[
        ('Что посмотреть', [('Вёрстка сайта с нуля (BEM и Sass)', 'https://www.youtube.com/watch?v=3AP7opexzSs', 'video')]),
        ('Что почитать', [
            ('Как создавать структуру в Sass-проектах', 'https://sass-guidelin.es/#architecture', 'read'),
            ('Готовая файловая структура для проекта', 'https://github.com/HugoGiraudel/sass-boilerplate/tree/master/stylesheets', 'read'),
            *BOOKS[1],
        ]),
    ],
)

L35 = dict(
    id='l35', file='lesson_35_adv.html', num='35', course='project', mode='html',
    short='Портфолио: адаптивность',
    title='Создаём сайт-портфолио: 1920 / 768 / 360px',
    about='Адаптивная вёрстка, clip-path, брейкпоинты',
    lead='Делаем так, чтобы портфолио отлично смотрелось на планшете и телефоне.',
    sections=[
        sec('Задания', emoji='📱', items=[
            task('Адаптивная версия сайта', P(
                'Сверстай сайт для разрешений 1920, 768 и 360 пикселей по макетам. Макет — '
                '<a href="assets/lesson35_figma_done.fig" download>скачать для Figma</a> или '
                '<a href="https://www.figma.com/file/HyCmE9VWYgQZRZO4SWukyP/Untitled?node-id=0%3A1" target="_blank" rel="noopener">открыть онлайн</a>.'),
                level=3, local=True, images=[('img/35_tablet.png', 'Планшет'), ('img/35_phone.png', 'Телефон')]),
            task('Три брейкпоинта', P('Сделай так, чтобы у блока <code>.projects</code> менялось число колонок:',
                UL('по умолчанию — 3 колонки (<code>grid-template-columns: repeat(3, 1fr)</code>)',
                   '<code>@media (max-width: 768px)</code> — 2 колонки',
                   '<code>@media (max-width: 360px)</code> — 1 колонка')),
                level=2, new=True,
                starter=page('<div class="projects">\n' + '\n'.join(f'    <div class="project">Проект {i}</div>' for i in range(1, 7)) + '\n</div>', css='''
        .projects { display: grid; gap: 16px; }
        .project { background-color: #19b8a6; color: white; padding: 40px; border-radius: 12px; font-family: sans-serif; }
'''),
                tests=[dom('На широком экране 3 колонки', 'return css(".projects", "grid-template-columns").split(" ").length === 3 || "Сейчас колонки: " + css(".projects", "grid-template-columns");'),
                       dom('@media (max-width: 768px) — 2 колонки', 'const m = media().find(m => /max-width:\\s*768px/.test(m.conditionText || m.media.mediaText)); return (m && /repeat\\(2,|1fr 1fr(?! 1fr)/.test(m.cssText)) || "Добавь @media (max-width: 768px) с двумя колонками";'),
                       dom('@media (max-width: 360px) — 1 колонка', 'const m = media().find(m => /max-width:\\s*360px/.test(m.conditionText || m.media.mediaText)); return (m && /grid-template-columns:\\s*(1fr|repeat\\(1,)/.test(m.cssText)) || "Добавь @media (max-width: 360px) с одной колонкой";'),
                       dom('Медиазапросы идут от большего к меньшему', 'const list = media().map(m => parseInt((m.conditionText || m.media.mediaText).match(/\\d+/))); return list.indexOf(768) < list.indexOf(360) || "Сначала @media для 768px, потом для 360px — иначе 360px перезапишется";')],
                solution=page('<div class="projects">\n' + '\n'.join(f'    <div class="project">Проект {i}</div>' for i in range(1, 7)) + '\n</div>', css='''
        .projects { display: grid; gap: 16px; grid-template-columns: repeat(3, 1fr); }
        .project { background-color: #19b8a6; color: white; padding: 40px; border-radius: 12px; font-family: sans-serif; }
        @media (max-width: 768px) {
            .projects { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 360px) {
            .projects { grid-template-columns: 1fr; }
        }
''')),
            task('Скошенный фон через clip-path', P(
                'Сделай у шапки <code>.hero</code> скошенный нижний край с помощью <code>clip-path: polygon(...)</code>. '
                'Подобрать форму поможет <a href="https://bennettfeely.com/clippy/" target="_blank" rel="noopener">генератор clip-path</a>.'),
                level=2, new=True,
                starter=page('<section class="hero">\n    <h1>Привет! Я — веб-дизайнер</h1>\n</section>', css='''
        body { margin: 0; font-family: sans-serif; }
        .hero { height: 300px; background: linear-gradient(135deg, #6d4aff, #ff4d8d); color: white; display: flex; align-items: center; justify-content: center; }
'''),
                tests=[dom('У .hero есть clip-path: polygon', 'return /polygon/.test(css(".hero", "clip-path")) || "Добавь .hero clip-path: polygon(...)";')],
                solution=page('<section class="hero">\n    <h1>Привет! Я — веб-дизайнер</h1>\n</section>', css='''
        body { margin: 0; font-family: sans-serif; }
        .hero { height: 300px; background: linear-gradient(135deg, #6d4aff, #ff4d8d); color: white; display: flex; align-items: center; justify-content: center;
                clip-path: polygon(0 0, 100% 0, 100% 80%, 0 100%); }
''')),
        ]),
    ],
    links=[
        ('Ресурсы для создания сайта', [
            ('32 элемента современного веб-дизайна', 'https://careerfoundry.com/en/blog/ui-design/ui-element-glossary/', 'design'),
            ('Генератор clip-path', 'https://bennettfeely.com/clippy/', 'tool'),
            ('Адаптивные точки для SCSS', 'https://github.com/wrongakram/sass-mediaqueries/blob/master/src/breakpoints/breakpoints.scss', 'tool'),
            ('Архитектура Sass-проектов', 'https://sass-guidelin.es/#architecture', 'read'),
            ('Пример архитектуры Sass', 'https://github.com/HugoGiraudel/sass-boilerplate/tree/master/stylesheets', 'read'),
        ]),
        ('Что почитать', [
            ('Адаптивная вёрстка', 'https://jazzteam.org/ru/technical-articles/overview-of-approaches-and-css-frameworks-for-adaptive-web-page-layout/', 'read'),
            *BOOKS[1],
        ]),
    ],
)

L36 = dict(
    id='l36', file='lesson_36_adv.html', num='36', course='project', mode='html',
    short='Портфолио: публикация',
    title='Создаём сайт-портфолио: проверка и публикация',
    about='Чек-лист, Lighthouse, сжатие картинок, хостинг',
    lead='Финишная прямая: проверяем сайт по чек-листу, ускоряем его и выкладываем в интернет.',
    sections=[
        sec('Чек-лист перед публикацией (без хостинга)', emoji='✅', items=[table(['Проверка', 'Описание'], [
            ['Микро-ошибки', '<a href="https://chrome.google.com/webstore/detail/html-validator/mpbelhhnfhfjnaehkcnnaknldmnocglk" target="_blank" rel="noopener">HTML-валидатор</a>'],
            ['Изображения', 'Все ли изображения корректно загружаются'],
            ['Ссылки', 'Работают ли все ссылки'],
            ['Обратная связь', 'Обязательная секция для любого сайта'],
            ['Мобильные устройства', 'Сайт правильно выглядит на всех устройствах'],
            ['Chrome — Lighthouse', 'Проверка Lighthouse для мобильных и компьютеров'],
            ['Кросс-браузерный тест', 'Сайт работает во всех современных браузерах — <a href="https://www.w3counter.com/globalstats.php" target="_blank" rel="noopener">список браузеров</a>'],
        ])]),
        sec('Чек-лист перед публикацией (с хостингом)', emoji='🌍', items=[table(['Проверка', 'Описание'], [
            ['Корректность URL', 'Перенаправления ведут на нужные страницы'],
            ['robots.txt', '<a href="https://support.google.com/webmasters/answer/6062608?hl=ru" target="_blank" rel="noopener">Что такое robots.txt</a>'],
        ], caption='За подробным руководством обращайся в службу поддержки хостинга')]),
        sec('Полезные плагины для VS Code', emoji='🧩', items=[steps(
            ('CSS/JS minifier — сжимает код', [('img/l36_1.png', 'Minifier')]),
            ('Sass compiler — превращает Sass в CSS', [('img/l36_2.png', 'Sass compiler')]),
            ('Live Server — обновляет страницу при сохранении', [('img/l36_3.png', 'Live Server')]),
        )]),
        sec('Задания', emoji='🚀', items=[
            task('Проверь сайт по чек-листу', P(
                'Пройди по чек-листу выше. Открой свой сайт в Chrome, нажми <kbd>F12</kbd> → вкладка <b>Lighthouse</b> → '
                '<b>Analyze page load</b>. Исправь всё, что подсветится красным, и добейся хотя бы 90 баллов.'),
                level=2, local=True),
            task('Опубликуй портфолио', P(
                'Сожми картинки (<a href="https://squoosh.app/editor" target="_blank" rel="noopener">squoosh.app</a>, '
                '<a href="https://compressjpeg.com" target="_blank" rel="noopener">compressjpeg</a>, '
                '<a href="https://compresspng.com/" target="_blank" rel="noopener">compresspng</a>) и выложи сайт на GitHub Pages '
                'или <a href="https://sprinthost.ru/s33951" target="_blank" rel="noopener">хостинг</a>. '
                'Пришли ссылку преподавателю!'),
                level=3, local=True),
            task('Картинка для любого экрана', P(
                'С помощью тега <code>&lt;picture&gt;</code> покажи на узких экранах (до 600px) картинку <code>img/35_phone.png</code>, '
                'а на остальных — <code>img/35_tablet.png</code>. У <code>&lt;img&gt;</code> обязательно заполни <code>alt</code>. '
                '<a href="https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images" target="_blank" rel="noopener">Как это работает</a>.'),
                level=2, new=True,
                tests=[has('picture'), has('picture source[media][srcset]', 'Есть source с media и srcset'),
                       dom('source для узких экранов', 'const s = $("picture source"); return (/max-width:\\s*600px/.test(s.media) && /35_phone/.test(s.srcset)) || "source должен показывать 35_phone.png при (max-width: 600px)";'),
                       has('picture img[src*="35_tablet"]', 'img по умолчанию — 35_tablet.png'),
                       dom('У картинки есть alt', 'return !!$("picture img").alt.trim() || "Заполни alt";')],
                solution=page('''
<picture>
    <source media="(max-width: 600px)" srcset="img/35_phone.png">
    <img src="img/35_tablet.png" alt="Макет моего сайта" width="300">
</picture>
''')),
        ]),
    ],
    links=[
        ('Ресурсы для создания сайта', [
            ('Сжимаем JPEG', 'https://compressjpeg.com', 'tool'),
            ('Сжимаем PNG', 'https://compresspng.com/', 'tool'),
            ('Сжимаем изображения', 'https://squoosh.app/editor', 'tool'),
            ('Изменяем размер изображений', 'https://resizeimage.net/', 'tool'),
            ('Используем картинки правильно (picture)', 'https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images', 'read'),
            ('Руководство: публикация веб-страницы', 'https://developer.mozilla.org/ru/docs/Learn/Getting_started_with_the_web/Publishing_your_website', 'read'),
            ('Хостинг, который используем мы', 'https://sprinthost.ru/s33951', 'tool'),
        ]),
        ('Что почитать', [
            ('Книга «Отзывчивый веб-дизайн» (ознакомительная версия)', 'assets/responsive.pdf', 'read'),
            ('Книга «Отзывчивый веб-дизайн» (купить)', 'https://www.ozon.ru/context/detail/id/8747299/', 'read'),
            ('Книга «Не заставляйте меня думать» (ознакомительная версия)', 'assets/krug.pdf', 'read'),
            ('Книга «Не заставляйте меня думать» (купить)', 'https://www.litres.ru/stiv-krug/ne-zastavlyayte-menya-dumat-veb-uzabiliti-i-zdravyy-smysl-24147734/', 'read'),
            ('Правила для контента', 'https://guide.so-edinenie.org/rules', 'read'),
        ]),
    ],
)

LESSONS = [L25, L26, L27, L28, L29, L30, L32, L33, L34, L35, L36]
