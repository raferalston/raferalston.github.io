"""Уроки 1–8: HTML и основы CSS."""
from kk_helpers import (task, sec, note, html, images, table, steps, P, UL, C,  # noqa: F401
                        dom, has, style, code_has, read_file)

W3 = 'https://www.w3schools.com/html/exercise.asp?x=xrcise_'
W3C = 'https://www.w3schools.com/css/exercise.asp?filename=exercise_'


def page(body, css='', title='Моя страница'):
    """Стартовый шаблон страницы."""
    style = f'    <style>\n{css.rstrip()}\n    </style>\n' if css else ''
    body = '\n'.join('    ' + l if l.strip() else '' for l in body.strip('\n').splitlines())
    return (f'<!DOCTYPE html>\n<html lang="ru">\n<head>\n    <meta charset="UTF-8">\n    <title>{title}</title>\n'
            f'{style}</head>\n<body>\n{body}\n</body>\n</html>\n')


def practice(title, *pairs):
    return (title, [(label, url, 'practice') for label, url in pairs])


# ------------------------------------------------------------------ Урок 1
L1 = dict(
    id='l1', file='lesson_1.html', num='1', course='basic',
    short='Первая страница: теги',
    title='Первая веб-страница. Блочные и строчные теги',
    about='VS Code, структура HTML, заголовки, абзацы, списки',
    lead='Устанавливаем редактор кода и создаём первую страницу. Разбираемся, чем блочные теги отличаются от строчных.',
    sections=[
        sec('Как запустить дома Visual Studio Code', emoji='⬇️', items=[
            steps(
                dict(text='Скачай и установи <a href="https://code.visualstudio.com" target="_blank" rel="noopener">Visual Studio Code</a>.',
                     attrs='class="Первое число для шифра сейфа - 8"'),
                ('Установи расширения.', [('img/img_1.png', 'Установка расширений')]),
                ('Создай новую папку для проекта.', [('img/img_2.png', 'Новая папка')]),
                ('В папке создай файл <code>index.html</code>.', [('img/img_3.png', 'Файл index.html')]),
                dict(text='Напиши в документе <code>html</code>, выбери <code>html:5</code> и нажми <kbd>Enter</kbd>.',
                     images=[('img/img_4.png', 'Заготовка html:5')], title_attrs='id="Второе число для шифра сейфа - 5"'),
                ('Можно начинать работать!', [('img/img_5.png', 'Готово')]),
            ),
        ]),
        sec('Задания', emoji='✍️', items=[
            note('Пиши код в редакторе — ниже сразу появится <b>результат</b>. '
                 'Когда закончишь, нажми <b>«✓ Проверить»</b>. Код сохраняется в браузере сам.', 'info'),
            task('Страница из блочных и строчных тегов', P(
                'Создай страницу, используя все известные тебе <b>блочные</b> (<code>h1–h6</code>, <code>p</code>, <code>div</code>) '
                'и <b>строчные</b> (<code>b</code>, <code>i</code>, <code>em</code>, <code>mark</code>, <code>span</code>) теги.',
                'Посмотри образец и сделай похожую страницу про себя.'),
                level=1, example='lesson_1_example.html',
                tests=[has('h1'), has('p', min=2), has('b, strong', 'Есть жирный текст (b или strong)'),
                       has('i, em', 'Есть курсив (i или em)'), has('mark', 'Есть выделение mark'),
                       has('h2, h3, h4, h5, h6', 'Есть заголовок поменьше (h2–h6)')],
                solution=page('''
<h1>Добро пожаловать на мою <em>страничку</em></h1>
<p>Меня зовут <b>Аня</b>, я учусь <mark>делать сайты</mark>.</p>
<p>Больше всего мне нравится <i>рисовать</i> и играть в шахматы.</p>
<h6>Слишком маленький заголовок, чтобы его рассмотреть</h6>
''')),
            task('Все заголовки', P(
                'Создай шесть заголовков — от <code>&lt;h1&gt;</code> до <code>&lt;h6&gt;</code>. '
                'В каждом напиши, какого он уровня. Посмотри, как меняется размер.'),
                level=1, new=True,
                tests=[has(f'h{i}') for i in range(1, 7)],
                solution=page('\n'.join(f'<h{i}>Заголовок {i} уровня</h{i}>' for i in range(1, 7)))),
            task('Списки', P(
                'Сделай <b>маркированный</b> список покупок (<code>&lt;ul&gt;</code>, минимум 5 пунктов) '
                'и <b>нумерованный</b> список шагов, как приготовить бутерброд (<code>&lt;ol&gt;</code>, минимум 3 пункта).'),
                level=1, new=True,
                tests=[has('ul > li', 'В ul не меньше 5 пунктов', min=5), has('ol > li', 'В ol не меньше 3 пунктов', min=3)],
                solution=page('''
<h2>Список покупок</h2>
<ul>
    <li>Хлеб</li>
    <li>Сыр</li>
    <li>Помидоры</li>
    <li>Молоко</li>
    <li>Яблоки</li>
</ul>
<h2>Как сделать бутерброд</h2>
<ol>
    <li>Отрезать кусок хлеба</li>
    <li>Положить сыр</li>
    <li>Добавить помидор</li>
</ol>
''')),
            task('Стихотворение', P(
                'Запиши любое четверостишие. Каждая строчка — с новой строки: используй <code>&lt;br&gt;</code> '
                '(минимум 3 штуки). Между названием и стихом поставь горизонтальную линию <code>&lt;hr&gt;</code>.'),
                level=1, new=True,
                tests=[has('br', 'Есть переносы строк br (не меньше 3)', min=3), has('hr', 'Есть линия hr'), has('p')],
                solution=page('''
<h2>Зимнее утро</h2>
<hr>
<p>
    Мороз и солнце; день чудесный!<br>
    Ещё ты дремлешь, друг прелестный —<br>
    Пора, красавица, проснись:<br>
    Открой сомкнуты негой взоры...
</p>
''')),
            task('Спецсимволы', P(
                'Некоторые символы нельзя просто так написать в HTML. Выведи на странице:',
                UL('знак копирайта: <b>© КИДКОД</b> (<code>&amp;copy;</code>)',
                   'текст <b>&lt;h1&gt;</b> — именно как текст, а не как тег (<code>&amp;lt;</code> и <code>&amp;gt;</code>)',
                   'сердечко <b>♥</b> (<code>&amp;hearts;</code>)')),
                level=2, new=True,
                hint=P('Полный список спецсимволов — в полезных ссылках внизу страницы.'),
                tests=[dom('На странице есть ©', 'return document.body.textContent.includes("©") || "Не нашёл символ ©";'),
                       dom('Тег <h1> виден как текст', 'return document.body.textContent.includes("<h1>") || "Не вижу текст <h1> на странице";'),
                       dom('Есть сердечко ♥', 'return document.body.textContent.includes("♥") || "Не нашёл ♥";')],
                solution=page('''
<p>&copy; КИДКОД</p>
<p>Самый главный заголовок делается тегом &lt;h1&gt;</p>
<p>Я &hearts; HTML</p>
''')),
            task('Формулы и цитаты', P(
                'Напиши формулу воды <b>H<sub>2</sub>O</b> и площадь квадрата <b>a<sup>2</sup></b> с помощью тегов '
                '<code>&lt;sub&gt;</code> и <code>&lt;sup&gt;</code>. Добавь цитату в теге <code>&lt;blockquote&gt;</code>.'),
                level=2, new=True,
                tests=[has('sub'), has('sup'), has('blockquote')],
                solution=page('''
<p>Формула воды: H<sub>2</sub>O</p>
<p>Площадь квадрата: S = a<sup>2</sup></p>
<blockquote>Лучший способ предсказать будущее — создать его.</blockquote>
''')),
        ]),
    ],
    links=[
        ('Полезные ссылки', [
            ('Список текстовых тегов', 'https://html5book.ru/html-text/'),
            ('Блочные элементы', 'http://htmlbook.ru/html/type/block/'),
            ('Специальные символы', 'https://htmlweb.ru/html/symbols.php'),
            ('Проверить почту и пароль на взлом', 'https://haveibeenpwned.com/', 'tool'),
            ('Тест для 1 урока', 'web_tests/lesson_1/index.html', 'test'),
        ]),
        ('Что почитать', [('Основы HTML', 'https://html5book.ru/osnovy-html/', 'read')]),
        practice('Где потренироваться',
                 ('Тег заголовка (heading)', W3 + 'headings1'),
                 ('Тег параграфа (paragraph)', W3 + 'paragraphs1')),
    ],
)

# ------------------------------------------------------------------ Урок 2
L2_PAGE = page('''
<h1>Загадка!</h1>
<mark>Я зашифровал слово, попробуй его расшифровать! А также попробуй создать точно такую же страничку =)</mark>
<div>
    <h2>жявягйябдйя</h2>
    <form action="" id="quizForm">
        <input type="text">
        <input type="submit" value="Ответ" id="secret">
    </form>
    <p id="answer"></p>
</div>
<div>
    <strong>Подсказка: </strong>
    <small>Шифр был придуман древнеримским <i>Диктатором!</i></small>
</div>
''', title='Загадка')

L2 = dict(
    id='l2', file='lesson_2.html', num='2', course='basic',
    short='Браузер, ссылки, таблицы, формы',
    title='Как работает веб. Ссылки, таблицы и формы',
    about='Консоль разработчика, a, table, form, input',
    lead='Открываем «капот» браузера — консоль разработчика, узнаём, как страница попадает к нам из интернета, '
         'и учимся делать ссылки, таблицы и формы.',
    sections=[
        sec('Как работать с браузером Chrome', emoji='🔍', items=[
            steps(('Открой браузер и нажми <kbd>F12</kbd> или <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>I</kbd>.',
                   [('img/browser_1.png', 'Консоль в браузере')]),
                  ('Простая схема работы веба: браузер отправляет запрос, сервер присылает ответ.',
                   [('img/web.png', 'Схема работы веба')])),
        ]),
        sec('Задания', emoji='✍️', items=[
            task('Создай такую же страницу и разгадай шифр', P(
                'Открой образец, разгадай зашифрованное слово и сделай <b>точно такую же</b> страницу: '
                'заголовок, выделенный текст, форму с полем и кнопкой, подсказку.',
                'Нажми <kbd>F12</kbd> на странице-образце — там можно найти кое-что интересное!'),
                level=1, example='lesson_2_test.html', example_label='Открыть загадку',
                tests=[has('h1'), has('mark'), has('form'), has('form input[type="text"]', 'В форме есть текстовое поле'),
                       has('input[type="submit"], button', 'Есть кнопка отправки'),
                       has('strong'), has('small'), has('i')],
                solution=L2_PAGE),
            task('Расписание уроков', P(
                'Сделай таблицу с расписанием на 3 дня: первая строка — заголовки (<code>&lt;th&gt;</code>), '
                'дальше минимум 3 строки с уроками. У таблицы должна быть рамка: атрибут <code>border="1"</code>.'),
                level=1, new=True,
                tests=[has('table'), has('th', 'Не меньше 3 ячеек-заголовков th', min=3),
                       has('tr', 'Не меньше 4 строк tr', min=4),
                       dom('Есть рамка', 'return has("table[border]") || css("td", "border-top-style") !== "none" || "Добавь border=\\"1\\"";')],
                solution=page('''
<table border="1">
    <tr><th>Понедельник</th><th>Вторник</th><th>Среда</th></tr>
    <tr><td>Математика</td><td>Русский</td><td>Информатика</td></tr>
    <tr><td>Физкультура</td><td>Литература</td><td>Английский</td></tr>
    <tr><td>Рисование</td><td>Музыка</td><td>Технология</td></tr>
</table>
''')),
            task('Все виды ссылок', P('Сделай три ссылки:',
                UL('на любой сайт, которая открывается <b>в новой вкладке</b> (<code>target="_blank"</code>)',
                   'на электронную почту (<code>href="mailto:..."</code>)',
                   'ссылку-<b>картинку</b>: внутри <code>&lt;a&gt;</code> — тег <code>&lt;img&gt;</code> '
                   '(можно взять картинку <code>img/telegram.png</code>)')),
                level=1, new=True,
                tests=[has('a[href^="http"][target="_blank"]', 'Ссылка на сайт в новой вкладке'),
                       has('a[href^="mailto:"]', 'Ссылка на почту'), has('a img', 'Картинка внутри ссылки')],
                solution=page('''
<p><a href="https://developer.mozilla.org/ru/" target="_blank">Учебник MDN</a></p>
<p><a href="mailto:hello@kidkod.ru">Написать письмо</a></p>
<p><a href="https://t.me/kidkodschool" target="_blank"><img src="img/telegram.png" alt="Телеграм" width="48"></a></p>
''')),
            task('Форма регистрации', P('Сделай форму регистрации в игре. В ней должны быть:',
                UL('поле для имени и поле для почты (<code>type="email"</code>)',
                   'поле для пароля (<code>type="password"</code>)',
                   'выпадающий список <code>&lt;select&gt;</code> с выбором класса героя (минимум 3 варианта)',
                   'галочка <code>type="checkbox"</code> «Согласен с правилами»',
                   'кнопка «Зарегистрироваться»',
                   'подписи <code>&lt;label&gt;</code> к полям')),
                level=2, new=True,
                tests=[has('form'), has('input[type="email"]'), has('input[type="password"]'),
                       has('select option', 'В select не меньше 3 вариантов', min=3), has('input[type="checkbox"]'),
                       has('button, input[type="submit"]', 'Есть кнопка'), has('label', 'Есть подписи label', min=2)],
                solution=page('''
<h1>Регистрация героя</h1>
<form>
    <label for="name">Имя:</label>
    <input type="text" id="name"><br>
    <label for="email">Почта:</label>
    <input type="email" id="email"><br>
    <label for="pass">Пароль:</label>
    <input type="password" id="pass"><br>
    <label for="hero">Класс героя:</label>
    <select id="hero">
        <option>Воин</option>
        <option>Маг</option>
        <option>Лучник</option>
    </select><br>
    <label><input type="checkbox"> Согласен с правилами</label><br>
    <button type="submit">Зарегистрироваться</button>
</form>
''')),
            task('Найди код ответа сервера', P(
                'Открой консоль разработчика (<kbd>F12</kbd>) → вкладка <b>Network</b> (Сеть) и обнови эту страницу. '
                'Какой <b>код ответа</b> пришёл для файла <code>lesson_2.html</code>?',
                'Теперь открой несуществующую страницу, например <code>raferalston.github.io/nothing.html</code>. Какой код теперь? '
                'Найди оба кода в списке кодов ответов (ссылка внизу).'),
                level=1, new=True, editor=False,
                answer='Для существующей страницы — 200 OK (всё хорошо).\n'
                       'Для несуществующей — 404 Not Found (страница не найдена).\n'),
        ]),
    ],
    links=[
        ('Полезные ссылки', [
            ('Форма и её атрибуты', 'http://htmlbook.ru/html/form'),
            ('Элементы формы', 'http://htmlbook.ru/samhtml5/formy'),
            ('Список кодов ответов HTTP', 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BA%D0%BE%D0%B4%D0%BE%D0%B2_%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D1%8F_HTTP'),
            ('Тест для 2 урока', 'web_tests/lesson_2/index.html', 'test'),
        ]),
        ('Что почитать', [
            ('Как работают веб-запросы', 'https://developer.mozilla.org/ru/docs/Learn/Getting_started_with_the_web/How_the_Web_works', 'read'),
            ('Список тегов', 'https://www.w3schools.com/tags/', 'read'),
        ]),
        practice('Где потренироваться',
                 ('Тег таблицы (table)', W3 + 'tables1'),
                 ('Ссылки (a)', W3 + 'links1'),
                 ('Тег формы (form)', W3 + 'forms1')),
    ],
)

# ------------------------------------------------------------------ Урок 3
L3 = dict(
    id='l3', file='lesson_3.html', num='3', course='basic',
    short='Основы CSS',
    title='Основы CSS: цвета, шрифты, отступы и рамки',
    about='color, font-size, margin, padding, border',
    lead='Учимся украшать страницу: меняем цвета и шрифты, добавляем отступы и рамки.',
    sections=[
        sec('Задания', emoji='🎨', items=[
            note('<b>Шпаргалка:</b> стили пишутся в теге <code>&lt;style&gt;</code> внутри <code>&lt;head&gt;</code>: '
                 '<code>селектор { свойство: значение; }</code>. <code>margin</code> — внешний отступ, '
                 '<code>padding</code> — внутренний, <code>border</code> — рамка.', 'info'),
            task('Страница со всеми известными стилями', P(
                'Создай страницу и примени к ней все известные тебе стили: цвет текста и фона, размер шрифта, '
                'отступы и рамки. Пример — на картинке.'),
                level=1, images=[('img/css_1.png', 'Пробуем стили')],
                tests=[has('style', 'Есть тег style'),
                       dom('У заголовка свой цвет', 'if (!has("h1")) return "Нет заголовка h1"; return css("h1", "color") !== "rgb(0, 0, 0)" || "Поменяй цвет h1";'),
                       dom('У какого-то элемента есть фон', 'return $$("body, body *").some(e => getComputedStyle(e).backgroundColor !== "rgba(0, 0, 0, 0)") || "Задай кому-нибудь background-color";'),
                       dom('У какого-то элемента есть рамка', 'return $$("body *").some(e => getComputedStyle(e).borderTopStyle !== "none") || "Добавь кому-нибудь border";'),
                       dom('У какого-то элемента есть padding', 'return $$("body *").some(e => parseFloat(getComputedStyle(e).paddingTop) > 0) || "Добавь кому-нибудь padding";')],
                solution=page('''
<h1>Мой первый стиль</h1>
<p class="card">Этот абзац в рамке и с отступами.</p>
''', css='''
        body { background-color: #fff8e7; font-family: Arial, sans-serif; }
        h1 { color: tomato; font-size: 48px; }
        .card {
            background-color: lightblue;
            padding: 20px;
            margin: 30px;
            border: 3px dashed navy;
        }
''')),
            task('Нарисуй макет своего сайта', P(
                'Возьми лист бумаги и нарисуй, как будет выглядеть твой будущий сайт: где шапка, меню, картинки, текст. '
                'Такой рисунок называется <b>макет</b> (wireframe).'),
                level=1, editor=False, images=[('img/wireframe.png', 'Пример макета')]),
            task('Цветные заголовки', P(
                'Сделай заголовок <code>h1</code> <b>красным</b> (<code>red</code>), '
                'заголовок <code>h2</code> — цвета <code>#1e90ff</code>, а у абзацев <code>p</code> '
                'поставь размер шрифта <code>20px</code>.'),
                level=1, new=True,
                starter=page('<h1>Главный заголовок</h1>\n<h2>Подзаголовок</h2>\n<p>Обычный текст абзаца.</p>',
                             css='        /* Пиши стили здесь */\n'),
                tests=[style('h1', 'color', 'red'), style('h2', 'color', '#1e90ff'), style('p', 'font-size', '20px')],
                solution=page('<h1>Главный заголовок</h1>\n<h2>Подзаголовок</h2>\n<p>Обычный текст абзаца.</p>', css='''
        h1 { color: red; }
        h2 { color: #1e90ff; }
        p { font-size: 20px; }
''')),
            task('Карточка', P(
                'Оформи блок <code>.card</code>: внутренний отступ <code>20px</code>, внешний <code>30px</code>, '
                'рамка <code>3px solid</code> любого цвета, скругление углов <code>10px</code> и светлый фон '
                '<code>lightyellow</code>.'),
                level=1, new=True,
                starter=page('<div class="card">\n    <h2>Кот Барсик</h2>\n    <p>Любит спать и есть.</p>\n</div>',
                             css='        .card {\n            \n        }\n'),
                tests=[style('.card', 'padding-top', '20px', '.card { padding: 20px }'),
                       style('.card', 'margin-top', '30px', '.card { margin: 30px }'),
                       style('.card', 'border-top-width', '3px', 'Рамка толщиной 3px'),
                       style('.card', 'border-top-style', 'solid', 'Рамка сплошная (solid)'),
                       style('.card', 'border-top-left-radius', '10px', 'Скругление 10px'),
                       style('.card', 'background-color', 'lightyellow')],
                solution=page('<div class="card">\n    <h2>Кот Барсик</h2>\n    <p>Любит спать и есть.</p>\n</div>', css='''
        .card {
            padding: 20px;
            margin: 30px;
            border: 3px solid orange;
            border-radius: 10px;
            background-color: lightyellow;
        }
''')),
            task('Оформление текста', P('Настрой текст:',
                UL('<code>h1</code> — все буквы заглавные (<code>text-transform: uppercase</code>)',
                   'абзац <code>p</code> — по центру (<code>text-align: center</code>)',
                   'ссылка <code>a</code> — без подчёркивания (<code>text-decoration: none</code>)',
                   'текст <code>.note</code> — жирный (<code>font-weight: bold</code>) и курсивный (<code>font-style: italic</code>)')),
                level=2, new=True,
                starter=page('<h1>Новости школы</h1>\n<p>Сегодня мы научились делать сайты!</p>\n'
                             '<a href="#">Читать дальше</a>\n<p class="note">Домашку сдать до пятницы.</p>',
                             css='        /* Пиши стили здесь */\n'),
                tests=[style('h1', 'text-transform', 'uppercase'), style('p', 'text-align', 'center'),
                       style('a', 'text-decoration-line', 'none', 'a { text-decoration: none }'),
                       style('.note', 'font-weight', 'bold'), style('.note', 'font-style', 'italic')],
                solution=page('<h1>Новости школы</h1>\n<p>Сегодня мы научились делать сайты!</p>\n'
                              '<a href="#">Читать дальше</a>\n<p class="note">Домашку сдать до пятницы.</p>', css='''
        h1 { text-transform: uppercase; }
        p { text-align: center; }
        a { text-decoration: none; }
        .note { font-weight: bold; font-style: italic; }
''')),
            task('Три способа записать цвет', P(
                'Покрась три абзаца разными способами записи цвета: <code>.name</code> — словом <code>tomato</code>, '
                '<code>.hex</code> — кодом <code>#2ecc71</code>, <code>.rgb</code> — функцией <code>rgb(52, 152, 219)</code>.'),
                level=2, new=True,
                starter=page('<p class="name">Цвет словом</p>\n<p class="hex">Цвет HEX-кодом</p>\n<p class="rgb">Цвет в RGB</p>',
                             css='        /* Пиши стили здесь */\n'),
                tests=[style('.name', 'color', 'tomato'), style('.hex', 'color', '#2ecc71'), style('.rgb', 'color', 'rgb(52, 152, 219)'),
                       code_has(r'#2ecc71', 'Используется HEX-код', flags='i'), code_has(r'rgb\(', 'Используется rgb()')],
                solution=page('<p class="name">Цвет словом</p>\n<p class="hex">Цвет HEX-кодом</p>\n<p class="rgb">Цвет в RGB</p>', css='''
        .name { color: tomato; }
        .hex { color: #2ecc71; }
        .rgb { color: rgb(52, 152, 219); }
''')),
        ]),
    ],
    links=[
        ('Полезные ссылки', [
            ('Значения для размера шрифта', 'https://www.w3schools.com/cssref/pr_font_font-size.asp'),
            ('Текстовые свойства', 'https://developer.mozilla.org/ru/docs/Learn/CSS/Styling_text/Fundamentals'),
            ('Список цветов', 'https://www.w3schools.com/cssref/css_colors.asp'),
            ('CSS — color', 'https://www.w3schools.com/Css/css_colors.asp'),
            ('Внешний отступ (margin)', 'https://www.w3schools.com/css/css_margin.asp'),
            ('Внутренний отступ (padding)', 'https://www.w3schools.com/css/css_padding.asp'),
            ('Свойства границы (border)', 'https://www.w3schools.com/css/css_border.asp'),
            ('Горячие клавиши VS Code', 'https://nikomedvedev.ru/other/vscodeshortcuts/hotkeys.html', 'tool'),
            ('Тест для 3 урока', 'web_tests/lesson_3/index.html', 'test'),
        ]),
        ('Что почитать', [('Каким должен быть ваш веб-сайт', 'https://developer.mozilla.org/ru/docs/Learn/Getting_started_with_the_web/What_will_your_website_look_like', 'read')]),
        practice('Где потренироваться',
                 ('CSS', W3 + 'css1'),
                 *[(f'Margin #{i}', f'{W3C}margin{i}') for i in range(1, 5)],
                 *[(f'Padding #{i}', f'{W3C}padding{i}') for i in range(1, 4)],
                 *[(f'Border #{i}', f'{W3C}border{i}') for i in range(1, 5)]),
    ],
)

# ------------------------------------------------------------------ Урок 4
L4_STRUCT = page('''
<h1>Название</h1>
<div>
    <div class="picture-1">
        <img src="img/lesson_6.jpg" alt="Тут будет первая картинка" width="200">
        <span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
    </div>
</div>
<div class="picture-2">
    <img src="img/lesson_6.jpg" alt="Тут будет вторая картинка" width="200">
</div>
<div>
    <span class="text-1">Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
    <span class="text-2">Deserunt modi tempore eligendi minus recusandae.</span>
</div>
<div>
    <button>Кнопка</button>
</div>
''', title='Структура html')

L4_ANCHOR_START = read_file('inner_anchor.html').strip() + '\n'

L4 = dict(
    id='l4', file='lesson_4.html', num='4', course='basic',
    short='Структура сайта и селекторы',
    title='Структура сайта. Селекторы class и id',
    about='div, class, id, внутренние ссылки, vh и vw, GitHub',
    lead='Строим каркас сайта по рисунку, знакомимся с селекторами <code>class</code> и <code>id</code> '
         'и регистрируемся на GitHub.',
    head_extra='\n    <style>.code-third-number { width: 6px; display: inline-block; } .code-four-number { color: rgba(255, 255, 255, 0); }</style>',
    body_extra='<span class="code-third-number check-css-of-this-element"></span>',
    sections=[
        sec('Задания', emoji='🏗️', items=[
            task('HTML-структура по рисунку', P(
                'Создай HTML-структуру своего сайта по рисунку-макету: заголовок, блоки с картинками '
                '(<code>class="picture-1"</code>, <code>class="picture-2"</code>), блок с текстами '
                '(<code>class="text-1"</code>, <code>class="text-2"</code>) и кнопку.'),
                level=1, images=[('img/wireframe.png', 'Макет'), ('img/html_struct_code.png', 'Структура и контент'),
                                 ('img/html_sctruct_view.png', 'Результат')],
                tests=[has('h1'), has('.picture-1 img', 'Картинка в .picture-1'), has('.picture-2 img', 'Картинка в .picture-2'),
                       has('.text-1'), has('.text-2'), has('button')],
                solution=L4_STRUCT),
            task('Внутренняя ссылка', P(
                'Внутренняя ссылка ведёт не на другую страницу, а к месту на этой же странице: '
                '<code>href="#id-блока"</code>. Замени <code>_______</code> так, чтобы ссылка «ВНИЗ» вела ко второму блоку, '
                'а «НАВЕРХ» — к первому. Покрути результат и понажимай ссылки!'),
                level=1, images=[('img/inner_anchor.png', 'Вид')], starter=L4_ANCHOR_START,
                tests=[has('a[href="#second-section"]', 'Ссылка ВНИЗ ведёт к #second-section'),
                       has('a[href="#first-section"]', 'Ссылка НАВЕРХ ведёт к #first-section')],
                solution=L4_ANCHOR_START.replace('_______">ВНИЗ', '#second-section">ВНИЗ').replace('_______">НАВЕРХ', '#first-section">НАВЕРХ')),
            task('Селекторы class и id', P('Напиши стили, не меняя HTML:',
                UL('элемент с <code>id="main-title"</code> — фиолетовый (<code>purple</code>)',
                   'все элементы с классом <code>.important</code> — жирные и с жёлтым фоном (<code>yellow</code>)',
                   'элементы с классом <code>.hidden</code> — спрятать (<code>display: none</code>)')),
                level=1, new=True,
                hint=P('Селектор класса начинается с точки: <code>.important</code>, селектор id — с решётки: <code>#main-title</code>.'),
                starter=page('''
<h1 id="main-title">Правила класса</h1>
<p>Приходить вовремя.</p>
<p class="important">Не шуметь на уроке!</p>
<p>Делать домашку.</p>
<p class="important">Сохранять код!</p>
<p class="hidden">Этот текст должен исчезнуть</p>
''', css='        /* Пиши стили здесь */\n'),
                tests=[style('#main-title', 'color', 'purple'), style('.important', 'font-weight', 'bold'),
                       style('.important', 'background-color', 'yellow'), style('.hidden', 'display', 'none')],
                solution=page('''
<h1 id="main-title">Правила класса</h1>
<p>Приходить вовремя.</p>
<p class="important">Не шуметь на уроке!</p>
<p>Делать домашку.</p>
<p class="important">Сохранять код!</p>
<p class="hidden">Этот текст должен исчезнуть</p>
''', css='''
        #main-title { color: purple; }
        .important { font-weight: bold; background-color: yellow; }
        .hidden { display: none; }
''')),
            task('Экран целиком: vh и vw', P(
                'Сделай блок <code>.hero</code> высотой ровно в <b>весь экран</b> (<code>100vh</code>), '
                'а блок <code>.half</code> — шириной в <b>половину</b> экрана (<code>50vw</code>). '
                'Не забудь убрать отступы у <code>body</code>: <code>margin: 0</code>.'),
                level=2, new=True,
                starter=page('<div class="hero">Весь экран</div>\n<div class="half">Половина ширины</div>', css='''
        .hero { background-color: #6d4aff; color: white; }
        .half { background-color: #ff9f1c; }
'''),
                tests=[dom('.hero высотой во весь экран', 'if (!has(".hero")) return "Нет .hero"; return Math.abs($(".hero").getBoundingClientRect().height - innerHeight) < 2 || "Высота .hero = " + css(".hero", "height") + ", а экран — " + innerHeight + "px";'),
                       dom('.half шириной в половину экрана', 'if (!has(".half")) return "Нет .half"; return Math.abs($(".half").getBoundingClientRect().width - innerWidth / 2) < 2 || "Ширина .half = " + css(".half", "width");'),
                       style('body', 'margin-top', '0px', 'У body нет отступов')],
                solution=page('<div class="hero">Весь экран</div>\n<div class="half">Половина ширины</div>', css='''
        body { margin: 0; }
        .hero { background-color: #6d4aff; color: white; height: 100vh; }
        .half { background-color: #ff9f1c; width: 50vw; }
''')),
        ]),
        sec('Как зарегистрировать аккаунт на GitHub', emoji='🐙', items=[
            steps(
                'Открой сайт <a href="https://github.com/" target="_blank" rel="noopener">github.com</a>.',
                ('Введи свои данные и нажми <b>Sign up for GitHub</b>.', ['img/git_1.png']),
                ('Проверь почту и нажми <b>Continue</b>.', ['img/git_2.png']),
                ('Введи пароль и нажми <b>Continue</b>.', ['img/git_3.png']),
                ('Введи никнейм и нажми <b>Continue</b>.', ['img/git_4.png']),
                ('Напиши <b>n</b> и нажми <b>Continue</b>.', ['img/git_5.png']),
                ('Нажми <b>Start puzzle</b> и пройди головоломку.', ['img/git_6.png']),
                ('После успешного прохождения нажми <b>Create account</b>.', ['img/git_7.png']),
                ('Введи код, который пришёл на почту.', ['img/git_8.png']),
                ('Отметь пункты, как на картинке.', ['img/git_9.png']),
                ('В следующем меню нажми <b>Continue</b>.', ['img/git_10.png']),
                ('Выбери <b>Continue for free</b>.', ['img/git_11.png']),
            ),
            html('<div class="code-four-number">3</div>'),
        ]),
    ],
    links=[
        ('Полезные ссылки', [
            ('Игра для изучения селекторов', 'https://flukeout.github.io/', 'game'),
            ('Единицы измерения vh, vw, vmin, vmax', 'https://html5book.ru/edinicy-izmereniya-vh-vw-vmin-vmax/'),
            ('Селекторы', 'https://developer.mozilla.org/ru/docs/Web/CSS/CSS_%D0%A1%D0%B5%D0%BB%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D1%8B'),
            ('Горячие клавиши VS Code', 'https://nikomedvedev.ru/other/vscodeshortcuts/hotkeys.html', 'tool'),
            ('Тест для 4 урока', 'web_tests/lesson_4/index.html', 'test'),
        ]),
        practice('Где потренироваться',
                 ('Селекторы — class', W3 + 'classes1'), ('Селекторы — id', W3 + 'id1'),
                 ('Ширина/высота #1', W3C + 'dimension1'), ('Ширина/высота #2', W3C + 'dimension2'),
                 *[(f'Блоковая модель #{i}', f'{W3C}boxmodel{i}') for i in range(1, 5)]),
    ],
)

# ------------------------------------------------------------------ Урок 5
L5_POS = read_file('pos_work.html').strip() + '\n'

L5 = dict(
    id='l5', file='lesson_5.html', num='5', course='basic',
    short='Сайт в интернете и position',
    title='Выкладываем сайт в интернет. Позиционирование',
    about='GitHub Pages, position: relative, absolute, fixed, sticky',
    lead='Публикуем свой сайт на GitHub Pages, чтобы домашку можно было открыть с любого устройства, '
         'и учимся ставить элементы в любое место страницы.',
    body_extra='<!-- пятая цифра шифра - 7 -->',
    sections=[
        sec('Задания', emoji='🚀', items=[
            task('Выложи домашку на свой сайт', P(
                'По <a href="how_deploy.html" target="_blank">инструкции</a> создай свой сайт на GitHub Pages и добавь на него задания:',
                UL('<a href="lesson_2_test.html" target="_blank">точную копию страницы-загадки</a> (урок 2)',
                   'страницу со стилями (урок 3)', 'HTML-структуру своей странички (урок 4)'),
                'На главной странице сайта сделай ссылки на все задания — как на картинке.'),
                level=1, local=True, images=[('img/links_for_task.png', 'Ссылки на задания')]),
            task('Расставь квадраты', P(
                'Расположи четыре цветных квадрата лесенкой, как на картинке. Используй <code>position: absolute</code> '
                'и свойства <code>top</code>, <code>left</code>.',
                'А потом <a href="lesson_5_test.html" target="_blank">разгадай шифр сейфа</a> — и получи подсказку!'),
                level=2, images=[('img/pos_work.png', 'Позиционирование')],
                starter=page('<div class="f"></div>\n<div class="s"></div>\n<div class="t"></div>\n<div class="fo"></div>', css='''
        .f { background-color: darkorange; }
        .s { background-color: green; }
        .t { background-color: blue; }
        .fo { background-color: rebeccapurple; }
''', title='Тренируем позиционирование'),
                tests=[dom('Четыре блока с position: absolute', 'const n = $$("div").filter(d => getComputedStyle(d).position === "absolute").length; return n >= 4 || "Сейчас absolute только у " + n + " блоков";'),
                       dom('У блоков есть размер', 'return $$("div").every(d => d.offsetWidth > 10 && d.offsetHeight > 10) || "Задай блокам width и height";'),
                       dom('Каждый следующий блок правее и ниже', 'const r = $$("div").map(d => d.getBoundingClientRect()); for (let i = 1; i < r.length; i++) { if (!(r[i].left > r[i-1].left && r[i].top > r[i-1].top)) return "Блок " + (i + 1) + " должен быть правее и ниже блока " + i; } return true;')],
                solution=L5_POS),
            task('Липкая шапка', P(
                'Сделай так, чтобы шапка <code>header</code> <b>прилипала</b> к верху экрана при прокрутке: '
                '<code>position: sticky</code> и <code>top: 0</code>. Прокрути результат и проверь.'),
                level=1, new=True,
                starter=page('<header>Моя шапка</header>\n<main>\n' + '\n'.join(f'    <p>Абзац номер {i}. Прокручивай ниже!</p>' for i in range(1, 31)) + '\n</main>', css='''
        body { margin: 0; }
        header { background-color: #6d4aff; color: white; padding: 20px; font-size: 24px; }
'''),
                tests=[style('header', 'position', 'sticky'), style('header', 'top', '0px')],
                solution=page('<header>Моя шапка</header>\n<main>\n' + '\n'.join(f'    <p>Абзац номер {i}. Прокручивай ниже!</p>' for i in range(1, 31)) + '\n</main>', css='''
        body { margin: 0; }
        header { background-color: #6d4aff; color: white; padding: 20px; font-size: 24px; position: sticky; top: 0; }
''')),
            task('Значок на аватарке', P(
                'Сделай красный кружок-значок с числом <b>3</b> в правом верхнем углу аватарки, как у сообщений в мессенджерах. '
                'Родителю <code>.avatar</code> дай <code>position: relative</code>, а значку <code>.badge</code> — '
                '<code>position: absolute</code>, <code>top: 0</code>, <code>right: 0</code>.'),
                level=2, new=True,
                starter=page('<div class="avatar">\n    😺\n    <span class="badge">3</span>\n</div>', css='''
        .avatar { width: 120px; height: 120px; font-size: 90px; text-align: center; background-color: #eee; border-radius: 50%; }
        .badge { background-color: red; color: white; font-size: 20px; width: 34px; height: 34px; line-height: 34px; border-radius: 50%; }
'''),
                tests=[style('.avatar', 'position', 'relative'), style('.badge', 'position', 'absolute'),
                       dom('Значок в правом верхнем углу', 'const a = $(".avatar").getBoundingClientRect(), b = $(".badge").getBoundingClientRect(); return (Math.abs(a.top - b.top) < 3 && Math.abs(a.right - b.right) < 3) || "Значок должен стоять в правом верхнем углу";')],
                solution=page('<div class="avatar">\n    😺\n    <span class="badge">3</span>\n</div>', css='''
        .avatar { width: 120px; height: 120px; font-size: 90px; text-align: center; background-color: #eee; border-radius: 50%; position: relative; }
        .badge { background-color: red; color: white; font-size: 20px; width: 34px; height: 34px; line-height: 34px; border-radius: 50%; position: absolute; top: 0; right: 0; }
''')),
            task('Кнопка «Наверх»', P(
                'Кнопка <code>.up</code> должна всегда висеть в правом нижнем углу экрана, даже при прокрутке: '
                '<code>position: fixed</code>, отступы <code>20px</code> снизу и справа.'),
                level=2, new=True,
                starter=page('<h1 id="top">Длинная страница</h1>\n' + '\n'.join(f'<p>Строка {i}</p>' for i in range(1, 41)) + '\n<a class="up" href="#top">⬆</a>', css='''
        .up { background-color: #ff4d8d; color: white; padding: 12px 16px; border-radius: 50%; text-decoration: none; font-size: 24px; }
'''),
                tests=[style('.up', 'position', 'fixed'), style('.up', 'bottom', '20px'), style('.up', 'right', '20px')],
                solution=page('<h1 id="top">Длинная страница</h1>\n' + '\n'.join(f'<p>Строка {i}</p>' for i in range(1, 41)) + '\n<a class="up" href="#top">⬆</a>', css='''
        .up { background-color: #ff4d8d; color: white; padding: 12px 16px; border-radius: 50%; text-decoration: none; font-size: 24px;
              position: fixed; bottom: 20px; right: 20px; }
''')),
        ]),
    ],
    links=[
        ('Полезные ссылки', [
            ('Инструкция: как выложить сайт', 'how_deploy.html', 'lesson'),
            ('Позиционирование элементов', 'https://developer.mozilla.org/ru/docs/Web/CSS/position'),
            ('Список HTML-тегов', 'https://html5book.ru/html-tags/'),
        ]),
        ('Что почитать', [('Как создать форму', 'https://html5book.ru/sozdanie-html-form/', 'read')]),
        practice('Где потренироваться', *[(f'Позиционирование #{i}', f'{W3C}positioning{i}') for i in range(1, 4)]),
    ],
)

# ------------------------------------------------------------------ Урок 6
L6 = dict(
    id='l6', file='lesson_6.html', num='6', course='basic',
    short='Flexbox',
    title='Flexbox: раскладываем блоки',
    about='display: flex, flex-direction, justify-content, flex-wrap',
    lead='Flexbox — самый удобный способ расставить блоки в ряд, в столбик или ровно по центру.',
    sections=[
        sec('Задания', emoji='📦', items=[
            note('<b>Шпаргалка:</b> <code>display: flex</code> включают у <b>родителя</b>. '
                 '<code>justify-content</code> — выравнивание вдоль главной оси, <code>align-items</code> — поперёк, '
                 '<code>flex-direction: column</code> — столбиком, <code>flex-wrap: wrap</code> — перенос на новую строку.', 'info'),
            task('Страница-раскладка', P('Сделай такую же раскладку, как на образце. Используемые свойства:') +
                 '<div class="table-wrap"><table class="nice"><thead><tr><th>Свойство</th><th>Значение</th></tr></thead><tbody>'
                 '<tr><td>display</td><td>flex</td></tr><tr><td>flex-direction</td><td>column</td></tr>'
                 '<tr><td>flex-basis</td><td>20%</td></tr><tr><td>text-align</td><td>center</td></tr></tbody></table></div>',
                 level=2, example='flex_example.html',
                 tests=[style('body', 'display', 'flex'),
                        dom('Есть блок с flex-direction: column', 'return $$("body *").some(e => getComputedStyle(e).flexDirection === "column" && getComputedStyle(e).display === "flex") || "Не нашёл flex-контейнер со столбиком";'),
                        dom('Есть блок с flex-basis: 20%', 'return /flex-basis\\s*:\\s*20%/.test(code) || "Не нашёл flex-basis: 20%";'),
                        dom('Меню занимает левую часть экрана', 'const m = $("body > *"); return (m && m.getBoundingClientRect().left < 5 && m.getBoundingClientRect().width < innerWidth / 2) || "Первый блок должен стоять слева";')],
                 solution='file:flex_example.html'),
            task('Карточки товаров', P('Сделай три карточки, как на образце. Используемые свойства:') +
                 '<div class="table-wrap"><table class="nice"><thead><tr><th>Свойство</th><th>Значение</th></tr></thead><tbody>'
                 '<tr><td>cursor</td><td>pointer</td></tr><tr><td>border-bottom-…-radius</td><td>5px</td></tr>'
                 '<tr><td>flex-wrap</td><td>wrap</td></tr></tbody></table></div>',
                 level=2, example='homework_2.html',
                 hint=P('Картинку можно взять с сайта: <code>&lt;img src="img/lesson_6.jpg"&gt;</code>.'),
                 tests=[has('.container', 'Три карточки .container', min=3), style('body', 'display', 'flex'),
                        style('body', 'flex-wrap', 'wrap'), style('button', 'cursor', 'pointer'),
                        dom('У кнопки скруглены нижние углы', 'return parseFloat(css("button", "border-bottom-left-radius")) > 0 || "Скругли нижние углы кнопки";'),
                        has('.container img', 'В карточках есть картинки', min=3)],
                 solution='file:homework_2.html'),
            task('Ровно по центру', P(
                'Поставь блок <code>.box</code> <b>ровно в центр</b> экрана с помощью flexbox. '
                'У <code>body</code> уже есть высота во весь экран — осталось включить flex и выровнять.'),
                level=1, new=True,
                starter=page('<div class="box">Я в центре!</div>', css='''
        body { margin: 0; height: 100vh; background-color: #efeaff; }
        .box { width: 200px; padding: 30px; background-color: #6d4aff; color: white; text-align: center; border-radius: 16px; }
'''),
                tests=[style('body', 'display', 'flex'),
                       dom('Блок по центру экрана', 'const r = $(".box").getBoundingClientRect(); const dx = Math.abs(r.left + r.width / 2 - innerWidth / 2), dy = Math.abs(r.top + r.height / 2 - innerHeight / 2); return (dx < 3 && dy < 3) || "Блок сдвинут от центра на " + Math.round(dx) + "px по горизонтали и " + Math.round(dy) + "px по вертикали";')],
                solution=page('<div class="box">Я в центре!</div>', css='''
        body { margin: 0; height: 100vh; background-color: #efeaff; display: flex; justify-content: center; align-items: center; }
        .box { width: 200px; padding: 30px; background-color: #6d4aff; color: white; text-align: center; border-radius: 16px; }
''')),
            task('Меню в одну строку', P(
                'Сделай меню: логотип слева, ссылки справа. Для <code>nav</code> используй <code>display: flex</code> и '
                '<code>justify-content: space-between</code>, а для списка ссылок <code>.links</code> — тоже flex с '
                'промежутком <code>gap: 20px</code>.'),
                level=2, new=True,
                starter=page('''
<nav>
    <div class="logo">🚀 Космо</div>
    <div class="links">
        <a href="#">Главная</a>
        <a href="#">Игры</a>
        <a href="#">Контакты</a>
    </div>
</nav>
''', css='''
        body { margin: 0; font-family: sans-serif; }
        nav { background-color: #1f1b3d; padding: 16px 24px; }
        .logo { color: #ffd23f; font-weight: bold; font-size: 22px; }
        .links a { color: white; text-decoration: none; }
'''),
                tests=[style('nav', 'display', 'flex'), style('nav', 'justify-content', 'space-between'),
                       style('.links', 'display', 'flex'), style('.links', 'column-gap', '20px', '.links { gap: 20px }'),
                       dom('Логотип и ссылки в одной строке', 'const a = $(".logo").getBoundingClientRect(), b = $(".links").getBoundingClientRect(); return (Math.abs(a.top - b.top) < 20 && b.left > a.right) || "Логотип и ссылки должны быть в одной строке";')],
                solution=page('''
<nav>
    <div class="logo">🚀 Космо</div>
    <div class="links">
        <a href="#">Главная</a>
        <a href="#">Игры</a>
        <a href="#">Контакты</a>
    </div>
</nav>
''', css='''
        body { margin: 0; font-family: sans-serif; }
        nav { background-color: #1f1b3d; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }
        .logo { color: #ffd23f; font-weight: bold; font-size: 22px; }
        .links { display: flex; gap: 20px; }
        .links a { color: white; text-decoration: none; }
''')),
            task('Галерея в три колонки', P(
                'Шесть блоков <code>.item</code> должны стоять <b>по три в ряд</b>. Контейнеру <code>.gallery</code> — '
                '<code>display: flex</code> и <code>flex-wrap: wrap</code>, а каждому <code>.item</code> — '
                'ширину <code>33.33%</code>.'),
                level=2, new=True,
                starter=page('<div class="gallery">\n' + '\n'.join(f'    <div class="item">{e}</div>' for e in '🍎🍌🍇🍉🍓🥝') + '\n</div>', css='''
        body { margin: 0; }
        .item { box-sizing: border-box; font-size: 60px; text-align: center; padding: 20px; border: 2px solid white; background-color: #ffe6f0; }
'''),
                tests=[style('.gallery', 'display', 'flex'), style('.gallery', 'flex-wrap', 'wrap'),
                       dom('По три блока в ряд', 'const tops = $$(".item").map(e => Math.round(e.getBoundingClientRect().top)); const rows = {}; tops.forEach(t => rows[t] = (rows[t] || 0) + 1); const counts = Object.values(rows); return (counts.length === 2 && counts.every(c => c === 3)) || "Сейчас в рядах: " + counts.join(", ");')],
                solution=page('<div class="gallery">\n' + '\n'.join(f'    <div class="item">{e}</div>' for e in '🍎🍌🍇🍉🍓🥝') + '\n</div>', css='''
        body { margin: 0; }
        .gallery { display: flex; flex-wrap: wrap; }
        .item { box-sizing: border-box; width: 33.33%; font-size: 60px; text-align: center; padding: 20px; border: 2px solid white; background-color: #ffe6f0; }
''')),
        ]),
        sec('Полезные сокращения для VS Code', emoji='⌨️', items=[
            images(('img/vsc_short_1.png', 'Сокращения 1'), ('img/vsc_short_2.png', 'Сокращения 2'), ('img/vsc_short_3.png', 'Сокращения 3')),
        ]),
    ],
    links=[
        ('Полезные ссылки', [
            ('Всё о flex', 'https://www.w3schools.com/css/css3_flexbox.asp'),
            ('Flexbox — руководство (на английском)', 'https://css-tricks.com/snippets/css/a-guide-to-flexbox/'),
            ('Flexbox — руководство (на русском)', 'https://tuhub.ru/posts/flexbox-complete-guide'),
            ('Выравнивание в flex-контейнере', 'https://www.w3schools.com/csSref/playit.asp?filename=playcss_align-content&preval=center'),
            ('Выравнивание текста', 'https://www.w3schools.com/cssref/pr_text_text-align.asp'),
            ('Flexbox Froggy — тренажёр', 'https://flexboxfroggy.com/#ru', 'game'),
        ]),
        ('Что почитать', [('Отображение элемента (display)', 'https://www.w3schools.com/cssref/pr_class_display.asp', 'read')]),
    ],
)

# ------------------------------------------------------------------ Урок 7
L7 = dict(
    id='l7', file='lesson_7.html', num='7', course='basic',
    short=':hover и inline-block',
    title='Эффект :hover и flex-элементы',
    about='inline-block, :hover, transition, transform',
    lead='Оживляем страницу: элементы реагируют на наведение мыши и плавно меняются.',
    sections=[
        sec('Задания', emoji='✨', items=[
            task('Навигационная панель', P(
                'Сделай навигационную панель, как на образце. Ссылкам в меню задай '
                '<code>display: inline-block</code> и внутренние отступы.'),
                level=1, example='navbar_7.html',
                tests=[has('nav'), has('nav a', 'В меню не меньше 3 ссылок', min=3), style('nav a', 'display', 'inline-block'),
                       dom('У ссылок есть внутренние отступы', 'return parseFloat(css("nav a", "padding-top")) > 0 || "Добавь ссылкам padding";'),
                       style('nav a', 'text-decoration-line', 'none', 'Ссылки без подчёркивания')],
                solution='file:navbar_7.html'),
            task('HOVER ME', P(
                'Сделай надпись из отдельных букв (каждая — в своём <code>&lt;span&gt;</code>). '
                'При наведении мыши буква должна <b>увеличиваться</b> (<code>transform: scale(1.4)</code>) и менять цвет, '
                'а изменение — быть плавным (<code>transition</code>).'),
                level=2, example='lesson_7_homework.html',
                tests=[has('span', 'Не меньше 5 букв в span', min=5), dom('Есть правило span:hover', 'return !!rule(/span:hover/) || "Не нашёл span:hover в CSS";'),
                       dom('При наведении буква увеличивается', 'const r = rule(/span:hover/); return (r && /scale/.test(r.style.transform)) || "Добавь в span:hover свойство transform: scale(...)";'),
                       dom('Есть плавный переход', 'return parseFloat(css("span", "transition-duration")) > 0 || "Добавь span свойство transition";')],
                solution='file:lesson_7_homework.html'),
            task('Кнопка, которая оживает', P(
                'Сделай кнопку, которая при наведении меняет цвет фона и курсор становится «рукой» '
                '(<code>cursor: pointer</code>). Изменение цвета должно занимать <code>0.3s</code>.'),
                level=1, new=True,
                starter=page('<button class="btn">Нажми меня</button>', css='''
        .btn { background-color: #19b8a6; color: white; border: 0; padding: 16px 32px; font-size: 20px; border-radius: 12px; }
'''),
                tests=[style('.btn', 'cursor', 'pointer'), dom('Есть правило .btn:hover с фоном', 'return !!rule(/\\.btn:hover/, "background-color") || "Добавь .btn:hover { background-color: ... }";'),
                       dom('transition 0.3s', 'return css(".btn", "transition-duration").split(",").some(x => parseFloat(x) === 0.3) || "Сейчас transition-duration: " + css(".btn", "transition-duration");')],
                solution=page('<button class="btn">Нажми меня</button>', css='''
        .btn { background-color: #19b8a6; color: white; border: 0; padding: 16px 32px; font-size: 20px; border-radius: 12px;
               cursor: pointer; transition: background-color 0.3s; }
        .btn:hover { background-color: #6d4aff; }
''')),
            task('Карточка всплывает', P(
                'При наведении на карточку <code>.card</code> она должна <b>подниматься вверх</b> на 10px '
                '(<code>transform: translateY(-10px)</code>) и получать тень (<code>box-shadow</code>).'),
                level=2, new=True,
                starter=page('<div class="card">\n    <h2>🐱 Котики</h2>\n    <p>Наведи на меня мышку</p>\n</div>', css='''
        body { padding: 40px; font-family: sans-serif; }
        .card { width: 220px; padding: 20px; border-radius: 16px; background-color: white; border: 1px solid #ddd; transition: all 0.25s; }
'''),
                tests=[dom('В .card:hover есть translateY', 'const r = rule(/\\.card:hover/); return (r && /translateY\\(-/.test(r.style.transform)) || "Добавь .card:hover { transform: translateY(-10px) }";'),
                       dom('В .card:hover есть тень', 'const r = rule(/\\.card:hover/); return (r && !!r.style.boxShadow) || "Добавь тень box-shadow";'),
                       dom('Есть плавный переход', 'return parseFloat(css(".card", "transition-duration")) > 0 || "Добавь .card transition";')],
                solution=page('<div class="card">\n    <h2>🐱 Котики</h2>\n    <p>Наведи на меня мышку</p>\n</div>', css='''
        body { padding: 40px; font-family: sans-serif; }
        .card { width: 220px; padding: 20px; border-radius: 16px; background-color: white; border: 1px solid #ddd; transition: all 0.25s; }
        .card:hover { transform: translateY(-10px); box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2); }
''')),
        ]),
        sec('Подготовка к тесту', emoji='📝', items=[
            note('На следующем занятии будет <b>тест</b>! Повтори прошедшие уроки: '
                 '<a href="lesson_1.html">1</a>, <a href="lesson_2.html">2</a>, <a href="lesson_3.html">3</a>, '
                 '<a href="lesson_4.html">4</a>, <a href="lesson_5.html">5</a>, <a href="lesson_6.html">6</a>.'),
        ]),
    ],
    links=[
        ('Полезные ссылки', [
            ('Набор современных веб-компонентов', 'https://www.htmlelements.com/demos/', 'tool'),
            ('CSS-переходы (transition)', 'https://developer.mozilla.org/ru/docs/Web/CSS/CSS_Transitions/Using_CSS_transitions'),
            ('Генератор CSS-теней', 'https://developer.mozilla.org/ru/docs/Web/CSS/CSS_Box_Model/Box-shadow_generator', 'tool'),
            ('Ещё один генератор теней', 'http://angrytools.com/css-generator/border/', 'tool'),
            ('Flexbox — руководство (на русском)', 'https://tuhub.ru/posts/flexbox-complete-guide'),
            (':hover эффект', 'http://htmlbook.ru/css/hover'),
        ]),
    ],
)

# ------------------------------------------------------------------ Урок 8
L8 = dict(
    id='l8', file='lesson_8.html', num='8', course='basic',
    short='Промежуточный проект',
    title='Промежуточный проект на HTML и CSS',
    about='Собираем всё изученное в один сайт',
    lead='Пора собрать всё, что мы знаем, в один настоящий сайт!',
    sections=[
        sec('Задания', emoji='🏆', items=[
            task('Сайт по макету', P(
                'Сверстай сайт по картинке, используя всё, что изучили: теги, стили, отступы, flexbox и :hover. '
                'Сравни свой результат с ответом только после того, как закончишь.'),
                level=3, local=True, images=[('img/lesson_8_question.png', 'Задание')], answer_link='lesson_8_final.html'),
            task('Лендинг за 30 минут', P('Сделай одностраничный сайт о своём хобби. Обязательно:',
                UL('шапка <code>&lt;header&gt;</code> с меню <code>&lt;nav&gt;</code> (минимум 3 ссылки)',
                   'заголовок <code>&lt;h1&gt;</code>', 'минимум два раздела <code>&lt;section&gt;</code>',
                   'подвал <code>&lt;footer&gt;</code>', 'меню — в одну строку с помощью flexbox',
                   'ссылки меню меняются при наведении (<code>:hover</code>)')),
                level=3, new=True,
                tests=[has('header'), has('header nav a, nav a', 'В меню не меньше 3 ссылок', min=3), has('h1'),
                       has('section', 'Не меньше двух section', min=2), has('footer'), style('nav', 'display', 'flex'),
                       dom('Есть эффект :hover для ссылок', 'return !!rule(/a:hover/) || "Добавь правило для a:hover";')],
                solution=page('''
<header>
    <nav>
        <a href="#about">Обо мне</a>
        <a href="#hobby">Хобби</a>
        <a href="#contacts">Контакты</a>
    </nav>
</header>
<h1>Я люблю космос 🚀</h1>
<section id="about">
    <h2>Обо мне</h2>
    <p>Мне 12 лет, я учусь делать сайты.</p>
</section>
<section id="hobby">
    <h2>Моё хобби</h2>
    <p>Смотрю на звёзды в телескоп.</p>
</section>
<footer id="contacts">© 2024 Мой сайт</footer>
''', css='''
        body { margin: 0; font-family: sans-serif; }
        header { background-color: #1f1b3d; padding: 16px; }
        nav { display: flex; gap: 20px; justify-content: center; }
        nav a { color: white; text-decoration: none; }
        nav a:hover { color: #ffd23f; }
        h1, section { text-align: center; }
        footer { background-color: #1f1b3d; color: white; text-align: center; padding: 16px; }
''')),
        ]),
        sec('Повторяем прошлые уроки', emoji='🔁', items=[
            note('Пройдись по урокам <a href="lesson_1.html">1</a>, <a href="lesson_2.html">2</a>, <a href="lesson_3.html">3</a>, '
                 '<a href="lesson_4.html">4</a>, <a href="lesson_5.html">5</a>, <a href="lesson_6.html">6</a> и проверь, '
                 'все ли задания выполнены.'),
        ]),
    ],
)

LESSONS = [L1, L2, L3, L4, L5, L6, L7, L8]
