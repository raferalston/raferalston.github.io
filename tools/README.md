# Домашние задания по веб-дизайну — как редактировать

Страницы `index.html` и уроков (`lesson_1.html` … `lesson_8.html`, `lesson_9_adv.html` … `lesson_36_adv.html`)
**генерируются**. Не правь их руками, иначе изменения пропадут при следующей сборке.
Страницы-образцы и ответы (`flex_example.html`, `lesson_21_ans_1.html` и т. п.) остаются как есть.

1. Задания лежат в `tools/lessons_1.py` (уроки 1–8), `tools/lessons_2.py` (9–16), `tools/lessons_3.py` (17–24),
   `tools/lessons_4.py` (25–36). Помощники — в `tools/kk_helpers.py`.
2. Добавь или измени `task(...)`. Основные поля:
   - `level` — сложность 1–3, `new=True` — метка «новое»;
   - `mode` — `'html'` (редактор всей страницы с живым просмотром) или `'js'` (редактор JavaScript + консоль);
   - `starter` — стартовый код, `fixture` — HTML, внутри которого выполняется JavaScript (для `mode='js'`);
   - `tests` — автопроверка: `has('ul > li', min=5)`, `style('h1', 'color', 'red')`, `io(ввод, ожидаемый_вывод)`,
     `call('pow(3)', '9')`, `var_is('x', '5')`, `code_has(regex, подпись)`, `dom(подпись, js)` — любая проверка на JS;
   - `solution` — эталонное решение (показывается в «Показать ответ», по нему проверяются тесты);
   - `example` — ссылка на страницу-образец, `answer_link` / `answer_pages` — старые страницы с ответами;
   - `local=True` — большое задание для VS Code (без редактора на странице).
3. Собери страницы и проверь, что эталонные решения проходят тесты, а стартовый код — нет:

```bash
python3 tools/build.py
node tools/check_tests.js            # нужен Node.js и пакет playwright
```

Код учеников выполняется в изолированном iframe (`assets/kk.js`), редактор — CodeMirror с jsDelivr.
Код и отметки о выполнении хранятся в localStorage браузера ученика.
Стиль общий с домашкой по Python (kidkodschool.github.io): цвета бренда — CSS-переменные в начале `assets/kk.css`.

Пасхалка с шифром сейфа (уроки 1, 4, 5 → `lesson_5_test.html`) сохранена: `attrs`/`title_attrs` в шагах урока 1,
`head_extra`/`body_extra` в уроках 4 и 5.
