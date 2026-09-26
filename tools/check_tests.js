// Проверяет, что эталонные решения всех заданий проходят автотесты.
// Запуск из корня репозитория (нужен Node.js и playwright):
//     python3 tools/build.py && node tools/check_tests.js [lesson_3.html ...]
const http = require('http');
const fs = require('fs');
const path = require('path');

let chromium;
try { ({ chromium } = require('playwright')); } catch (e) {
  const glob = require('child_process').execSync('npm root -g').toString().trim();
  ({ chromium } = require(path.join(glob, 'playwright')));
}

const ROOT = path.resolve(__dirname, '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.jpg': 'image/jpeg', '.gif': 'image/gif', '.svg': 'image/svg+xml' };

const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(p, (err, data) => {
    if (err) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' });
    res.end(data);
  });
});

(async () => {
  await new Promise((r) => server.listen(0, r));
  const port = server.address().port;
  const map = fs.readFileSync(path.join(ROOT, 'assets/course-map.js'), 'utf8');
  const files = process.argv.slice(2).length ? process.argv.slice(2)
    : JSON.parse(map.slice(map.indexOf('['), map.lastIndexOf(']') + 1)).map((l) => l.file);
  const opts = {};
  if (fs.existsSync('/opt/pw-browsers/chromium')) opts.executablePath = undefined;
  const browser = await chromium.launch(opts);
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  page.on('dialog', (d) => d.dismiss());
  let bad = 0, total = 0;
  for (const f of files) {
    await page.goto(`http://localhost:${port}/${f}`);
    const report = await page.evaluate(() => window.KKWeb.selfTest());
    for (const r of report) {
      total++;
      if (!r.ok) { bad++; console.log(`✗ ${f} · ${r.task}\n    ${r.msg.replace(/\n/g, '\n    ')}`); }
    }
    console.log(`${f}: ${report.filter((r) => r.ok).length}/${report.length}`);
  }
  await browser.close();
  server.close();
  console.log(bad ? `\nОшибок: ${bad} из ${total}` : `\nВсе ${total} эталонных решений проходят проверки ✔`);
  process.exit(bad ? 1 : 0);
})();
