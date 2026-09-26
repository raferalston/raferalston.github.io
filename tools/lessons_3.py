"""Уроки 17–24: основы JavaScript."""
from kk_helpers import (task, sec, note, images, table, steps, P, UL, C,  # noqa: F401
                        dom, has, style, io, call, code_has, var_is, body_script)

W3J = 'https://www.w3schools.com/js/exercise_js.asp?filename=exercise_js_'


def practice_js(title, *names):
    return (title, [(f'Упражнение #{i + 1}', W3J + n, 'practice') for i, n in enumerate(names)])


def js_lessons(upto):
    return ('Предыдущие JS-уроки', [(f'Урок {n}', f'lesson_{n}_adv.html', 'lesson') for n in range(17, upto)])


JS_NOTE = note('Здесь пишем <b>только JavaScript</b>. <code>console.log()</code> и <code>alert()</code> выводят результат в консоль под редактором, '
               'а <code>prompt()</code> откроет окошко для ввода. При проверке ответы на <code>prompt()</code> подставляются сами.', 'info')

# ------------------------------------------------------------------ Урок 17
L17 = dict(
    id='l17', file='lesson_17_adv.html', num='17', course='js', mode='js',
    short='Введение в JavaScript',
    title='Знакомство с JavaScript',
    about='console.log, alert, первые шаги с DOM',
    lead='JavaScript оживляет страницы: реагирует на клики, меняет текст и цвета, считает и даже делает игры.',
    sections=[
        sec('Задания', emoji='⚡', items=[
            JS_NOTE,
            task('Первая программа', P('Выведи в консоль фразу <b>Привет, мир!</b> с помощью <code>console.log()</code>.'),
                 level=1, new=True, starter="// Напиши свою первую программу\n",
                 tests=[io([], ['Привет, мир!'])], solution="console.log('Привет, мир!')\n"),
            task('Окно с сообщением', P(
                'Покажи окно <code>alert()</code> с текстом <b>Добро пожаловать!</b>, а потом выведи в консоль, '
                'сколько будет <code>2 + 2</code> (пусть посчитает JavaScript).'),
                level=1, new=True,
                tests=[io([], ['Добро пожаловать!', '4']), code_has(r'2\s*\+\s*2', 'JavaScript сам считает 2 + 2')],
                solution="alert('Добро пожаловать!')\nconsole.log(2 + 2)\n"),
            task('Меняем текст на странице', P(
                'На странице есть заголовок <code>&lt;h1 id="title"&gt;</code>. С помощью JavaScript поменяй его текст на '
                '<b>Привет, JavaScript!</b> и сделай его красным.'),
                level=1, new=True,
                fixture='<h1 id="title">Скучный заголовок</h1>\n<p>Этот текст не трогаем.</p>',
                starter="let title = document.querySelector('#title')\n// Поменяй текст и цвет\n",
                hint=P('Текст меняется через <code>title.textContent = ...</code>, а цвет — через <code>title.style.color = ...</code>'),
                tests=[dom('Текст заголовка изменён', 'return text("#title") === "Привет, JavaScript!" || "Сейчас в заголовке: " + text("#title");'),
                       style('#title', 'color', 'red', 'Заголовок красный')],
                solution="let title = document.querySelector('#title')\ntitle.textContent = 'Привет, JavaScript!'\ntitle.style.color = 'red'\n"),
            task('Кнопка-приветствие', P(
                'Когда пользователь нажимает на кнопку <code>#hello</code>, должно появляться окно с текстом <b>Привет!</b>'),
                level=2, new=True,
                fixture='<button id="hello">Нажми меня</button>',
                starter="let button = document.querySelector('#hello')\n",
                hint=P('Используй <code>button.addEventListener(\'click\', function () { ... })</code>'),
                tests=[dom('До нажатия ничего не выводится', 'return !out().includes("Привет!") || "alert должен появляться только после нажатия";'),
                       dom('После нажатия появляется «Привет!»', 'click("#hello"); await wait(50); return out().includes("Привет!") || "После нажатия нет сообщения «Привет!»";')],
                solution="let button = document.querySelector('#hello')\n\nbutton.addEventListener('click', function () {\n    alert('Привет!')\n})\n"),
            task('Сайт с рыцарями', P(
                'Создай сайт по картинке, а потом добавь анимацию появления рыцарей. '
                'Картинки: <a href="img/knights/kn_1.png" target="_blank">левый рыцарь</a>, '
                '<a href="img/knights/kn_2.png" target="_blank">правый рыцарь</a>. '
                'Макет можно <a href="img/17.xd">скачать для Adobe XD</a>.'),
                level=3, local=True, images=[('img/17.png', 'Сайт с рыцарями'), ('img/knights/17.gif', 'Анимация рыцарей')],
                answer_link='lesson_17_homework.html'),
        ]),
    ],
    links=[
        ('Полезные ссылки', [
            ('Первые шаги в JavaScript', 'https://developer.mozilla.org/ru/docs/Learn/JavaScript/%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B5_%D1%88%D0%B0%D0%B3%D0%B8'),
            ('Примеры применения JavaScript', 'https://www.creativebloq.com/web-design/examples-of-javascript-1233964'),
            ('Тест для 17 урока', 'web_tests/lesson_17/index.html', 'test'),
        ]),
        ('Что почитать', [
            ('Основы JavaScript', 'https://developer.mozilla.org/ru/docs/Learn/Getting_started_with_the_web/JavaScript_basics', 'read'),
            ('DOM-дерево', 'https://learn.javascript.ru/dom-nodes', 'read'),
        ]),
    ],
)

# ------------------------------------------------------------------ Урок 18
L18 = dict(
    id='l18', file='lesson_18_adv.html', num='18', course='js', mode='js',
    short='Типы данных: числа и строки',
    title='Основные типы данных в JavaScript',
    about='let, числа, строки, slice, typeof',
    lead='Создаём переменные, считаем расстояния и режем строки на кусочки.',
    sections=[
        sec('Где писать JavaScript-код', emoji='🧭', items=[
            note('Короткие примеры удобно пробовать прямо в консоли браузера (<kbd>F12</kbd> → Console), '
                 'а задания ниже можно решать в редакторе на странице.', 'info'),
            images(('img/l18_how.png', 'Как начать писать код')),
        ]),
        sec('Задания', emoji='🔢', items=[
            task('От Москвы до Санкт-Петербурга', P(
                'Расстояние от Москвы до Санкт-Петербурга — <b>705 км</b>. Создай переменные и вычисли это расстояние '
                'в сантиметрах (переменная <code>inCentimeters</code>) и в миллиметрах (<code>inMillimeters</code>).'),
                level=1, images=[('img/l18_q1.png', 'Вопрос 1')], answer_pages=['lesson_18_ans_1.html'],
                starter="let meter = 1000\nlet centimeter = 100\nlet toSaintPetersburg = meter * 705\n\n",
                tests=[var_is('inCentimeters', '70500000'), var_is('inMillimeters', '705000000')],
                solution="let meter = 1000\nlet centimeter = 100\nlet toSaintPetersburg = meter * 705\n\n"
                         "let inCentimeters = toSaintPetersburg * centimeter\nlet millimeter = 10\n"
                         "let inMillimeters = inCentimeters * millimeter\nconsole.log(inCentimeters, inMillimeters)\n"),
            task('Переведи в мили', P(
                'В одной миле <b>1.6 км</b>. Переведи 705 км в мили и сохрани ответ в переменную <code>toSaintPetersburgMile</code>.'),
                level=1, images=[('img/l18_q2.png', 'Вопрос 2')], answer_pages=['lesson_18_ans_2.html'],
                starter="let kilInMile = 1.6\n",
                tests=[var_is('toSaintPetersburgMile', '440.625')],
                solution="let kilInMile = 1.6\nlet toSaintPetersburgMile = 705 / kilInMile\nconsole.log(toSaintPetersburgMile)\n"),
            task('Срезы строки', P(
                'С помощью <code>slice()</code> сохрани в переменные кусочки строки:',
                UL('<code>word1</code> — <code>"Probably"</code>',
                   '<code>word3</code> — <code>"LONGEST"</code> (заглавными буквами — <code>toUpperCase()</code>)',
                   '<code>what</code> — <code>" string you ever seen"</code> (с пробелом в начале)')),
                level=2, images=[('img/l18_q3.png', 'Вопрос 3')], answer_pages=['lesson_18_ans_3.html'],
                starter="let longestString = 'Probably the longest string you ever seen'\n",
                tests=[var_is('word1', "'Probably'"), var_is('word3', "'LONGEST'"), var_is('what', "' string you ever seen'")],
                solution="let longestString = 'Probably the longest string you ever seen'\n\n"
                         "let word1 = longestString.slice(0, 8)\nlet word3 = longestString.slice(13, 20).toUpperCase()\n"
                         "let what = longestString.slice(20)\nconsole.log(word1, word3, what)\n"),
            task('Арифметика с переменными', P(
                'Создай переменную <code>number</code>, равную <b>сумме</b> <code>nOne</code> и <code>nTwo</code>. '
                'Потом <b>прибавь к ней 1</b>, а затем <b>увеличь в 3 раза</b>. В конце должно получиться 12.'),
                level=1, images=[('img/l18_q4.png', 'Вопрос 4')], answer_pages=['lesson_18_ans_4.html'],
                starter="let nOne = 1\nlet nTwo = 2\n",
                tests=[var_is('number', '12'), code_has(r'nOne\s*\+\s*nTwo', 'number — это сумма nOne и nTwo'),
                       code_has(r'(\+\+|\+=\s*1|\*=\s*3|\*\s*3)', 'Использованы операции с переменной')],
                solution="let nOne = 1\nlet nTwo = 2\n\nlet number = nOne + nTwo\nnumber += 1\nnumber *= 3\nconsole.log(number)\n"),
            task('Сколько дней я живу', P(
                'Переменная <code>age</code> хранит твой возраст. Выведи в консоль, сколько это <b>дней</b> '
                '(считаем, что в году 365 дней), и сколько <b>часов</b>.'),
                level=1, new=True, starter="let age = 12\n",
                tests=[io([], ['4380', '105120'])],
                solution="let age = 12\nlet days = age * 365\nconsole.log(days)\nconsole.log(days * 24)\n"),
            task('Какой это тип?', P(
                'С помощью <code>typeof</code> выведи тип каждого значения: <code>42</code>, <code>\'кот\'</code>, '
                '<code>true</code> и переменной, которой ничего не присвоили.'),
                level=1, new=True, starter="let nothing\n",
                tests=[io([], ['number', 'string', 'boolean', 'undefined']), code_has('typeof', 'Используется typeof')],
                solution="let nothing\nconsole.log(typeof 42)\nconsole.log(typeof 'кот')\nconsole.log(typeof true)\nconsole.log(typeof nothing)\n"),
            task('Шаблонная строка', P(
                'Выведи фразу <b>Меня зовут Аня, мне 12 лет</b>, подставив переменные в шаблонную строку: '
                '<code>`Меня зовут ${name}...`</code> (кавычки — обратные, клавиша <kbd>Ё</kbd>).'),
                level=2, new=True, starter="let name = 'Аня'\nlet age = 12\n",
                tests=[io([], ['Меня зовут Аня, мне 12 лет']), code_has(r'`[^`]*\$\{', 'Используется шаблонная строка ${...}')],
                solution="let name = 'Аня'\nlet age = 12\nconsole.log(`Меня зовут ${name}, мне ${age} лет`)\n"),
        ]),
    ],
    links=[
        ('Полезные ссылки', [('Тест для 18 урока', 'web_tests/lesson_18/18.html', 'test')]),
        ('Что почитать', [
            ('Тип данных — число', 'https://learn.javascript.ru/types#chislo', 'read'),
            ('Арифметические операции', 'https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Operators/Arithmetic_Operators', 'read'),
            ('Тип данных — строка', 'https://learn.javascript.ru/types#stroka', 'read'),
            ('Длина строки', 'https://learn.javascript.ru/string#dlina-stroki', 'read'),
            ('Индексация строки', 'https://learn.javascript.ru/string#dostup-k-simvolam', 'read'),
            ('Срез строки (slice)', 'https://learn.javascript.ru/string#poluchenie-podstroki', 'read'),
            ('Все типы данных', 'https://learn.javascript.ru/types', 'read'),
        ]),
        practice_js('Строки (string)', 'strings1', 'strings2', 'strings3'),
        practice_js('Методы строк', *[f'string_methods{i}' for i in range(1, 6)]),
    ],
)

# ------------------------------------------------------------------ Урок 19
L19 = dict(
    id='l19', file='lesson_19_adv.html', num='19', course='js', mode='js',
    short='Массивы',
    title='Массивы (array)',
    about='push, pop, shift, unshift, индексы, length',
    lead='Массив — это список значений под одним именем. Учимся добавлять, удалять и доставать элементы.',
    sections=[
        sec('Задания', emoji='📚', items=[
            task('Что получится?', P('Подумай, что будет в массиве <code>vegetables</code> после <code>push</code>. Потом проверь себя, запустив код.'),
                 level=1, images=[('img/l19_q1.png', 'Вопрос 1')], answer_pages=['lesson_19_ans_1.html'],
                 starter="let vegetables = ['cucumber', 'pepper', 'potato']\nvegetables.push('onion')\nconsole.log(vegetables)\n"),
            task('Любимые фильмы', P('Выполни по шагам, используя <code>.push()</code>, <code>.pop()</code>, <code>.shift()</code>, <code>.unshift()</code>:') +
                 '<ol><li>Создай пустой массив <code>favMovies</code></li><li>Добавь в него два элемента: <code>\'movie 1\'</code> и <code>\'movie 2\'</code></li>'
                 '<li>Добавь <code>\'movie 3\'</code> в начало массива</li><li>Замени последний элемент на <code>\'change\'</code></li></ol>',
                 level=1, images=[('img/l19_q2.png', 'Вопрос 2')], answer_pages=['lesson_19_ans_2.html'],
                 starter="let favMovies = []\n",
                 tests=[var_is('favMovies', "['movie 3', 'movie 1', 'change']"), code_has(r'\.push\(', 'Используется push'),
                        code_has(r'\.unshift\(', 'Используется unshift')],
                 solution="let favMovies = []\nfavMovies.push('movie 1', 'movie 2')\nfavMovies.unshift('movie 3')\nfavMovies.pop()\n"
                          "favMovies.push('change')\nconsole.log(favMovies)\n"),
            task('Достань элементы', P(
                'Достань из массива <code>randArr</code> по индексам и сохрани в переменные: '
                '<code>a</code> — <code>"10Hello"</code>, <code>b</code> — <code>2</code>, <code>c</code> — <code>25</code>.'),
                level=2, images=[('img/l19_q3.png', 'Вопрос 3')], answer_pages=['lesson_19_ans_3.html'],
                starter="let randArr = [1, [10 + 'Hello', 'World'], [2], 25]\n",
                hint=P('Массив внутри массива: <code>randArr[1][0]</code> — нулевой элемент первого элемента.'),
                tests=[var_is('a', "'10Hello'"), var_is('b', '2'), var_is('c', '25'),
                       code_has(r'randArr\[', 'Значения достаются из randArr по индексам')],
                solution="let randArr = [1, [10 + 'Hello', 'World'], [2], 25]\n\nlet a = randArr[1][0]\nlet b = randArr[2][0]\nlet c = randArr[3]\nconsole.log(a, b, c)\n"),
            task('Массив в массиве', P('Что вернёт <code>array2[2][0]</code>? Сначала подумай, потом проверь.'),
                 level=1, images=[('img/l19_q4.png', 'Вопрос 4')], answer_pages=['lesson_19_ans_4.html'],
                 starter="let array1 = [10 * 5]\nlet array2 = [1, 2, array1, 3]\nconsole.log(array2[2][0])\n"),
            task('Длина и последний элемент', P(
                'Выведи в консоль <b>количество</b> цветов в массиве и <b>последний</b> цвет. '
                'Последний элемент получи через <code>colors.length</code>, а не цифрой — ведь массив может измениться!'),
                level=1, new=True, starter="let colors = ['красный', 'оранжевый', 'жёлтый', 'зелёный', 'синий']\n",
                tests=[io([], ['5', 'синий']), code_has(r'colors\.length\s*-\s*1', 'Последний элемент — colors[colors.length - 1]')],
                solution="let colors = ['красный', 'оранжевый', 'жёлтый', 'зелёный', 'синий']\nconsole.log(colors.length)\nconsole.log(colors[colors.length - 1])\n"),
            task('Собери слово', P(
                'Склей буквы из массива в одно слово методом <code>join(\'\')</code> и выведи его. '
                'Потом проверь методом <code>includes()</code>, есть ли в массиве буква <code>\'О\'</code>.'),
                level=2, new=True, starter="let letters = ['К', 'И', 'Д', 'К', 'О', 'Д']\n",
                tests=[io([], ['КИДКОД', 'true']), code_has(r'\.join\(', 'Используется join'), code_has(r'\.includes\(', 'Используется includes')],
                solution="let letters = ['К', 'И', 'Д', 'К', 'О', 'Д']\nconsole.log(letters.join(''))\nconsole.log(letters.includes('О'))\n"),
        ]),
    ],
    links=[
        ('Полезные ссылки', [('Тест для 19 урока', 'web_tests/lesson_19/19.html', 'test')]),
        ('Что почитать', [
            ('Всё о массивах #1', 'https://developer.mozilla.org/ru/docs/Learn/JavaScript/%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B5_%D1%88%D0%B0%D0%B3%D0%B8/Arrays', 'read'),
            ('Всё о массивах #2', 'https://learn.javascript.ru/array', 'read'),
            ('Методы массивов', 'https://learn.javascript.ru/array-methods', 'read'),
        ]),
        practice_js('Массивы (array)', *[f'arrays{i}' for i in range(1, 4)]),
        practice_js('Методы массивов', *[f'array_methods{i}' for i in range(1, 4)]),
    ],
)

# ------------------------------------------------------------------ Урок 20
L20 = dict(
    id='l20', file='lesson_20_adv.html', num='20', course='js', mode='js',
    short='Объекты',
    title='Объекты (object)',
    about='Ключи и значения, вложенные объекты, for...in',
    lead='Объект хранит данные с подписями: имя героя, его здоровье, инвентарь. Учимся создавать и менять объекты.',
    sections=[
        sec('Задания', emoji='🗃️', items=[
            task('Мои любимые фильмы или игры', P(
                'Создай объект <code>favorites</code> с твоими любимыми фильмами или играми — <b>минимум 5</b> штук, например:'),
                level=1, images=[('img/l20_q1.png', 'Вопрос 1')], starter="let favorites = {\n    \n}\n",
                tests=[dom('Есть объект favorites', 'return (typeof favorites === "object" && favorites !== null && !Array.isArray(favorites)) || "Создай объект favorites = { ... }";'),
                       dom('В объекте не меньше 5 записей', 'return Object.keys(favorites).length >= 5 || "Сейчас записей: " + Object.keys(favorites).length;')],
                solution="let favorites = {\n    game1: 'Minecraft',\n    game2: 'Roblox',\n    game3: 'Terraria',\n"
                         "    movie1: 'Шрек',\n    movie2: 'Холодное сердце'\n}\nconsole.log(favorites)\n"),
            task('Что получится?', P('Какие значения выведутся? Запиши ответы, а потом проверь, запустив код.'),
                 level=2, images=[('img/l20_q2.png', 'Вопрос 2')], answer_pages=['lesson_20_ans_1.html'],
                 starter="let randObj = {\n    'first': {\n        inner: [0, 1, 2]\n    },\n    second: ['a', {'inside array': 'b'}],\n"
                         "    'last?': ['foo', 'bar', 'Hello', ['maybe not', {'inner inner': 3.14}]]\n}\n\n"
                         "console.log(randObj.first['inner'])\nconsole.log(randObj['second'][1]['inside array'])\n"
                         "console.log(randObj['last?'][4])\nconsole.log(randObj['last?'][3][1]['inner inner'])\n"
                         "randObj.addedKey = [1, 2, [3]]\nconsole.log(randObj.addedKey[2][0])\nconsole.log(randObj)\n"),
            task('Инвентарь мага', P(
                'Выполни все действия с объектом <code>mage</code> по картинке. Какие значения будут у <code>mage.xp</code>, '
                '<code>mage.hp</code>, <code>mage.items</code> и <code>stash</code> в конце?'),
                level=2, images=[('img/l20_q3.png', 'Вопрос 3')], answer_pages=['lesson_20_ans_2.html'],
                starter="let mage = {\n    name: 'name',\n    items: [],\n    xp: 0,\n    hp: 10\n}\n\n",
                tests=[var_is('mage.xp', '6'), var_is('mage.hp', '16'), var_is('mage.items', "['staff']"), var_is('stash', "'cloak'")],
                solution="let mage = {\n    name: 'name',\n    items: [],\n    xp: 0,\n    hp: 10\n}\n\n"
                         "mage.items.push('staff')\nmage.items.push('cloak')\nlet stash = mage.items.pop()\nmage.xp++\nmage.xp += 5\n"
                         "mage.hp = mage.hp + mage.xp\nconsole.log(mage)\n"),
            task('Герой повышает уровень', P(
                'У героя уровень 1 и пустой инвентарь. Повысь ему уровень на 1, положи в инвентарь <code>\'меч\'</code> '
                'и выведи фразу <b>Артур — уровень 2</b>, взяв имя и уровень из объекта.'),
                level=1, new=True, starter="let hero = {\n    name: 'Артур',\n    level: 1,\n    items: []\n}\n",
                tests=[var_is('hero.level', '2'), dom('В инвентаре есть меч', 'return hero.items.includes("меч") || "Добавь меч в hero.items";'),
                       io([], ['Артур — уровень 2']), code_has(r'hero\.name', 'Имя берётся из объекта (hero.name)')],
                solution="let hero = {\n    name: 'Артур',\n    level: 1,\n    items: []\n}\n\nhero.level += 1\nhero.items.push('меч')\n"
                         "console.log(hero.name + ' — уровень ' + hero.level)\n"),
            task('Ценник', P(
                'Выведи все товары и цены из объекта <code>prices</code> — каждый с новой строки, в виде '
                '<b>яблоко: 50</b>. Используй цикл <code>for (let key in prices)</code>.'),
                level=2, new=True, starter="let prices = {\n    яблоко: 50,\n    банан: 30,\n    груша: 70\n}\n",
                tests=[io([], ['яблоко: 50', 'банан: 30', 'груша: 70']), code_has(r'for\s*\(\s*(let|const|var)\s+\w+\s+in\s+prices', 'Используется for...in')],
                solution="let prices = {\n    яблоко: 50,\n    банан: 30,\n    груша: 70\n}\n\nfor (let key in prices) {\n    console.log(key + ': ' + prices[key])\n}\n"),
        ]),
    ],
    links=[
        ('Полезные ссылки', [('Тест для 20 урока', 'web_tests/lesson_20/20.html', 'test')]),
        ('Что почитать', [
            ('Основная информация об объектах', 'https://developer.mozilla.org/ru/docs/Learn/JavaScript/%D0%9E%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D1%8B/%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D1%8B', 'read'),
            ('Всё об объектах', 'https://learn.javascript.ru/object', 'read'),
        ]),
        practice_js('Где потренироваться', 'objects1', 'objects2', 'objects3'),
    ],
)

# ------------------------------------------------------------------ Урок 21
L21_NAME = """let name = prompt('Введите имя персонажа и мы проверим, подходит ли оно вам: ')

if (name.length === 0) {
    alert('Вы не ввели имя!')
} else if (name.length <= 3) {
    alert('Оно слишком короткое, попробуйте ввести больше чем ' + name.length + ' символа')
} else if (name.length <= 6) {
    alert(name + ' это имя идеально вам подходит!')
} else {
    alert('Оно слишком длинное, попробуйте ввести меньше чем ' + name.length + ' символов')
}
"""

L21_RIDDLE = """let question = ['Странный дождь порой идёт: сотней струй он кверху бьёт.', 'фонтан']

let answer = prompt('Отгадайте загадку: ' + question[0] + ' Ваш ответ: ')

if (answer.toLowerCase() === question[1]) {
    alert('Правильный ответ!')
} else {
    alert('Ответ неверный, правильный ответ: ' + question[1])
}
"""

L21 = dict(
    id='l21', file='lesson_21_adv.html', num='21', course='js', mode='js',
    short='Условия и сравнения',
    title='Сравнения, ветвления и типы данных ч. 2',
    about='if / else, prompt, Number, boolean, null',
    lead='Программа начинает «думать»: в зависимости от ответа пользователя делает разные вещи.',
    sections=[
        sec('Задания', emoji='🔀', items=[
            note('Во всех заданиях результат выводим через <a href="https://developer.mozilla.org/ru/docs/Web/API/Window/alert" target="_blank" rel="noopener">alert()</a>. '
                 '<code>prompt()</code> всегда возвращает <b>строку</b> — чтобы получить число, используй '
                 '<a href="https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/parseInt" target="_blank" rel="noopener">parseInt()</a> '
                 'или <a href="https://learn.javascript.ru/type-conversions#chislennoe-preobrazovanie" target="_blank" rel="noopener">Number()</a>.', 'info'),
            task('Сумма или произведение', P(
                'Программа спрашивает у пользователя два числа. Если их сумма <b>больше 1000</b> — выводит '
                '<b>Сумма этих чисел: …</b>, иначе — <b>Произведение этих чисел: …</b>'),
                level=1, images=[('img/l21_q1.png', 'Ввод'), ('img/l21_q1_2.png', 'Ввод'), ('img/l21_q1_3.png', 'Результат')],
                answer_pages=['lesson_21_ans_1.html'],
                tests=[io([600, 500], ['Сумма этих чисел: 1100'], ['Произведение']),
                       io([10, 20], ['Произведение этих чисел: 200'], ['Сумма']),
                       io([1000, 0], ['Произведение этих чисел: 0'], ['Сумма'])],
                solution=body_script('lesson_21_ans_1.html')),
            task('Проверка имени персонажа', P('Программа спрашивает имя персонажа и отвечает по-разному:',
                UL('ничего не ввели — <b>Вы не ввели имя!</b>',
                   'от 1 до 3 символов — <b>…слишком короткое…</b>',
                   'от 4 до 6 символов — <b>&lt;имя&gt; это имя идеально вам подходит!</b>',
                   'больше 6 символов — <b>…слишком длинное…</b>')),
                level=2, images=[('img/l21_q2.png', 'Ввод'), ('img/l21_q2_2.png', 'Результат'), ('img/l21_q2_5.png', 'от 1 до 3 символов'),
                                 ('img/l21_q2_3.png', 'от 4 до 6 символов'), ('img/l21_q2_4.png', 'если ничего не ввели')],
                answer_pages=['lesson_21_ans_2.html'],
                tests=[io([''], ['Вы не ввели имя!']), io(['Ян'], ['слишком короткое']), io(['Оля'], ['слишком короткое']),
                       io(['Анна'], ['Анна это имя идеально вам подходит!']), io(['Максим'], ['идеально']),
                       io(['Константин'], ['слишком длинное'])],
                solution=L21_NAME),
            task('Загадка', P(
                'Программа задаёт загадку и отвечает <b>Правильный ответ!</b> или '
                '<b>Ответ неверный, правильный ответ: фонтан</b>. Ответ «Фонтан» с большой буквы тоже должен засчитываться.'),
                level=1, images=[('img/l21_q3_1.png', 'Загадка'), ('img/l21_q3_2.png', 'Результат')],
                answer_pages=['lesson_21_ans_3.html'],
                hint=P('Приведи ответ к маленьким буквам: <code>answer.toLowerCase()</code>'),
                tests=[io(['фонтан'], ['Правильный ответ!'], ['неверный']), io(['Фонтан'], ['Правильный ответ!'], ['неверный']),
                       io(['дождь'], ['Ответ неверный, правильный ответ: фонтан'])],
                solution=L21_RIDDLE),
            task('Чётное или нечётное', P(
                'Спроси у пользователя число и выведи <b>Число чётное</b> или <b>Число нечётное</b>.'),
                level=1, new=True,
                hint=P('Остаток от деления на 2: <code>number % 2 === 0</code> — значит, чётное.'),
                tests=[io([4], ['Число чётное'], ['нечётное']), io([7], ['Число нечётное']), io([0], ['Число чётное'], ['нечётное'])],
                solution="let number = Number(prompt('Введите число: '))\n\nif (number % 2 === 0) {\n    alert('Число чётное')\n} else {\n    alert('Число нечётное')\n}\n"),
            task('Оценка за тест', P('Спроси, сколько баллов из 100 набрал ученик, и выведи оценку:',
                UL('90 и больше — <b>Оценка: 5</b>', '70–89 — <b>Оценка: 4</b>', '50–69 — <b>Оценка: 3</b>', 'меньше 50 — <b>Оценка: 2</b>')),
                level=2, new=True,
                tests=[io([95], ['Оценка: 5']), io([90], ['Оценка: 5']), io([75], ['Оценка: 4']), io([55], ['Оценка: 3']),
                       io([50], ['Оценка: 3']), io([10], ['Оценка: 2'])],
                solution="let score = Number(prompt('Сколько баллов ты набрал? '))\n\nif (score >= 90) {\n    alert('Оценка: 5')\n"
                         "} else if (score >= 70) {\n    alert('Оценка: 4')\n} else if (score >= 50) {\n    alert('Оценка: 3')\n"
                         "} else {\n    alert('Оценка: 2')\n}\n"),
            task('Високосный год', P(
                'Год високосный, если он делится на 4, но не делится на 100, <b>или</b> если делится на 400. '
                'Спроси год и выведи <b>Год високосный</b> или <b>Год не високосный</b>.'),
                level=3, new=True,
                hint=P('Логические операторы: <code>&amp;&amp;</code> — «и», <code>||</code> — «или».'),
                tests=[io([2024], ['Год високосный'], ['не високосный']), io([2023], ['Год не високосный']),
                       io([1900], ['Год не високосный']), io([2000], ['Год високосный'], ['не високосный'])],
                solution="let year = Number(prompt('Введите год: '))\n\nif ((year % 4 === 0 && year % 100 !== 0) || year % 400 === 0) {\n"
                         "    alert('Год високосный')\n} else {\n    alert('Год не високосный')\n}\n"),
        ]),
    ],
    links=[
        ('Полезные ссылки', [('Тест для 21 урока', 'web_tests/lesson_21/21.html', 'test')]),
        ('Что почитать', [
            ('Тип данных — null', 'https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/null', 'read'),
            ('Тип данных — undefined', 'https://developer.mozilla.org/ru/docs/Web/JavaScript/Reference/Global_Objects/undefined', 'read'),
            ('Тип данных — boolean', 'https://javascript.ru/basic/types#boolean', 'read'),
            ('Ветвления в JavaScript', 'https://learn.javascript.ru/ifelse', 'read'),
        ]),
        practice_js('Сравнения', *[f'comparisons{i}' for i in range(1, 5)]),
        practice_js('Ветвление', 'conditions1', 'conditions2'),
    ],
)

# ------------------------------------------------------------------ Урок 22
L22_RIDDLE = body_script('lesson_22_ans_1.html')
L22_GAME = body_script('lesson_22_ans_4.html')
L22_MINMAX = """let arr = [7, 12, 42, 66, 0, -7, 122, -7.5]
let max = arr[0]
let min = arr[0]

for (let i = 1; i < arr.length; i++) {
    if (arr[i] < min) {
        min = arr[i]
    }
    if (arr[i] > max) {
        max = arr[i]
    }
}

console.log('Минимальное: ' + min)
console.log('Максимальное: ' + max)
"""

L22 = dict(
    id='l22', file='lesson_22_adv.html', num='22', course='js', mode='js',
    short='Циклы',
    title='Циклы',
    about='while, for, break, перебор массива',
    lead='Циклы повторяют действия много раз: спрашивают, пока не ответят правильно, перебирают массивы, рисуют узоры.',
    sections=[
        sec('Задания', emoji='🔁', items=[
            JS_NOTE,
            task('Загадка с повтором', P(
                'Программа загадывает загадку <b>«Чем можно поделиться только один раз?»</b> и спрашивает ответ, '
                '<b>пока</b> пользователь не ответит правильно (<code>секретом</code>). На неправильный ответ пишет '
                '<b>Ответ неверный, попробуй ещё раз...</b>, на правильный — <b>секретом это правильный ответ! Молодец</b>. '
                'Используй цикл <code>while</code>.'),
                level=1, images=[('img/l22_q1.png', 'Вопрос'), ('img/l22_q1.gif', 'Как работает')],
                demo=L22_RIDDLE,
                tests=[io(['дружбой', 'секретом'], ['Ответ неверный', 'секретом это правильный ответ']),
                       io(['Секретом'], ['секретом это правильный ответ'], ['неверный']),
                       io(['а', 'б', 'в', 'секретом'], ['правильный ответ']), code_has(r'while\s*\(', 'Используется цикл while')],
                solution=L22_RIDDLE.replace('еще', 'ещё')),
            task('Самое большое и самое маленькое', P(
                'Найди в массиве самое большое и самое маленькое число с помощью цикла (без <code>Math.max</code>) и выведи '
                '<b>Минимальное: …</b> и <b>Максимальное: …</b>'),
                level=2, images=[('img/l22_q2.png', 'Вопрос'), ('img/l22_q2_2.png', 'Результат')], answer_pages=['lesson_22_ans_2.html'],
                starter="let arr = [7, 12, 42, 66, 0, -7, 122, -7.5]\n",
                tests=[io([], ['Минимальное: -7.5', 'Максимальное: 122']), code_has(r'for\s*\(', 'Используется цикл for'),
                       dom('Без Math.max и Math.min', 'return !/Math\\.(max|min)/.test(code) || "Реши с помощью цикла, без Math.max/Math.min";')],
                solution=L22_MINMAX),
            task('Сумма ряда чисел', P(
                'Спроси у пользователя число и выведи сумму всех чисел от 1 до него: '
                '<b>Сумма всех чисел у числа: 10. Равняется: 55</b>. '
                '<a href="https://www.yaklass.ru/p/algebra/9-klass/progressii-9139/arifmeticheskaia-progressiia-9141/re-9be60eb3-2e3a-4782-b724-d5bca94395dc" target="_blank" rel="noopener">Что такое арифметическая прогрессия</a>.'),
                level=1, images=[('img/l22_q3.png', 'Вопрос'), ('img/l22_q3_2.png', 'Ввод'), ('img/l22_q3_3.png', 'Результат')],
                answer_pages=['lesson_22_ans_3.html'],
                tests=[io([10], ['Равняется: 55']), io([100], ['Равняется: 5050']), io([1], ['Равняется: 1'])],
                solution=body_script('lesson_22_ans_3.html')),
            task('Одномерный мир', P(
                'Сделай мини-игру: в мире <code>[\'*\', \'_\', \'_\', \'_\']</code> персонаж <code>*</code> ходит налево '
                '(<code>left</code>) и направо (<code>right</code>). Перед каждым ходом покажи мир через '
                '<code>alert(field.join(\' \'))</code>. Если идти некуда — <b>Налево нельзя!</b> / <b>Направо нельзя!</b>. '
                'Команда <code>exit</code> (или «Отмена») — <b>Спасибо за игру!</b>'),
                level=3, images=[('img/l22_a4.gif', 'Пример')], demo=L22_GAME,
                tests=[io(['right', 'right', 'left', 'exit'], ['* _ _ _', '_ * _ _', '_ _ * _', 'Спасибо за игру!']),
                       io(['left', 'exit'], ['Налево нельзя!']), io(['right', 'right', 'right', 'right', 'exit'], ['_ _ _ *', 'Направо нельзя!']),
                       io([None], ['Спасибо за игру!'], label='«Отмена» заканчивает игру')],
                solution=L22_GAME),
            task('Таблица умножения', P(
                'Спроси число и выведи для него таблицу умножения от 1 до 10 в виде <b>7 x 3 = 21</b> — каждую строку через <code>console.log</code>.'),
                level=1, new=True,
                tests=[io([7], ['7 x 1 = 7', '7 x 5 = 35', '7 x 10 = 70'], ['7 x 11']), io([2], ['2 x 9 = 18'])],
                solution="let n = Number(prompt('Какую таблицу умножения показать? '))\n\nfor (let i = 1; i <= 10; i++) {\n    console.log(n + ' x ' + i + ' = ' + n * i)\n}\n"),
            task('FizzBuzz', P(
                'Выведи числа от 1 до 15, но вместо чисел, которые делятся на 3, пиши <b>Fizz</b>, на 5 — <b>Buzz</b>, '
                'а на 3 и 5 сразу — <b>FizzBuzz</b>. Это знаменитая задача с собеседований программистов!'),
                level=2, new=True,
                tests=[dom('Выведено ровно 15 строк', 'return lines().length === 15 || "Сейчас строк: " + lines().length;'),
                       dom('Правильная последовательность', 'const want = ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]; const got = lines().map(s => s.trim()); return want.every((w, i) => got[i] === w) || "Ожидалось: " + want.join(", ") + "\\nПолучилось: " + got.join(", ");')],
                solution="for (let i = 1; i <= 15; i++) {\n    if (i % 15 === 0) {\n        console.log('FizzBuzz')\n    } else if (i % 3 === 0) {\n"
                         "        console.log('Fizz')\n    } else if (i % 5 === 0) {\n        console.log('Buzz')\n    } else {\n        console.log(i)\n    }\n}\n"),
            task('Звёздная лесенка', P(
                'Спроси высоту лесенки и нарисуй её звёздочками — в первой строке одна <code>*</code>, во второй две и так далее.'),
                level=2, new=True, examples=[('Для высоты 4', '*\n**\n***\n****')],
                tests=[dom('Лесенка высотой 4', 'const got = lines().filter(s => s.includes("*")).map(s => s.trim()); return (got.join("|") === "*|**|***|****") || "Получилось:\\n" + got.join("\\n");', inputs=[4]),
                       dom('Лесенка высотой 2', 'const got = lines().filter(s => s.includes("*")).map(s => s.trim()); return (got.join("|") === "*|**") || "Получилось:\\n" + got.join("\\n");', inputs=[2])],
                solution="let height = Number(prompt('Высота лесенки: '))\nlet line = ''\n\nfor (let i = 1; i <= height; i++) {\n    line += '*'\n    console.log(line)\n}\n"),
        ]),
    ],
    links=[
        ('Полезные ссылки', [('Тест для 22 урока', 'web_tests/lesson_22/22.html', 'test')]),
        ('Что почитать', [
            ('Циклы', 'https://learn.javascript.ru/while-for', 'read'),
            ('Циклы и итерации', 'https://developer.mozilla.org/ru/docs/Web/JavaScript/Guide/%D0%A6%D0%B8%D0%BA%D0%BB%D1%8B_%D0%B8_%D0%B8%D1%82%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8', 'read'),
        ]),
        practice_js('Циклы', 'loops1', 'loops2', 'loop_while1', 'loop_while2'),
    ],
)

# ------------------------------------------------------------------ Урок 23
L23_ELEPHANT = body_script('lesson_23_ans_1.html')

L23 = dict(
    id='l23', file='lesson_23_adv.html', num='23', course='js', mode='js',
    short='Функции',
    title='Функции',
    about='function, return, параметры, стрелочные функции',
    lead='Функция — это «рецепт», который можно вызывать много раз. Учимся писать свои функции и возвращать из них результат.',
    sections=[
        sec('Задания', emoji='🧩', items=[
            task('Купи слона', P(
                'Программа предлагает купить слона 🐘. Что бы ни ответил пользователь, она отвечает: '
                '<b>Все говорят &lt;ответ&gt; а ты купи 🐘</b>. Остановиться можно, только нажав «Отмена» '
                '(тогда <code>prompt</code> вернёт <code>null</code>). Проверку ответа вынеси в функцию <code>buyElephant</code>.'),
                level=1, images=[('img/l23_a1.gif', 'Как работает')], demo=L23_ELEPHANT,
                tests=[io(['нет', None], ['Купи 🐘', 'Все говорят нет а ты купи 🐘']),
                       io(['не хочу', 'отстань', None], ['Все говорят не хочу а ты купи 🐘', 'Все говорят отстань а ты купи 🐘']),
                       code_has(r'function\s+buyElephant|buyElephant\s*=', 'Есть функция buyElephant')],
                solution=L23_ELEPHANT),
            task('Квадрат числа', P(
                'Напиши функцию <code>pow(x)</code>, которая <b>возвращает</b> квадрат числа. '
                'Спроси число у пользователя и выведи <b>Ответ: …</b>'),
                level=1, images=[('img/l23_q1.png', 'Ввод'), ('img/l23_q1_2.png', 'Результат')], answer_pages=['lesson_23_ans_2.html'],
                tests=[call('pow(5)', '25'), call('pow(-3)', '9'), io([4], ['Ответ: 16'])],
                solution="function pow(x) {\n    return x * x\n}\n\nlet userInput = Number(prompt('Введите число и я возведу его в квадрат: '))\nalert('Ответ: ' + pow(userInput))\n"),
            task('Зеркальный текст', P(
                'Напиши функцию <code>reverseString(string)</code>, которая возвращает строку задом наперёд (с помощью цикла). '
                'Спроси текст у пользователя и выведи <b>Результат: …</b>'),
                level=2, images=[('img/l23_q2.png', 'Ввод'), ('img/l23_q2_2.png', 'Результат')], answer_pages=['lesson_23_ans_3.html'],
                tests=[call("reverseString('abc')", "'cba'"), call("reverseString('')", "''"), io(['Привет'], ['Результат: тевирП'])],
                solution=body_script('lesson_23_ans_3.html')),
            task('Вечеринка с пиццей', P(
                'Напиши функцию <code>pizzaCount(pizza, people)</code>, которая возвращает массив из двух строк: '
                'смайлики 😛 по числу гостей и 🍕 по числу пицц. Спроси, сколько будет людей и пицц, и выведи '
                '<b>Будет людей - 😛😛😛 и пицц - 🍕🍕</b>.'),
                level=2, images=[('img/l23_q3.png', 'Ввод'), ('img/l23_q3_2.png', 'Ввод'), ('img/l23_q3_3.png', 'Результат')],
                answer_pages=['lesson_23_ans_4.html'],
                tests=[call('pizzaCount(2, 3)', "['😛😛😛', '🍕🍕']"), io([3, 2], ['Будет людей - 😛😛😛 и пицц - 🍕🍕'])],
                solution=body_script('lesson_23_ans_4.html')),
            task('Самое большое из трёх', P(
                'Напиши функцию <code>maxOfThree(a, b, c)</code>, которая возвращает самое большое из трёх чисел. '
                'Используй <code>if</code>, а не <code>Math.max</code>.'),
                level=1, new=True, starter="function maxOfThree(a, b, c) {\n    // твой код\n}\n\nconsole.log(maxOfThree(1, 5, 3))\n",
                tests=[call('maxOfThree(1, 5, 3)', '5'), call('maxOfThree(9, 2, 3)', '9'), call('maxOfThree(1, 2, 8)', '8'),
                       call('maxOfThree(-1, -5, -3)', '-1'), call('maxOfThree(7, 7, 2)', '7'),
                       dom('Без Math.max', 'return !/Math\\.max/.test(code) || "Реши без Math.max";')],
                solution="function maxOfThree(a, b, c) {\n    let max = a\n    if (b > max) {\n        max = b\n    }\n    if (c > max) {\n        max = c\n    }\n    return max\n}\n\nconsole.log(maxOfThree(1, 5, 3))\n"),
            task('Стрелочная функция', P(
                'Запиши функцию <code>isEven</code> в виде <b>стрелочной</b> функции: <code>const isEven = (n) =&gt; ...</code>. '
                'Она возвращает <code>true</code>, если число чётное, и <code>false</code>, если нет.'),
                level=2, new=True, starter="const isEven = \n\nconsole.log(isEven(4))\n",
                tests=[call('isEven(4)', 'true'), call('isEven(7)', 'false'), call('isEven(0)', 'true'), code_has('=>', 'Функция стрелочная (=>)')],
                solution="const isEven = (n) => n % 2 === 0\n\nconsole.log(isEven(4))\n"),
            task('Приветствие по умолчанию', P(
                'Напиши функцию <code>greet(name)</code>, которая возвращает строку <b>Привет, Аня!</b>. '
                'Если имя не передали, функция должна вернуть <b>Привет, друг!</b> — используй значение параметра по умолчанию: '
                '<code>function greet(name = \'друг\')</code>.'),
                level=2, new=True, starter="function greet(name) {\n    \n}\n\nconsole.log(greet('Аня'))\nconsole.log(greet())\n",
                tests=[call("greet('Аня')", "'Привет, Аня!'"), call('greet()', "'Привет, друг!'"), call("greet('Гвидо')", "'Привет, Гвидо!'")],
                solution="function greet(name = 'друг') {\n    return 'Привет, ' + name + '!'\n}\n\nconsole.log(greet('Аня'))\nconsole.log(greet())\n"),
        ]),
    ],
    links=[
        ('Полезные ссылки', [('Тест для 23 урока', 'web_tests/lesson_23/23.html', 'test')]),
        ('Что почитать', [
            ('Всё о функциях', 'https://learn.javascript.ru/function-basics', 'read'),
            ('Стек вызовов', 'https://developer.mozilla.org/ru/docs/%D0%A1%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8C/Call_stack', 'read'),
            ('Визуализатор кода для JavaScript', 'http://pythontutor.com/javascript.html#mode=edit', 'tool'),
        ]),
        practice_js('Функции', *[f'functions{i}' for i in range(1, 5)]),
    ],
)

# ------------------------------------------------------------------ Урок 24
DOM1_TABLE = table(['Как вызвать', 'Что делает'], [
    ['<code>document.all</code>', 'HTML-коллекция со всеми элементами на странице'],
    ['<code>document.title</code>', 'Заголовок (title) документа'],
    ['<code>document.head</code>, <code>document.body</code>', 'HTML выбранной части'],
    ['<code>document.URL</code>', 'Ссылка в адресной строке'],
    ['<code>document.forms</code>', 'Все формы в документе'],
    ['<code>ELEMENT.innerHTML</code>', 'Изменить HTML элемента'],
    ['<code>ELEMENT.textContent</code>', 'Изменить текст у элемента'],
    ['<code>document.getElementById(\'ID\')</code>', 'Найти элемент по id (вернёт 1 элемент)'],
    ['<code>document.getElementsByClassName(\'CLASS\')</code>', 'Найти элементы по классу (вернёт коллекцию)'],
    ['<code>document.getElementsByTagName(\'TAG\')</code>', 'Найти элементы по тегу (вернёт коллекцию)'],
    ['<code>document.querySelector(\'SELECTOR\')</code>', 'Найти элемент по селектору (вернёт 1 элемент): <code>.class</code>, <code>#id</code>, <code>tag</code>'],
    ['<code>document.querySelectorAll(\'SELECTOR\')</code>', 'Найти все элементы по селектору'],
    ['<code>ELEMENT.style</code>', 'Изменить стиль: <code>element.style.color = \'red\'</code>'],
    ['<code>ELEMENT.parentNode</code>', 'Родительский элемент'],
    ['<code>ELEMENT.children</code>', 'Все вложенные в элемент теги'],
], caption='Всё, что написано ЗАГЛАВНЫМИ буквами, — заранее выбранный элемент DOM-дерева')

L24 = dict(
    id='l24', file='lesson_24_adv.html', num='24', course='js', mode='js',
    short='DOM, часть 1',
    title='Управление элементами на странице. DOM, часть 1',
    about='querySelector, textContent, innerHTML, style',
    lead='DOM — это страница глазами JavaScript. Находим элементы и меняем их текст, HTML и стили.',
    sections=[
        sec('Свойства и методы DOM-дерева', emoji='🌳', items=[DOM1_TABLE]),
        sec('Задания', emoji='🛠️', items=[
            task('Страница по заказу', P(
                'На странице есть заголовок и абзац с текстом <b>ERROR</b>. Спроси у пользователя по очереди: '
                'текст заголовка, цвет заголовка, текст абзаца и цвет абзаца — и поменяй их. '
                'Для изменения текста и цвета напиши функции <code>text(element, t)</code> и <code>style(element, s)</code>.'),
                level=2, images=[('img/l24_q1.png', 'Шаг 1'), ('img/l24_q1_2.png', 'Шаг 2'), ('img/l24_q1_3.png', 'Шаг 3'),
                                 ('img/l24_q1_4.png', 'Шаг 4'), ('img/l24_q1_5.png', 'Результат')],
                fixture='<h1>ERROR</h1>\n<p>ERROR</p>', answer_link='lesson_24_ans_1.html',
                tests=[dom('Заголовок получил текст и цвет', 'return (text("h1") === "Привет" && cssIs("h1", "color", "red")) || "Заголовок: «" + text("h1") + "», цвет " + css("h1", "color");', inputs=['Привет', 'red', 'Как дела?', 'blue']),
                       dom('Абзац получил текст и цвет', 'return (text("p") === "Как дела?" && cssIs("p", "color", "blue")) || "Абзац: «" + text("p") + "», цвет " + css("p", "color");', inputs=['Привет', 'red', 'Как дела?', 'blue']),
                       code_has(r'function\s+text|text\s*=\s*(function|\()', 'Есть функция text'),
                       code_has(r'function\s+style|style\s*=\s*(function|\()', 'Есть функция style')],
                solution=body_script('lesson_24_ans_1.html')),
            task('Список из массива', P(
                'Выведи фрукты из массива на страницу: для каждого создай пункт <code>&lt;li&gt;</code> внутри '
                '<code>&lt;ul id="list"&gt;</code>. Используй цикл — фруктов может стать больше!'),
                level=1, new=True, fixture='<h2>Мои фрукты</h2>\n<ul id="list"></ul>',
                starter="let fruits = ['Яблоко', 'Банан', 'Вишня']\nlet list = document.querySelector('#list')\n",
                hint=P('Проще всего так: <code>list.innerHTML += \'&lt;li&gt;\' + fruits[i] + \'&lt;/li&gt;\'</code>'),
                tests=[dom('В списке 3 пункта', 'return count("#list li") === 3 || "Сейчас пунктов: " + count("#list li");'),
                       dom('Пункты в правильном порядке', 'return $$("#list li").map(e => e.textContent.trim()).join(",") === "Яблоко,Банан,Вишня" || "Сейчас: " + $$("#list li").map(e => e.textContent).join(", ");'),
                       code_has(r'for\s*\(|forEach', 'Используется цикл')],
                solution="let fruits = ['Яблоко', 'Банан', 'Вишня']\nlet list = document.querySelector('#list')\n\nfor (let i = 0; i < fruits.length; i++) {\n    list.innerHTML += '<li>' + fruits[i] + '</li>'\n}\n"),
            task('Покрась всех', P(
                'Найди все абзацы с классом <code>.item</code> через <code>querySelectorAll</code> и сделай их зелёными (<code>green</code>). '
                'Первый из них сделай ещё и жирным.'),
                level=1, new=True,
                fixture='\n'.join(f'<p class="item">Пункт {i}</p>' for i in range(1, 6)) + '\n<p>Обычный абзац</p>',
                starter="let items = document.querySelectorAll('.item')\n",
                tests=[dom('Все .item зелёные', 'return $$(".item").every(e => getComputedStyle(e).color === norm("color", "green")) || "Не все .item зелёные";'),
                       dom('Обычный абзац не тронут', 'return css("p:not(.item)", "color") !== norm("color", "green") || "Обычный абзац не должен краситься";'),
                       dom('Первый пункт жирный', 'return ["bold", "700"].includes(css(".item", "font-weight")) || "Первый .item должен быть жирным";')],
                solution="let items = document.querySelectorAll('.item')\n\nfor (let i = 0; i < items.length; i++) {\n    items[i].style.color = 'green'\n}\nitems[0].style.fontWeight = 'bold'\n"),
            task('Сколько пунктов в меню?', P(
                'Посчитай с помощью JavaScript, сколько пунктов <code>li</code> в меню, и выведи <b>Всего пунктов: …</b> '
                'в консоль, а ещё поменяй заголовок страницы (<code>document.title</code>) на <b>Меню готово</b>.'),
                level=1, new=True,
                fixture='<ul class="menu">\n    <li>Главная</li>\n    <li>Игры</li>\n    <li>Новости</li>\n    <li>Контакты</li>\n</ul>',
                tests=[io([], ['Всего пунктов: 4']), code_has(r'\.length', 'Количество считается через .length'),
                       dom('Заголовок страницы изменён', 'return document.title === "Меню готово" || "Сейчас document.title = " + document.title;')],
                solution="let items = document.querySelectorAll('.menu li')\nconsole.log('Всего пунктов: ' + items.length)\ndocument.title = 'Меню готово'\n"),
        ]),
    ],
    links=[
        ('Что почитать', [
            ('DOM-дерево', 'https://learn.javascript.ru/dom-nodes', 'read'),
            ('Все свойства и методы document', 'https://developer.mozilla.org/ru/docs/Web/API/Document', 'read'),
        ]),
        practice_js('Где потренироваться', 'datatypes1', *[f'dom_html{i}' for i in range(1, 9)]),
        js_lessons(24),
    ],
)

LESSONS = [L17, L18, L19, L20, L21, L22, L23, L24]
