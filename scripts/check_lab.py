#!/usr/bin/env python3
# check_lab.py index.html [--blind blind.json] [--compare answers.json] [--browser] [--shot <view-id>]
import json, pathlib, re, shutil, subprocess, sys, tempfile

args = sys.argv[1:]
path = pathlib.Path(args[0])
page = path.read_text(encoding="utf-8")
opt = lambda f: args[args.index(f) + 1] if f in args else None
err, warn = [], []

m = re.search(r'<script[^>]*id="lab-data"[^>]*>(.*?)</script>', page, re.S)
if not m:
    sys.exit('No <script type="application/json" id="lab-data"> block')
try:
    D = json.loads(m.group(1))
except json.JSONDecodeError as e:
    sys.exit(f"lab-data is not valid JSON ({e}); a literal </script> in a string also breaks it")
if not D.get("topics"):
    sys.exit("lab-data has no topics")

TAGS = {"b", "i", "em", "strong", "mark", "code", "sub", "sup", "br", "span", "kbd"}
def text(s, where):
    if not isinstance(s, str) or not s.strip():
        return err.append(f"{where}: empty text")
    for tag in re.findall(r"</?([A-Za-z][\w-]*)", s):
        if tag.lower() not in TAGS:
            err.append(f"{where}: raw <{tag}> (write &lt; for a literal <)")

srcs = {s.get("id", ""): s for s in D.get("sources", [])}
seen = {k: set() for k in srcs}
def ref(r, where):
    mm = re.fullmatch(r"(?:(\w+):)?(\d+)(?:-(\d+))?", str(r))
    if not mm or (mm.group(1) or "") not in srcs:
        return err.append(f"{where}: bad ref {r!r}")
    s, a, b = srcs[mm.group(1) or ""], int(mm.group(2)), int(mm.group(3) or mm.group(2))
    if not 1 <= a <= b <= s["pages"]:
        err.append(f"{where}: ref {r!r} is outside 1-{s['pages']}")
    seen[s.get("id", "")].update(range(a, b + 1))

keys = [t["key"] for t in D["topics"]]
BAN = re.compile(r"\b(all|none) of (the )?(above|these)\b|^both\b", re.I)
quiz = D.get("quiz", {})
for k in keys:
    if len(quiz.get(k, [])) < 5:
        warn.append(f"quiz {k}: {len(quiz.get(k, []))} questions (aim for 5-10)")
    for i, q in enumerate(quiz.get(k, []), 1):
        w = f"quiz {k}#{i}"
        if len(q) != 5:
            err.append(f"{w}: expected [prompt, options, answer, why, ref]"); continue
        p, opts, a, why, r = q
        text(p, w); text(why, w + " why"); ref(r, w)
        for o in opts:
            text(o, w + " option")
        if not 2 <= len(opts) <= 6:
            err.append(f"{w}: {len(opts)} options")
        if len({re.sub(r"\W", "", str(o).lower()) for o in opts}) < len(opts):
            err.append(f"{w}: duplicate options")
        if not isinstance(a, int) or not 0 <= a < len(opts):
            err.append(f"{w}: answer index {a!r}"); continue
        if any(BAN.search(str(o)) for o in opts):
            warn.append(f"{w}: 'all/none of the above' or 'both' option")
        rest = [len(str(o)) for j, o in enumerate(opts) if j != a]
        if len(opts[a]) > 30 and len(opts[a]) > 1.3 * max(rest):
            warn.append(f"{w}: the correct option is the longest by far")

fronts, per = set(), {k: 0 for k in keys}
for i, c in enumerate(D.get("cards", []), 1):
    w = f"card {i}"
    if len(c) != 4 or c[0] not in keys:
        err.append(f"{w}: expected [topic, front, back, ref] with a known topic"); continue
    t, f, b, r = c
    text(f, w); text(b, w + " back"); ref(r, w); per[t] += 1
    if f.lower() in fronts:
        err.append(f"{w}: duplicate front {f!r}")
    fronts.add(f.lower())
    if "?" not in f and len(f.split()) <= 3 and not re.match(r"(define|name|list|state|give|explain|describe|compare)\b", f, re.I):
        warn.append(f"{w}: front {f!r} is a topic, not a question")
    if len(b) > 220:
        warn.append(f"{w}: back is {len(b)} characters; split it")
warn += [f"cards {k}: only {n}" for k, n in per.items() if n < 3]

for k, items in D.get("written", {}).items():
    for i, x in enumerate(items, 1):
        w = f"written {k}#{i}"
        if k not in keys or len(x) != 4 or len(x[1]) < 2:
            err.append(f"{w}: expected [prompt, [2+ key points], model answer, ref]"); continue
        text(x[0], w); text(x[2], w + " model"); ref(x[3], w)
        for pt in x[1]:
            text(pt, w + " point")
for g in D.get("games", []):
    w, ch = f"game {g.get('id')}", g.get("choices", [])
    if len(ch) < 2 or not g.get("items"):
        err.append(f"{w}: needs 2+ choices and some items")
    for it in g.get("items", []):
        text(it[0], w)
        if it[1] not in ch:
            err.append(f"{w}: {it[1]!r} is not one of the choices")
for rid, items in D.get("reveal", {}).items():
    for i, x in enumerate(items, 1):
        w = f"reveal {rid}#{i}"
        if len(x) != 4 or x[1] not in ("y", "n", "p"):
            err.append(f"{w}: expected [question, 'y'|'n'|'p', answer, ref]"); continue
        text(x[0], w); text(x[2], w + " answer"); ref(x[3], w)
for k, items in D.get("traps", {}).items():
    for i, s in enumerate(items, 1):
        text(s, f"trap {k}#{i}")
for sid, s in srcs.items():
    miss = sorted(set(range(1, s["pages"] + 1)) - seen[sid] - set(s.get("skip", [])))
    if miss:
        warn.append(f"{s.get('name', sid)}: pages {miss} are used by no question, card or reveal (cover them or add to skip)")

node = shutil.which("node")
gen_keys = []
g = re.search(r'<script[^>]*id="lab-gen"[^>]*>(.*?)</script>', page, re.S)
if g and node:
    harness = r"""const vm=require('vm'),src=require('fs').readFileSync(0,'utf8'),ctx={};vm.createContext(ctx);
vm.runInContext(src+';this.GEN=GEN',ctx);let s=7;const rnd=()=>(s=s*16807%2147483647)/2147483647;
const r={rnd,int:(a,b)=>a+Math.floor(rnd()*(b-a+1)),pick:a=>a[Math.floor(rnd()*a.length)]};let n=0;
for(const[k,list]of Object.entries(ctx.GEN))for(const x of list)for(let i=0;i<500;i++){const p=x.make(r);n++;
const ok=p&&typeof p.q==='string'&&p.q&&(typeof p.ans==='string'?p.ans.trim():Number.isFinite(p.ans))&&Array.isArray(p.steps)&&p.steps.length;
if(!ok){console.log(k+' "'+x.title+'" gave '+JSON.stringify(p));process.exit(1)}}
console.log(n+' generated problems ok');console.log(JSON.stringify(Object.keys(ctx.GEN)))"""
    res = subprocess.run([node, "-e", harness], input=g.group(1), capture_output=True, text=True)
    if res.returncode:
        err.append(f"generator: {(res.stdout + res.stderr).strip()[:400]}")
    else:
        print(res.stdout.splitlines()[0]); gen_keys = json.loads(res.stdout.splitlines()[-1])
for i, s in enumerate(re.findall(r'<script(?![^>]*application/json)(?![^>]*\ssrc=)[^>]*>(.*?)</script>', page, re.S), 1):
    if not node:
        warn.append("node not found: script checks skipped"); break
    tmp = pathlib.Path(tempfile.mkstemp(suffix=".js")[1]); tmp.write_text(s, encoding="utf-8")
    res = subprocess.run([node, "--check", str(tmp)], capture_output=True, text=True)
    if res.returncode:
        err.append(f"script {i} syntax: " + " | ".join(res.stderr.strip().splitlines()[:4]))

hooks = [f'data-quiz="{k}"' for k in keys] + ['id="pips"', 'id="deck"', 'data-quiz="mistakes"', 'id="sheetbox"', 'data-quiz="final"']
hooks += [f'data-written="{k}"' for k in D.get("written", {})] + [f'data-gen="{k}"' for k in gen_keys]
hooks += [f'data-game="{x.get("id")}"' for x in D.get("games", [])] + [f'data-reveal="{k}"' for k in D.get("reveal", {})]
warn += [f"page has no {h} element, so that part never shows" for h in hooks if h not in page]

if opt("--blind"):
    blind = {f"{k}#{i}": [q[0]] + [f"{'ABCDEF'[j]}. {o}" for j, o in enumerate(q[1])] for k in keys for i, q in enumerate(quiz.get(k, []), 1)}
    pathlib.Path(opt("--blind")).write_text(json.dumps(blind, ensure_ascii=False, indent=1), encoding="utf-8")
if opt("--compare"):
    got = json.loads(pathlib.Path(opt("--compare")).read_text(encoding="utf-8"))
    for k in keys:
        for i, q in enumerate(quiz.get(k, []), 1):
            if not isinstance(q[2], int) or not 0 <= q[2] < len(q[1]):
                continue
            mine, theirs = "ABCDEF"[q[2]], str(got.get(f"{k}#{i}", "?")).strip()[:1].upper()
            if theirs != mine:
                err.append(f"blind check {k}#{i}: key says {mine}, blind reader says {theirs}: {q[0][:70]}")

LOOK = """v => { const el = document.getElementById(v);
  if (!el || el.hidden || !el.getClientRects().length) return {shown: false};
  const o = {shown: true, empty: el.innerText.trim().length < 20, wide: document.documentElement.scrollWidth > innerWidth + 1, bad: []};
  for (const svg of el.querySelectorAll('svg')) { const box = svg.getBoundingClientRect();
    const t = [...svg.querySelectorAll('text')].map(x => [x.textContent.trim(), x.getBoundingClientRect()]).filter(x => x[1].width);
    t.forEach(([s, a], i) => {
      if (a.left < box.left - 1 || a.right > box.right + 1 || a.top < box.top - 1 || a.bottom > box.bottom + 1) o.bad.push('clipped label: ' + s);
      t.slice(i + 1).forEach(([s2, b]) => { const ix = Math.min(a.right, b.right) - Math.max(a.left, b.left), iy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (ix > 0 && iy > 0 && ix * iy > 0.25 * Math.min(a.width * a.height, b.width * b.height)) o.bad.push('overlapping labels: ' + s + ' / ' + s2); }); }); }
  return o; }"""
POKE = """() => { const v = document.querySelector('section.view:not([hidden])'); if (!v) return;
  v.querySelectorAll('input:not([type=checkbox]):not([type=radio]), textarea').forEach(i => { if (!i.value) { i.value = i.type === 'number' ? '1' : 'test'; i.dispatchEvent(new Event('input', {bubbles: true})); } });
  const els = [...v.querySelectorAll('button, [role=button], input[type=checkbox], summary')].filter(e => e.getClientRects().length && !e.disabled);
  if (els.length) els[Math.floor(Math.random() * els.length)].click(); }"""

def browser_check():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return warn.append("browser check skipped: Playwright for Python is not installed")
    with sync_playwright() as pw:
        br = None
        for kw in ({}, {"channel": "chrome"}):
            try:
                br = pw.chromium.launch(**kw); break
            except Exception:
                pass
        if not br:
            return warn.append("browser check skipped: no Chromium or Chrome to launch")
        for wd, ht in ((1280, 900), (360, 760)):
            pg = br.new_page(viewport={"width": wd, "height": ht})
            pg.on("pageerror", lambda e, wd=wd: err.append(f"[{wd}px] JS error: {e}"))
            pg.on("console", lambda c, wd=wd: c.type == "error" and err.append(f"[{wd}px] console: {c.text}"))
            pg.goto(path.resolve().as_uri()); pg.wait_for_timeout(500)
            for v in pg.eval_on_selector_all("section.view", "els => els.map(e => e.id)"):
                pg.evaluate("v => { location.hash = v }", v); pg.wait_for_timeout(250)
                o = pg.evaluate(LOOK, v)
                if not o["shown"]:
                    err.append(f"[{wd}px] #{v} does not show when its hash is opened"); continue
                if o["empty"]:
                    err.append(f"[{wd}px] #{v} is empty")
                if o["wide"]:
                    warn.append(f"[{wd}px] #{v} is wider than the screen")
                warn.extend(sorted({f"[{wd}px] #{v} {b}" for b in o["bad"]}))
                if v == opt("--shot"):
                    pg.screenshot(path=f"shot-{v}-{wd}.png", full_page=True)
                for _ in range(60):
                    pg.evaluate(POKE); pg.wait_for_timeout(15)
            pg.close()
        br.close()
if "--browser" in args:
    browser_check()

c = D.get("cards", [])
print(f"{len(keys)} topics, {sum(len(quiz.get(k, [])) for k in keys)} quiz questions, {len(c)} cards, "
      f"{sum(len(v) for v in D.get('written', {}).values())} written, {len(gen_keys)} topics with generators, {len(D.get('games', []))} games")
for x, n in dict.fromkeys(err, 0).items():
    print("ERROR", x + (f" (x{err.count(x)})" if err.count(x) > 1 else ""))
for x in dict.fromkeys(warn):
    print("warn ", x)
sys.exit(1 if err else 0)
