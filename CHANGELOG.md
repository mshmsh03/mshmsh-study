# Changelog

## 2.1.0 (2026-11-20)

SKILL.md is two thirds smaller (55 KB down to 19 KB), so the skill uses far fewer tokens each time it runs.

- The engine, its stylesheet and the checker moved out of SKILL.md into `assets/engine.js`, `assets/engine.css` and `scripts/check_lab.py`. Claude copies them into each lab without reading them. Their code is unchanged.
- The Claude app zip now includes `assets/` and `scripts/`. Upload the new zip in place of the old one. The old one keeps working until you do.

## 2.0.0 (2026-11-20)

Rewritten after studying the best study and quiz skills, then renamed from study-xoshaka to mshmsh-study.

- Every question and flashcard shows its slide. A slide Claude can't read gets a flag on the page.
- New practice: written answers with key points and a model answer, with an optional Check with Claude, and problem generators for calculation topics.
- New tabs: Mistakes, Sheet, spaced-repetition Flashcards, and a Final weighted toward weak topics.
- Reads PowerPoint speaker notes, photos and YouTube transcripts, and copies the lecturer's style from past papers.
- The engine, its stylesheet and a checker live inside SKILL.md, so every lab runs the same tested code.
- Before publishing: `check_lab.py`, then a blind answer-key check by a fresh agent.
- Tests in `tests/`, run by GitHub on every push.

## 1.0.0

study-xoshaka: a lecture turned into an interactive study page with diagrams, mini-games, quizzes, flashcards and a final challenge. Shared with a friend as a zip on 2026-11-11.
