---
name: "mshmsh-study"
description: "Turns lectures, slides or notes into a published study lab with diagrams, quizzes, practice problems, flashcards, a mistakes deck and a timed final, every fact tied to its slide. Use for quiz, midterm or final prep, 'make this fun to study', or when someone says mshmsh-study (or its old name, study-xoshaka)."
---

# mshmsh-study: interactive study labs

You turn course material into one published HTML study page, a "lab". The student opens it the night before a quiz or exam, so it has to be right, cover every slide, show where each fact comes from, and work on a phone.

You write the content as one JSON block, the topic visuals as HTML and SVG, and any problem generators. The engine, its stylesheet and the checker in the appendix do the rest. They are tested, so copy them instead of writing your own.

## 1. Read the source and learn the exam format

**Find the files.** Read attachments by name. Material can also come from a connected folder on the student's computer, Google Drive, a claude.ai Project, pasted text, or a YouTube lecture through a transcript tool such as the `see` skill.

**Read all of it.**
- PDF: read every page. When a page is mostly a diagram or its text is thin, render it with `pdftoppm -r 110 -png` and look at the image.
- PPTX: get the slide text and the speaker notes with `markitdown` or python-pptx, because lecturers often explain things in the notes. Render the slides with `soffice --headless --convert-to pdf` and `pdftoppm` to see the diagrams.
- Photos and scans: read them and transcribe what you see.

**Index the slides first.** Write one line per slide with its number, title and content. Mark slides with nothing to test, such as the title, agenda or references, as skip. Pasted notes and videos have no page numbers, so number the sections or minutes yourself and tell the student.

Write down every slide you couldn't read, such as a blurry photo or a diagram with no text. Never fill one in from memory. Put a `<p class="flag">` at that spot in the topic instead, for example "Slide 17 is a diagram I couldn't read. These four types are the textbook's, so check the slide."

**Exam format.** If the student hasn't said, ask once as a multi-select, with AskUserQuestion if you have it: multiple choice, written answers, problems and calculations, or not sure. If nobody answers, build the mix and say so in the reply.

**Past papers.** If the student shares past exams or the lecturer's sample questions, copy their question types, wording, difficulty and verbs. Note which topics came up before. Label your own questions as practice, never as the real exam.

**Graded work.** If the material is an assignment or take-home test the student will hand in, don't publish its answers. Build practice on the same lectures instead.

## 2. Outline the topics

Split the material into 5 to 8 topics per chapter, in the lecture's order and under its headings. For several chapters, group the topics by chapter. Past about 12 topics, ask whether the student wants one lab per chapter.

For each topic, pull out:
- Definitions in the lecture's wording. Quote short ones exactly.
- Lists with counts, such as "4 requirements" or "8 foundations". Counts make good questions.
- Names, years and places, meaning who did what and when.
- Formulas and procedures, with the lecture's notation, units and rounding.
- Traps, the pairs that are easy to mix up. Examples are two similar phrasings ("Can formal rules…" is Philosophy, "What are the formal rules…" is Mathematics), one term with two meanings, or the neighboring algorithm.
- What the lecturer stressed, such as anything marked important, repeated, boxed or bold.
- Open or discussion questions in the slides. Give the textbook answer with a short reason, and mark anything that has changed since the textbook.

When the lecture disagrees with the textbook or with common knowledge, follow the lecture, because that is what gets marked, and point out the difference in the explanation.

Cover every point in the source and don't drop any to save space. Every slide that isn't marked skip must feed at least one question, card or reveal, and the checker lists the slides that don't.

## 3. Give each topic a visual

Choose by the shape of the content, not for looks.

| Content shape | Visual |
|---|---|
| Two axes with two values each (Think/Act × Human/Rational) | colored 2×2 matrix with a header row and column |
| A process, protocol or test setup | inline SVG with people, rooms, arrows and labels |
| An algorithm run or a calculation (scheduling, page replacement, a handshake) | trace table or Gantt chart that builds up step by step |
| A thought experiment or story | SVG with Back and Next that lights up the part each step talks about |
| A base list and an extended list | toggle that lights up the extra items, 4 growing to 6 |
| Several fields feeding one idea | hub grid with the core in the center |
| Levels or progression | staircase with a "We are here" marker |
| A formula | the lecture's worked example, numbers substituted line by line |
| Code | a short snippet with its output or a bug to find |
| Key numbers | stat tiles |
| History | vertical timeline with a year pill, title and one line, ongoing eras marked "to today" |
| Yes/no judgment questions | reveal cards with YES, NO or PARTLY |
| A logic chain | stacked boxes with the conclusion highlighted |
| Plain lists to memorize | chips |

Highlight the must-memorize phrases with `<mark>`. Add a "Traps" box wherever topics are easy to confuse, and put the same traps in the data so the Sheet shows them.

In diagrams, name the main parts on the drawing and put longer explanations in HTML beside it. Give every label its own clear space. On phones a wide SVG scrolls sideways inside its own box.

Steps work on any figure. Mark it `data-steps` and list the captions in `<ol class="caps" hidden>`. Then mark parts with `data-s="1 3"` to light them at steps 1 and 3 and dim them otherwise, or with `data-from="2"` to show them from step 2 on. Use `data-from` to build trace tables and Gantt charts and `data-s` to walk through a story.

## 4. Make it active

Each topic ends with practice that matches the exam.
- **Quiz**, always. 5 to 10 multiple-choice or true/false questions, one at a time, with instant feedback and a one- or two-sentence explanation showing the slide number, then the score, the missed list and Retry.
- **Written**, for written exams or an unknown format. 1 to 3 questions per topic in the lecturer's verbs: define, explain, compare, list four. The student writes an answer, ticks the key points it covered and reads a model answer. If `describe_capabilities` lists `sample`, declare it after publishing as step 7 says, and the engine shows Check with Claude, which marks the answer against the key points.
- **Practice problems**, whenever the lecture has a method with a fixed answer, such as formulas, waiting times, page faults, subnetting, number conversions or truth tables. Each problem type gets a generator that makes new numbers every time, allows two tries, then shows the worked solution in the lecture's steps.

Across the page:
- **Mini-games**, one or two. The student sorts items into groups, such as definition to term or question to field, in random order with a streak counter.
- **Flashcards** tab. One card per key fact from every topic, with Again and Got it buttons. A known card comes back after 1, 3, 7 and then 14 days. It also has a topic filter and Study all.
- **Mistakes** tab. A missed quiz question from anywhere on the page stays here until the student gets it right twice in a row.
- **Sheet** tab. Every card as question and answer plus the traps, by topic, for the 15-minute review before the exam.
- **Final** tab. 20 questions from all topics, weighted toward weak topics and mistakes, plus a few generated problems, with a timer and a new mix each time.
- **Progress** in the header. The best score per topic, the number of mistakes and the cards due, saved in the browser.
- A "Tonight" line under the header that links Sheet, the topic quizzes, Mistakes and Final in that order.

### Writing questions
- Each question has exactly one defensible answer, and the lecture alone settles it.
- Distractors are real terms from the same lecture, such as other authors, other years, the neighboring category or the trap partner, so the student has to know the difference.
- Options are parallel, with the same grammar and about the same length. The right one is never the longest or the only detailed one. Avoid "all of the above", "none of the above" and "both A and B" unless you are copying the lecturer's own past paper.
- Mix the levels. About 40% recall definitions, counts and names. About 40% test understanding with why, compare or "which is <b>NOT</b> one of the four". About 20% apply a concept to a new case.
- Turn every trap and every count into a question.
- Work out every number in a question or answer with code, never in your head.
- The explanation says why the answer is right and names the fact it gets confused with, in one or two sentences. The page adds the slide number from the ref.
- The engine shuffles the options of every question except true/false, so answer position doesn't matter.

### Writing flashcards
- One fact per card. The front is a specific question, not a topic. Write "What does the Turing test check?", not "Turing test".
- The back is a phrase or one sentence. If it needs a paragraph, split it into more cards.
- For a list, make one card for the count and one for each item that matters.
- Make as many cards as there are key facts, often 25 to 60. Eight correct cards beat twenty with one wrong, so never pad the deck.

### Writing problem generators
Put them in `<script id="lab-gen">` as `var GEN = {t3: [{title: "…", ref: "20-22", make: function (r) {…}}]};`. The `r` argument gives `r.int(a, b)`, `r.pick(list)` and `r.rnd()`.

`make` returns `{q, ans, tol, unit, steps}`. `q` is the problem as HTML, `ans` is a number or exact text such as `"255.255.255.192"`, `tol` is the accepted error, and `steps` holds the worked solution lines with the student's numbers in them.

Follow the lecture's method and rounding. If the lecture reads factors from tables rounded to four decimals, set `tol` so table answers pass. Keep the numbers realistic, and avoid zeros and ties unless the lecture covers them. Print three generated problems with Node, work them by hand, and confirm that `ans` matches the last step. The checker runs every generator 500 times.

## 5. Build one HTML file

Work in `<course>-ch<N>/`. Copy the engine, its stylesheet and the checker out of this file instead of retyping them. The skill's base directory is printed when the skill loads.

```bash
python3 - "<skill base dir>/SKILL.md" <<'EOF'
import re, sys
fence = "`" * 3
for name, body in re.findall(fence + r"\w+ file=(\S+)\n(.*?)" + fence, open(sys.argv[1], encoding="utf-8").read(), re.S):
    open(name, "w", encoding="utf-8").write(body)
EOF
```

If SKILL.md isn't on disk, copy the three appendix blocks by hand.

Write `index.html` from the skeleton below, with `/*ENGINE_CSS*/` inside your `<style>` and `/*ENGINE*/` as the last script. Then fill both in:

```bash
python3 -c "import pathlib as p; f = p.Path('index.html'); t = f.read_text(encoding='utf-8'); f.write_text(t.replace('/*ENGINE_CSS*/', p.Path('engine.css').read_text(encoding='utf-8')).replace('/*ENGINE*/', p.Path('engine.js').read_text(encoding='utf-8')), encoding='utf-8')"
```

```html
<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OS Ch5 Study Lab</title>
<style>/* tokens, fonts, layout, your visuals */ /*ENGINE_CSS*/</style></head>
<body>
<header><h1>Operating Systems Chapter 5 Study Lab</h1><p>CPU scheduling, Dr. …</p>
  <p>Tonight: <a href="#sheet">Sheet</a>, <a href="#topic-1">topic quizzes</a>, <a href="#mistakes">Mistakes</a>, <a href="#final">Final</a></p>
  <div id="pips"></div></header>
<nav><a href="#topic-1">1 Basics</a> <a href="#topic-2">2 FCFS and SJF</a> <a href="#cards">Flashcards</a>
  <a href="#mistakes">Mistakes</a> <a href="#sheet">Sheet</a> <a href="#final">Final</a></nav>
<main>
<section class="view" id="topic-1"><p>Topic 1</p><h2>Scheduling basics</h2><p>One-line lead.</p>
  <!-- visual plates and the Traps box -->
  <div data-reveal="r1"></div> <div data-game="g1"></div>
  <div data-written="t1"></div> <div data-gen="t1"></div> <div data-quiz="t1"></div>
</section>
<section class="view" id="topic-2" hidden>…</section>
<section class="view" id="cards" hidden><h2>Flashcards</h2><div id="deck"></div></section>
<section class="view" id="mistakes" hidden><h2>Mistakes</h2><div data-quiz="mistakes"></div></section>
<section class="view" id="sheet" hidden><h2>Sheet</h2><div id="sheetbox"></div></section>
<section class="view" id="final" hidden><h2>Final challenge</h2><div data-quiz="final"></div></section>
</main>
<script type="application/json" id="lab-data">{ … }</script>
<script id="lab-gen">var GEN = { … };</script>
<script>/*ENGINE*/</script>
</body></html>
```

Rules for the page:
- Each tab is one `<section class="view">`, and all but the first are `hidden`. Ids are plain ASCII, like `topic-1`, `cards`, `mistakes`, `sheet` and `final`. Never use `settings`, `sidebar`, `customize`, `upgrade`, `downloads` or `comment-*`, which claude.ai reserves.
- Every topic has a `data-quiz` hook. Leave out the other hooks a topic doesn't use.
- The page runs in a sandbox, so alert, confirm, prompt, print and downloads don't work.

All content lives in the data block. Strings are HTML, so write a literal `<` as `&lt;` and use only the tags b, i, em, strong, mark, code, sub, sup, br, span and kbd.

```json
{"title": "Operating Systems · Chapter 5 Study Lab",
 "sources": [{"id": "", "name": "OS_Ch5.pdf", "pages": 42, "skip": [1, 2, 42], "unit": "Slide"}],
 "topics": [{"key": "t1", "title": "Scheduling basics"}],
 "quiz": {"t1": [["Prompt?", ["A", "B", "C", "D"], 1, "Why B is right; C is the trap.", "12"]]},
 "written": {"t2": [["Compare X and Y.", ["key point", "key point"], "Model answer in 2 to 4 sentences.", "14-15"]]},
 "cards": [["t1", "Front question?", "Back answer.", "8"]],
 "games": [{"id": "g1", "choices": ["Maximize", "Minimize"], "items": [["Throughput", "Maximize", "optional note"]]}],
 "reveal": {"r1": [["Is a thermostat an agent?", "p", "Partly, because …", "9"]]},
 "traps": {"t1": ["Throughput is jobs per unit time; turnaround is the time one job takes."]},
 "finalSize": 20}
```

Quiz answers are 0-based option indexes. Refs are slide numbers or ranges, such as "12" or "12-14". With several files, give each source an id and write refs like "L2:12". The page shows `unit` before the number, for example Slide, Page or Min.

**Design.** Read the artifact `guide` design topic once, then follow these lab rules.
- Take colors from the subject, and pair a display face with a readable body face from Google Fonts, with fallbacks. No purple gradients, emoji icons, Bricolage Grotesque or theme switch.
- Define tokens with `light-dark()` and add `[data-theme]` overrides, so light, dark and system mode all read well. engine.css uses `--bg`, `--surface`, `--ink`, `--muted`, `--line`, `--accent`, `--hl`, `--good-strong`, `--bad-strong` and `--warn-strong`.
- Put white text only on fixed dark colors (`--good-strong:#12704a`, `--bad-strong:#b3342d`, `--warn-strong:#8a5d00`), never on a theme token that turns light in dark mode.
- On phones, use one column below 600px, nothing wider than 360px, a nav that scrolls sideways, 44px tap targets and 16px inputs. Keep visible focus styles and respect `prefers-reduced-motion`.
- Give the Final link in the nav a dashed border so it stands apart.
- Restyle engine.css to match the lab, but keep its class names.
- For Kurdish or Arabic, the engine sets `dir="auto"` on the text it renders. Set `dir="rtl"` on your own right-to-left blocks. For a lab fully in Kurdish or Arabic, translate the button and label strings in your copy of the engine.

## 6. Check once, then fix

1. Run `python3 check_lab.py index.html --browser --shot topic-N`, with N the most diagram-heavy topic. Fix every ERROR. Fix these warnings as well: uncovered slides, card fronts that are topics, long backs, a correct option much longer than the rest, and overlapping or clipped labels.
2. Check the answer key blind. `--blind blind.json` writes the questions without answers. Give a fresh agent the source files and blind.json, and ask for `{"t1#1": "B", …}` from the lecture alone, with "?" where the lecture doesn't settle it or two options fit. Run `--compare answers.json` and fix each disagreement, whether it is a wrong key, unclear wording or two defensible options. Without an agent tool, answer blind.json yourself from the source without looking at the key.
3. Look at the two screenshots once. Fix what you see, rerun the checker, then stop. Don't loop.

## 7. Publish
- Call `list_types` first. A lab matches none of the types, so it is a hand-built page. Read the `guide` pages topic once per session.
- Publish with `publish_files`, using the page title as the title and `study` as the icon. The published page is the delivery, so don't send the file as well.
- If the page uses Check with Claude, call `declare_capabilities` with `{sample: {}}` after publishing.
- Look for an earlier lab of the same course with `list_artifacts` and the course name. If there is one, match its look so the course reads as one set, and link the labs to each other.
- To revise, edit the file, rerun the checker and republish to the same slug with `base_version`.

## 8. Reply
Keep it short. Give one line on what the page is, the tabs and what each does, and the Tonight order. **Flag anything you couldn't read in the source or that isn't from the lecture**, for example "the functionality types in Topic 4 are the standard ones; check the slide diagram". Write lecturers' names with their titles (Dr., Mr., د.). Use English unless the student asks for Kurdish or Arabic.

## Fixes and new chapters
- When the student reports a wrong answer, check the slide, fix the data, rerun the checker and republish to the same slug.
- For a new chapter of the same course, add its topics to the same lab so the Final mixes both, unless the student wants a separate page.
- If the student wants paper, make the Sheet content into a doc with the Docs type, which exports PDF and Word. The lab page can't print.

## Chat-only variant
If the student only wants a quick walkthrough in chat, explain each topic simply, with tables for anything you can compare, and put a `quiz_display_v0` widget after each topic. Then offer the full lab.

## Appendix: engine, stylesheet and checker

Step 5 copies these out. Don't rewrite them. If a lab needs something new, add it in your copy.

```js file=engine.js
{
const D = JSON.parse(document.getElementById('lab-data').textContent), G = window.GEN || {};
const $ = (s, el = document) => el.querySelector(s), $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const strip = s => String(s).replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const hash = s => { let h = 0; for (const c of String(s)) h = (h * 31 + c.codePointAt(0)) | 0; return (h >>> 0).toString(36); };
const R = {rnd: Math.random, int: (a, b) => a + Math.floor(Math.random() * (b - a + 1)), pick: a => a[Math.floor(Math.random() * a.length)]};
const TITLE = Object.fromEntries(D.topics.map(t => [t.key, t.title]));
const refTxt = r => {
  const m = String(r || '').match(/^(?:(\w+):)?(\d+)(?:-(\d+))?$/); if (!m) return '';
  const src = (D.sources || []).find(x => (x.id || '') === (m[1] || '')) || {}, u = src.unit || 'Slide';
  return '<span class="ref">' + (m[1] ? m[1] + ' · ' : '') + u + (m[3] ? 's ' + m[2] + '–' + m[3] : ' ' + m[2]) + '</span>';
};
const verdict = ok => '<span class="pill ' + (ok ? 'good' : 'bad') + '">' + (ok ? 'Right' : 'Not quite') + '</span> ';
const clock = t0 => { const s = Math.round((Date.now() - t0) / 1000); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };

// progress: best scores, mistakes (id -> correct-in-a-row), flashcard boxes (id -> [box, due])
const KEY = 'sx:' + D.title;
const store = (() => { try { localStorage.setItem(KEY + ':t', 1); localStorage.removeItem(KEY + ':t'); return localStorage; } catch (e) { return null; } })();
let S = {best: {}, miss: {}, box: {}};
try { S = Object.assign(S, JSON.parse(store && store.getItem(KEY)) || {}); } catch (e) {}
const save = () => { try { if (store) store.setItem(KEY, JSON.stringify(S)); } catch (e) {} renderPips(); };

const ALL = D.topics.flatMap(t => ((D.quiz || {})[t.key] || []).map(q => ({id: t.key + ':' + hash(q[0]), t: t.key, p: q[0], o: q[1], a: q[2], why: q[3], ref: q[4]})));
const BYID = Object.fromEntries(ALL.map(q => [q.id, q]));
const CARDS = (D.cards || []).map(c => ({id: c[0] + ':' + hash(c[1]), t: c[0], f: c[1], b: c[2], ref: c[3]}));
const GENS = Object.entries(G).flatMap(([t, list]) => list.map(g => [t, g]));
const due = c => { const s = S.box[c.id]; return !s || s[1] <= Date.now(); };

// numeric or text answers from problem generators
const norm = s => String(s).toLowerCase().replace(/\s+/g, '');
const judge = (q, raw) => {
  if (typeof q.ans === 'string') return norm(raw) === norm(q.ans);
  let s = String(raw).replace(/\s/g, ''); s = /,/.test(s) && !/\./.test(s) ? s.replace(',', '.') : s.replace(/,/g, '');
  const x = parseFloat(s), tol = q.tol != null ? q.tol : Math.max(0.01, Math.abs(q.ans) * 0.005);
  return Number.isFinite(x) && Math.abs(x - q.ans) <= tol + 1e-9;
};
const fmt = q => typeof q.ans === 'number' ? String(+q.ans.toFixed(4)) + (q.unit ? ' ' + q.unit : '') : q.ans;
const work = q => '<ol class="work">' + q.steps.map(s => '<li>' + s + '</li>').join('') + '</ol>';
const genHTML = q => '<p class="prompt" dir="auto">' + q.q + '</p><div class="row"><input class="ans" inputmode="decimal" autocomplete="off" aria-label="Your answer">' +
  (q.unit ? '<span>' + q.unit + '</span>' : '') + '<button class="check">Check</button></div><div class="fb" aria-live="polite"></div>';

function finalMix() {
  const N = Math.min(D.finalSize || 20, ALL.length + GENS.length), nGen = Math.min(GENS.length, Math.floor(N / 5)), out = [], taken = new Set();
  const add = q => { if (q && !taken.has(q.id) && out.length < N - nGen) { taken.add(q.id); out.push(q); } };
  shuffle(Object.keys(S.miss)).slice(0, Math.floor(N / 4)).forEach(id => add(BYID[id]));
  shuffle(D.topics).forEach(t => add(shuffle(ALL).find(q => q.t === t.key && !taken.has(q.id))));
  const weak = t => 1.5 - (S.best[t] == null ? 50 : S.best[t]) / 100;
  ALL.map(q => [Math.random() * weak(q.t), q]).sort((a, b) => b[0] - a[0]).forEach(x => add(x[1]));
  shuffle(GENS).slice(0, nGen).forEach(([t, g]) => out.push(Object.assign({gen: true, t, ref: g.ref}, g.make(R))));
  return shuffle(out);
}

function Quiz(el, key) {
  let items, i, score, missed, t0, first = true;
  const pick = () => key === 'final' ? finalMix() : key === 'mistakes' ? shuffle(Object.keys(S.miss).map(id => BYID[id]).filter(Boolean))
    : (first ? ALL.filter(q => q.t === key) : shuffle(ALL.filter(q => q.t === key)));
  const start = () => { items = pick(); first = false; i = 0; score = 0; missed = []; t0 = Date.now(); el.dataset.t0 = t0; show(); };
  const record = (q, ok) => {
    if (ok) score++; else missed.push(q);
    if (q.gen) return;
    if (!ok) S.miss[q.id] = 0; else if (q.id in S.miss && ++S.miss[q.id] >= 2) delete S.miss[q.id];
    save();
  };
  const nextBtn = fb => { fb.insertAdjacentHTML('beforeend', '<button class="next">' + (i + 1 < items.length ? 'Next' : 'See score') + '</button>'); const b = $('.next', fb); b.onclick = () => { i++; show(); }; b.focus({preventScroll: true}); };
  function show() {
    if (!items.length) { el.innerHTML = '<p class="muted">' + (key === 'mistakes' ? 'Nothing here yet. Questions you miss anywhere land here until you get them right twice in a row.' : 'No questions.') + '</p>'; return; }
    if (i >= items.length) return end();
    const q = items[i];
    const head = '<div class="qhead"><span>Question ' + (i + 1) + ' of ' + items.length + '</span>' + (key === 'final' ? '<span class="timer">' + clock(t0) + '</span>' : '') +
      (key !== q.t ? '<span class="tag">' + TITLE[q.t] + '</span>' : '') + '</div>';
    let done = false;
    if (q.gen) {
      el.innerHTML = head + genHTML(q);
      const inp = $('.ans', el), go = () => {
        if (done || !inp.value.trim()) return; done = true;
        const ok = judge(q, inp.value); inp.disabled = $('.check', el).disabled = true; record(q, ok);
        const fb = $('.fb', el); fb.innerHTML = '<p>' + verdict(ok) + 'Answer: <b>' + fmt(q) + '</b> ' + refTxt(q.ref) + '</p>' + work(q); nextBtn(fb);
      };
      $('.check', el).onclick = go; inp.onkeydown = e => { if (e.key === 'Enter') go(); };
      return;
    }
    const tf = q.o.length === 2 && q.o.every(o => /^(true|false)$/i.test(strip(o)));
    const order = tf ? [0, 1] : shuffle(q.o.map((_, j) => j));
    el.innerHTML = head + '<p class="prompt" dir="auto">' + q.p + '</p><div class="opts">' +
      order.map((j, n) => '<button class="opt" data-j="' + j + '"><kbd>' + (n + 1) + '</kbd><span dir="auto">' + q.o[j] + '</span></button>').join('') + '</div><div class="fb" aria-live="polite"></div>';
    $$('.opt', el).forEach(b => b.onclick = () => {
      if (done) return; done = true;
      const j = +b.dataset.j, ok = j === q.a;
      $$('.opt', el).forEach(x => { x.disabled = true; if (+x.dataset.j === q.a) x.classList.add('ok'); else if (x === b) x.classList.add('no'); });
      record(q, ok);
      const fb = $('.fb', el); fb.innerHTML = '<p dir="auto">' + verdict(ok) + q.why + ' ' + refTxt(q.ref) + '</p>'; nextBtn(fb);
    });
  }
  function end() {
    const pct = Math.round(100 * score / items.length);
    if (key !== 'mistakes') { S.best[key] = Math.max(S.best[key] || 0, pct); save(); }
    el.innerHTML = '<div class="score"><b>' + score + ' / ' + items.length + '</b> (' + pct + '%)' + (key === 'final' ? ' in ' + clock(t0) : '') + '</div>' +
      (missed.length ? '<p>Go back over these:</p><ul class="missed">' + missed.map(q => '<li dir="auto">' + (q.gen ? q.q : q.p) + ' <b>' + (q.gen ? fmt(q) : q.o[q.a]) + '</b> ' + refTxt(q.ref) + '</li>').join('') + '</ul>' : '<p>Nothing missed.</p>') +
      '<button class="retry">' + (key === 'final' ? 'New mix' : key === 'mistakes' ? 'Go again' : 'Retry') + '</button>';
    $('.retry', el).onclick = start;
  }
  if (key === 'final') {
    el.innerHTML = '<p>' + Math.min(D.finalSize || 20, ALL.length + GENS.length) + ' questions from every topic, weighted toward your weak spots and recent mistakes. Exam pace is about a minute each.</p><button class="begin">Start</button>';
    $('.begin', el).onclick = start;
  } else start();
  return {start};
}

function Practice(el, key) {
  const gens = G[key] || [];
  el.innerHTML = gens.map((g, n) => '<div class="prac" data-n="' + n + '"><h4>' + g.title + ' ' + refTxt(g.ref) + '</h4><div class="pbody"></div></div>').join('');
  $$('.prac', el).forEach(box => {
    const g = gens[+box.dataset.n], body = $('.pbody', box); let streak = 0;
    const next = () => {
      const q = g.make(R); let tries = 0, done = false;
      body.innerHTML = genHTML(q);
      const inp = $('.ans', body), fb = $('.fb', body);
      const reveal = ok => { done = true; inp.disabled = $('.check', body).disabled = true; streak = ok ? streak + 1 : 0;
        fb.innerHTML = '<p>' + verdict(ok) + 'Answer: <b>' + fmt(q) + '</b></p>' + work(q) + '<div class="row"><button class="new">New problem</button><span class="muted">Streak ' + streak + '</span></div>';
        $('.new', fb).onclick = next; };
      const go = () => {
        if (done || !inp.value.trim()) return;
        if (judge(q, inp.value)) return reveal(true);
        if (++tries >= 2) return reveal(false);
        fb.innerHTML = '<p><span class="pill warn">Not yet</span> Check your working and try once more.</p><button class="show">Show solution</button>';
        $('.show', fb).onclick = () => reveal(false); inp.select();
      };
      $('.check', body).onclick = go; inp.onkeydown = e => { if (e.key === 'Enter') go(); };
    };
    next();
  });
}

let SAMPLE = null;
if (window.claude && window.claude.use) window.claude.use('sample').then(s => { SAMPLE = s; document.body.classList.toggle('has-claude', !!s); }).catch(() => {});
function askClaude(w, answer, fb) {
  if (!SAMPLE) return;
  if (answer.trim().length < 15) { fb.innerHTML = '<p class="muted">Write your answer first, then check it.</p>'; return; }
  fb.innerHTML = '<p class="muted">Checking…</p>';
  SAMPLE.json('You mark a university exam answer. Judge it only against the key points and model answer below, which come from the lecture.\nQuestion: ' + strip(w[0]) +
    '\nKey points:\n' + w[1].map((p, k) => (k + 1) + '. ' + strip(p)).join('\n') + '\nModel answer: ' + strip(w[2]) + '\nStudent answer: """' + answer.slice(0, 3000) +
    '"""\nReply with JSON only: {"covered": [numbers of the key points the answer clearly makes], "wrong": "one incorrect statement in the answer, or empty", "tip": "one short sentence on what to add or fix"}', {modelTier: 'quick'})
    .then(r => {
      const got = new Set(((r && r.covered) || []).map(Number));
      fb.innerHTML = '<ul class="marks">' + w[1].map((p, k) => '<li class="' + (got.has(k + 1) ? 'hit' : 'gap') + '">' + (got.has(k + 1) ? 'Covered: ' : 'Missing: ') + p + '</li>').join('') + '</ul>' +
        (r && r.wrong ? '<p><b>Check this:</b> ' + esc(r.wrong) + '</p>' : '') + (r && r.tip ? '<p class="muted">' + esc(r.tip) + '</p>' : '');
    })
    .catch(e => { if (e && e.code === 'not_granted') { document.body.classList.remove('has-claude'); fb.innerHTML = ''; } else fb.innerHTML = '<p class="muted">Could not check right now. Use Show key points instead.</p>'; });
}
function Written(el, key) {
  const items = (D.written || {})[key] || [];
  el.innerHTML = items.map((w, n) => '<div class="wq" data-n="' + n + '"><p class="prompt">' + w[0] + ' ' + refTxt(w[3]) + '</p><textarea rows="4" aria-label="Your answer" placeholder="Answer it the way you would in the exam"></textarea>' +
    '<div class="row"><button class="show">Show key points</button><button class="ask needs-claude">Check with Claude</button></div><div class="wfb" aria-live="polite"></div></div>').join('');
  $$('.wq', el).forEach(box => {
    const w = items[+box.dataset.n], fb = $('.wfb', box);
    $('.show', box).onclick = () => {
      fb.innerHTML = '<p>Tick what your answer covered:</p>' + w[1].map(p => '<label class="pt"><input type="checkbox"> <span dir="auto">' + p + '</span></label>').join('') +
        '<p class="model" dir="auto"><b>Model answer.</b> ' + w[2] + '</p><p class="muted tally"></p>';
      const ticks = $$('input', fb), tally = () => { $('.tally', fb).textContent = ticks.filter(b => b.checked).length + ' of ' + ticks.length + ' key points'; };
      ticks.forEach(b => b.onchange = tally); tally();
    };
    $('.ask', box).onclick = () => askClaude(w, $('textarea', box).value, fb);
  });
}

function Game(el, id) {
  const g = (D.games || []).find(x => x.id === id); if (!g) return;
  let items, i, streak, best = 0, right;
  const start = () => { items = shuffle(g.items); i = 0; streak = 0; right = 0; show(); };
  function show() {
    if (i >= items.length) { el.innerHTML = '<div class="score"><b>' + right + ' / ' + items.length + '</b> sorted right · best streak ' + best + '</div><button class="again">Play again</button>'; $('.again', el).onclick = start; return; }
    const it = items[i]; let done = false, tm;
    el.innerHTML = '<div class="qhead"><span>' + (i + 1) + ' of ' + items.length + '</span><span>Streak ' + streak + '</span></div><p class="prompt">' + it[0] + '</p><div class="choices">' +
      g.choices.map((c, n) => '<button class="choice" dir="auto" data-c="' + n + '">' + c + '</button>').join('') + '</div><div class="fb" aria-live="polite"></div>';
    $$('.choice', el).forEach(b => b.onclick = () => {
      if (done) return; done = true;
      const ok = g.choices[+b.dataset.c] === it[1]; streak = ok ? streak + 1 : 0; best = Math.max(best, streak); if (ok) right++;
      $$('.choice', el).forEach(x => { x.disabled = true; if (g.choices[+x.dataset.c] === it[1]) x.classList.add('ok'); else if (x === b) x.classList.add('no'); });
      const fb = $('.fb', el); fb.innerHTML = '<p dir="auto">' + verdict(ok) + (it[2] || '') + '</p><button class="next">Next</button>';
      const go = () => { clearTimeout(tm); if (el.isConnected && items[i] === it) { i++; show(); } };
      $('.next', fb).onclick = go; tm = setTimeout(go, ok ? 900 : 2400);
    });
  }
  start();
}

function Reveal(el, id) {
  const V = {y: ['YES', 'good'], n: ['NO', 'bad'], p: ['PARTLY', 'warn']};
  el.innerHTML = ((D.reveal || {})[id] || []).map(x => '<button class="rv" aria-expanded="false"><span class="rq" dir="auto">' + x[0] + '</span><span class="ra" dir="auto" hidden><span class="pill ' + V[x[1]][1] + '">' +
    V[x[1]][0] + '</span> ' + x[2] + ' ' + refTxt(x[3]) + '</span></button>').join('');
  $$('.rv', el).forEach(b => b.onclick = () => { const a = $('.ra', b); a.hidden = !a.hidden; b.setAttribute('aria-expanded', String(!a.hidden)); });
}

// <figure data-steps> with <ol class="caps" hidden><li>caption</li>…</ol>; inside it data-s="1 3" = lit at steps 1 and 3 (dim otherwise), data-from="3" = hidden until step 3
function Steps(fig) {
  const caps = $$('.caps > li', fig).map(li => li.innerHTML), n = caps.length; let k = 1; if (!n) return;
  fig.insertAdjacentHTML('beforeend', '<div class="stepbar"><button class="back">Back</button><span class="cap" aria-live="polite"></span><button class="fwd">Next</button></div>');
  const nums = s => s.split(/\s+/).flatMap(x => { const m = x.match(/^(\d+)-(\d+)$/); return m ? Array.from({length: m[2] - m[1] + 1}, (_, j) => +m[1] + j) : [+x]; });
  const draw = () => {
    $$('[data-s]', fig).forEach(e => { const on = nums(e.dataset.s).includes(k); e.classList.toggle('lit', on); e.classList.toggle('dim', !on); });
    $$('[data-from]', fig).forEach(e => { const f = +e.dataset.from; e.style.visibility = k < f ? 'hidden' : ''; e.classList.toggle('lit', k === f); });
    $('.cap', fig).innerHTML = '<b>Step ' + k + ' of ' + n + '.</b> ' + caps[k - 1];
    $('.back', fig).disabled = k === 1; $('.fwd', fig).disabled = k === n;
  };
  $('.back', fig).onclick = () => { k--; draw(); }; $('.fwd', fig).onclick = () => { k++; draw(); }; draw();
}

function Deck(el) {
  const DAYS = [0, 1, 3, 7, 14]; let topic = 'all', queue = [], reverse = false;
  el.innerHTML = '<div class="deckbar"><select aria-label="Topic"><option value="all">All topics</option>' + D.topics.map(t => '<option value="' + t.key + '">' + esc(strip(t.title)) + '</option>').join('') +
    '</select><button class="all">Study all</button><button class="shuf">Shuffle</button><label><input type="checkbox" class="rev"> Answer side first</label></div><div class="fcwrap"></div>';
  const mine = c => topic === 'all' || c.t === topic;
  const build = all => { queue = shuffle(CARDS.filter(c => mine(c) && (all || due(c)))); show(); };
  function show() {
    const w = $('.fcwrap', el), later = CARDS.filter(c => mine(c) && !due(c)).length;
    if (!queue.length) { w.innerHTML = '<p class="muted">No cards due' + (later ? '; ' + later + ' come back later' : '') + '. Study all goes through every card.</p>'; return; }
    const c = queue[0], front = reverse ? c.b : c.f, back = (reverse ? c.f : c.b) + ' ' + refTxt(c.ref); let flipped = false;
    w.innerHTML = '<p class="muted">' + queue.length + ' left' + (later ? ' · ' + later + ' due later' : '') + '</p><button class="fc"><span class="tag">' + TITLE[c.t] + '</span><span class="face" dir="auto">' + front +
      '</span><span class="muted hint">Tap or press Space to flip</span></button><div class="rate" hidden><button data-rate="1">Again</button><button data-rate="2">Got it</button></div>';
    $('.fc', w).onclick = () => { flipped = !flipped; $('.face', w).innerHTML = flipped ? '<small class="muted">' + front + '</small><br>' + back : front; $('.rate', w).hidden = !flipped; };
    $$('[data-rate]', w).forEach(b => b.onclick = () => {
      const ok = b.dataset.rate === '2', s = S.box[c.id] || [0, 0], box = ok ? Math.min(s[0] + 1, DAYS.length - 1) : 0;
      S.box[c.id] = [box, Date.now() + DAYS[box] * 864e5]; queue.shift(); if (!ok) queue.push(c); save(); show();
    });
  }
  $('select', el).onchange = e => { topic = e.target.value; build(false); };
  $('.all', el).onclick = () => build(true);
  $('.shuf', el).onclick = () => { queue = shuffle(queue); show(); };
  $('.rev', el).onchange = e => { reverse = e.target.checked; show(); };
  build(false);
  return {refresh: () => { if (!queue.length) build(false); }};
}

function Sheet(el) {
  el.innerHTML = D.topics.map(t => '<section class="sh"><h3>' + t.title + '</h3>' + ((D.traps || {})[t.key] || []).map(x => '<p class="trap" dir="auto">' + x + '</p>').join('') +
    '<dl>' + CARDS.filter(c => c.t === t.key).map(c => '<dt dir="auto">' + c.f + '</dt><dd dir="auto">' + c.b + ' ' + refTxt(c.ref) + '</dd>').join('') + '</dl></section>').join('');
}

function renderPips() {
  const box = $('#pips'); if (!box) return;
  const pip = (label, v, name) => '<span class="pip' + (v == null ? '' : v >= 90 ? ' p4' : v >= 70 ? ' p3' : v >= 40 ? ' p2' : ' p1') + '" title="' + esc(strip(name)) + ': ' + (v == null ? 'not tried' : v + '%') + '">' + label + '</span>';
  box.innerHTML = D.topics.map((t, n) => pip(n + 1, S.best[t.key], t.title)).join('') + pip('F', S.best.final, 'Final') +
    '<span class="muted">' + Object.keys(S.miss).length + ' mistakes · ' + CARDS.filter(due).length + ' cards due</span>';
}

const W = {}, views = $$('section.view');
function route() {
  const v = views.find(x => x.id === location.hash.slice(1)) || views[0];
  views.forEach(x => { x.hidden = x !== v; });
  $$('nav a').forEach(a => { if (a.getAttribute('href') === '#' + v.id) { a.setAttribute('aria-current', 'page'); a.scrollIntoView({block: 'nearest', inline: 'center'}); } else a.removeAttribute('aria-current'); });
  if (v.id === 'mistakes' && W.mistakes) W.mistakes.start();
  if (v.id === 'cards' && W.deck) W.deck.refresh();
  window.scrollTo(0, 0);
}
$$('[data-quiz]').forEach(el => { W[el.dataset.quiz] = Quiz(el, el.dataset.quiz); });
$$('[data-gen]').forEach(el => Practice(el, el.dataset.gen));
$$('[data-written]').forEach(el => Written(el, el.dataset.written));
$$('[data-game]').forEach(el => Game(el, el.dataset.game));
$$('[data-reveal]').forEach(el => Reveal(el, el.dataset.reveal));
$$('[data-steps]').forEach(Steps);
if ($('#deck')) W.deck = Deck($('#deck'));
if ($('#sheetbox')) Sheet($('#sheetbox'));
addEventListener('hashchange', route); route(); renderPips();
setInterval(() => $$('.timer').forEach(t => { const q = t.closest('[data-t0]'); if (q) t.textContent = clock(+q.dataset.t0); }), 1000);
// keys: 1-6 answer, Enter next; on the deck, Space flips, 1 Again, 2 Got it
let lastBox = null;
addEventListener('click', e => { const b = e.target.closest('[data-quiz], [data-game]'); if (b) lastBox = b; }, true);
addEventListener('keydown', e => {
  if (e.target.closest('input, textarea, select') || e.ctrlKey || e.metaKey || e.altKey) return;
  if ((e.key === 'Enter' || e.key === ' ') && e.target.closest('button, a, summary, label')) return;
  const v = $('section.view:not([hidden])'); if (!v) return;
  const n = parseInt(e.key, 10);
  if ($('#deck', v)) { if (e.key === ' ') { e.preventDefault(); const c = $('.fc', v); if (c) c.click(); } else if (n === 1 || n === 2) { const b = $('.rate:not([hidden]) [data-rate="' + n + '"]', v); if (b) b.click(); } return; }
  const box = lastBox && v.contains(lastBox) ? lastBox : $('[data-quiz]', v) || $('[data-game]', v); if (!box) return;
  if (n >= 1) { const b = $$('.opt:not(:disabled), .choice:not(:disabled)', box)[n - 1]; if (b) b.click(); }
  else if (e.key === 'Enter') { const b = $('.next', box); if (b) { e.preventDefault(); b.click(); } }
});
}
```

```css file=engine.css
/* engine parts: restyle to fit the lab, keep the class names and the white-on-fixed-dark rule */
[hidden]{display:none!important}
nav a[aria-current]{background:var(--accent);border-color:var(--accent);color:var(--bg)}
button{font:inherit;min-height:44px;padding:8px 14px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer}
button:disabled{cursor:default}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.qhead{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;color:var(--muted);font-size:14px}
.prompt{font-size:18px}
.opts,.choices{display:grid;gap:8px}
.opt{display:flex;gap:10px;align-items:center;text-align:start}
.opt kbd{font:12px ui-monospace,monospace;color:var(--muted)}
.opt.ok,.choice.ok{background:var(--good-strong);border-color:var(--good-strong);color:#fff}
.opt.no,.choice.no{background:var(--bad-strong);border-color:var(--bad-strong);color:#fff}
.opt.ok kbd,.opt.no kbd{color:#fff}
.pill{display:inline-block;padding:1px 9px;border-radius:99px;color:#fff;font-size:13px;font-weight:600}
.pill.good{background:var(--good-strong)}.pill.bad{background:var(--bad-strong)}.pill.warn{background:var(--warn-strong)}
.ref,.muted,.tag{color:var(--muted)}.ref{font-size:13px;white-space:nowrap}.tag{font-size:13px}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
input.ans,textarea,select{font:inherit;font-size:16px;min-height:44px;padding:8px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink)}
input.ans{width:9em}textarea{width:100%}
.score{font-size:22px;margin:8px 0}.work,.missed,.marks{padding-inline-start:1.2em}
.pt{display:flex;gap:8px;align-items:flex-start;margin:6px 0}
.model{border-inline-start:3px solid var(--accent);padding-inline-start:10px}
.needs-claude{display:none}.has-claude .needs-claude{display:inline-flex}
.marks .hit{color:var(--good-strong)}.marks .gap{color:var(--bad-strong)}
.rv{display:grid;gap:6px;width:100%;text-align:start;margin:6px 0}
[data-steps] .dim{opacity:.25}
.stepbar{display:flex;gap:10px;align-items:center;margin-top:8px}.cap{flex:1}
.deckbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.fc{display:grid;gap:10px;width:100%;min-height:200px;place-content:center;text-align:center;font-size:20px}
.hint{font-size:13px}.rate{display:flex;gap:8px;margin-top:8px}.rate button{flex:1}
.trap{border-inline-start:4px solid var(--warn-strong);padding-inline-start:10px}
.flag{border:1px dashed var(--warn-strong);border-radius:10px;padding:8px 12px}
.sh dt{font-weight:600;margin-top:10px}.sh dd{margin:0}
.pip{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;border:1px solid var(--line);font-size:12px;margin-inline-end:4px}
.p1{background:var(--bad-strong);color:#fff}.p2{background:var(--warn-strong);color:#fff}.p3,.p4{background:var(--good-strong);color:#fff}.p4{box-shadow:0 0 0 2px var(--good-strong)}
mark{background:var(--hl);color:inherit}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
```

```python file=check_lab.py
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
```
