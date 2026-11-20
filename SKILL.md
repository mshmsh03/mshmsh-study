---
name: "mshmsh-study"
description: "Turns lectures, slides or notes into a published study lab with diagrams, quizzes, practice problems, flashcards, a mistakes deck and a timed final, every fact tied to its slide. Use for quiz, midterm or final prep, 'make this fun to study', or when someone says mshmsh-study (or its old name, study-xoshaka)."
---

# mshmsh-study: interactive study labs

You turn course material into one published HTML study page, a "lab". The student opens it the night before a quiz or exam, so it has to be right, cover every slide, show where each fact comes from, and work on a phone.

You write the content as one JSON block, the topic visuals as HTML and SVG, and any problem generators. The engine (`assets/engine.js`), its stylesheet (`assets/engine.css`) and the checker (`scripts/check_lab.py`) do the rest. They are tested, so copy them instead of writing your own.

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

Work in `<course>-ch<N>/`. Copy the engine, its stylesheet and the checker from the skill's folder instead of retyping them. Don't rewrite them. If a lab needs something new, add it in your copy. The skill's base directory is printed when the skill loads.

```bash
cp "<skill base dir>/assets/engine.js" "<skill base dir>/assets/engine.css" "<skill base dir>/scripts/check_lab.py" .
```

If those files aren't there, the skill was installed without its folder. Tell the student to install it again rather than writing the engine yourself.

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
