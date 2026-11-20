# mshmsh-study

A Claude skill that turns lectures, slides and notes into one interactive study page, a "lab", for the night before a quiz or exam. Every question and flashcard shows the slide it came from, so you can check anything against the lecture.

A lab has:

- **A tab per topic.** A visual that fits the content (a matrix, a diagram, a timeline, a step-by-step trace), the traps that are easy to mix up, and practice that fits your exam: a quiz, written answers with key points and a model answer, and calculation problems with new numbers every time.
- **Flashcards.** A card you know comes back after 1, 3, 7 and then 14 days.
- **Mistakes.** Every question you miss comes back until you get it right twice in a row.
- **Sheet.** Every card and trap on one page, for the last 15 minutes.
- **Final.** 20 questions from all topics, weighted toward your weak ones, with a timer.

It reads PDFs, PowerPoint files with their speaker notes, photos of slides or notes, and YouTube transcripts. It asks how your exam works, and it copies your lecturer's style when you share past papers. Kurdish and Arabic text runs right to left.

## Install

**Claude app:** download [mshmsh-study.zip](https://github.com/mshmsh03/mshmsh-study/releases/download/latest/mshmsh-study.zip) and upload it in your skill settings. To update, upload the new zip in place of the old one.

**Claude Code:**

```bash
npx skills add mshmsh03/mshmsh-study
```

Then type `/mshmsh-study`, or ask Claude to turn a lecture into a study page.

**Renamed:** this skill was called `study-xoshaka` until 2026-11-20. If you have the old one, remove it after installing this one so the two don't both load. In the Claude app, delete study-xoshaka. In Claude Code, run `npx skills remove study-xoshaka -g`.

## How it works

1. **Read everything** and index the slides. A slide it can't read gets a flag on the page, never a guess.
2. **Outline 5 to 8 topics** in the lecture's order: definitions, counts, names and dates, formulas, traps, and what the lecturer stressed.
3. **Pick a visual** for each topic from the shape of its content.
4. **Write the practice.** Questions have one defensible answer and real distractors, each flashcard holds one fact, and problem generators use the lecture's method and rounding.
5. **Build one HTML page.** The engine, its stylesheet and the checker live inside SKILL.md and get copied out, so every lab runs the same tested code.
6. **Check it.** `check_lab.py` checks the data, slide coverage, answer keys and generators, then clicks through the page at phone and desktop width looking for errors and overlapping labels. A fresh agent then answers the quiz blind from the lecture, and every disagreement with the key gets fixed.
7. **Publish** it as a page you can open on your phone.

## What you need

Claude has all of this in its own workspace. To build labs elsewhere you need Python 3 and Node.js, plus Playwright with Chromium for the browser check. Reading slides uses `pdftoppm`, LibreOffice and `markitdown` when they're installed.

## What is in this folder

| Path | What it is |
| --- | --- |
| `SKILL.md` | The workflow, plus `engine.js` (quiz, flashcards, mistakes, final), `engine.css` and `check_lab.py`, which Claude copies out of it |
| `tests/run.py` | Runs all the tests |
| `tests/sample/lab.html` | A sample lab (Operating Systems, CPU scheduling) written the way the skill says |
| `tests/flow_test.py` | Clicks through every part of a built lab |
| `tests/bad/` | A page full of planted mistakes the checker has to catch |

## Tested

`python3 tests/run.py` copies the engine out of SKILL.md with the skill's own command, builds the sample lab, then checks that:

- `check_lab.py` passes it, browser check included
- 31 feature checks pass: quiz scoring, mistakes clearing after two right answers, keys 1 to 6 and Enter, practice problems with two tries, written answers with and without Check with Claude, steps, the game, reveal cards, flashcards with spaced repetition, the final and the sheet
- `check_lab.py` catches all 18 mistakes planted in `tests/bad`

GitHub runs the tests on every push.

## Ideas from

- [Microsoft study-flashcards](https://github.com/microsoft/cat-agent-skills): a slide reference on every item, and following the source when it disagrees with common knowledge
- [Anthropic law-student flashcards](https://github.com/anthropics/claude-for-legal): one fact per card, and fewer cards rather than wrong ones
- [mattpocock/teach](https://github.com/mattpocock/skills): options of equal length, and learning by recalling and spacing out review
- [roundtable02/tutor](https://github.com/roundtable02/tutor-skills): no hints hidden in the options
- [examprep-ai](https://github.com/sickn33/agentic-awesome-skills): calculation and written practice, and past papers
- [Learn Anything](https://github.com/makeit-run/learn-anything): a fixed, tested engine where Claude only writes the content

## Licence

MIT. See [LICENSE](LICENSE).
