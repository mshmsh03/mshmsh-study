#!/usr/bin/env python3
"""Tests for mshmsh-study. Run from anywhere: python3 tests/run.py

1. Copies engine.js, engine.css and check_lab.py out of SKILL.md with the skill's own command.
2. Builds the sample lab the way the skill says, with the skill's own fill-in command.
3. check_lab.py must pass the sample lab, browser check included.
4. flow_test.py clicks through every part of the built lab.
5. check_lab.py must catch every mistake planted in tests/bad.
"""
import pathlib, re, shutil, subprocess, sys

root = pathlib.Path(__file__).resolve().parent.parent
out = root / "tests" / "out"
shutil.rmtree(out, ignore_errors=True)
out.mkdir(parents=True)
skill = (root / "SKILL.md").read_text(encoding="utf-8")
extract, inline = re.findall(r"```bash\n(.*?)```", skill, re.S)[:2]
fails = []


def run(*cmd):
    return subprocess.run([sys.executable, *cmd], cwd=out, capture_output=True, text=True)


def step(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)
        print(detail.strip()[-3000:])


copy_code = re.search(r"<<'EOF'\n(.*?)\nEOF", extract, re.S).group(1)
r = run("-c", copy_code, str(root / "SKILL.md"))
made = all((out / f).exists() for f in ("engine.js", "engine.css", "check_lab.py"))
step("the skill's copy command writes engine.js, engine.css and check_lab.py", r.returncode == 0 and made, r.stderr)

shutil.copy(root / "tests" / "sample" / "lab.html", out / "index.html")
r = run("-c", re.search(r'python3 -c "(.*)"', inline).group(1))
page = (out / "index.html").read_text(encoding="utf-8")
step("the skill's fill-in command puts the engine into the page", r.returncode == 0 and "/*ENGINE" not in page and "function Quiz" in page, r.stderr)

r = run("check_lab.py", "index.html", "--browser")
step("check_lab.py passes the sample lab, browser check included",
     r.returncode == 0 and "ERROR" not in r.stdout and "skipped" not in r.stdout, r.stdout + r.stderr)

r = run(str(root / "tests" / "flow_test.py"), "index.html")
n = sum(line.startswith("ok") for line in r.stdout.splitlines())
step(f"{n} feature checks pass", r.returncode == 0 and n >= 31, r.stdout + r.stderr)

shutil.copy(root / "tests" / "bad" / "index.html", out / "bad.html")
shutil.copy(root / "tests" / "bad" / "answers.json", out / "answers.json")
r = run("check_lab.py", "bad.html", "--compare", "answers.json", "--browser")
planted = ["raw <div>", "duplicate options", "answer index 5", "ref '22' is outside", "bad ref 'p5'",
           "duplicate front", "with a known topic", "[2+ key points]", "is not one of the choices",
           "'y'|'n'|'p'", 'generator: t2 "bad"', "blind check t1#3", "JS error: undefinedFunctionCall",
           "#final is empty", "overlapping labels", "clipped label", "wider than the screen",
           "pages [2, 7, 8, 9, 10]"]
missed = [p for p in planted if p not in r.stdout]
step(f"check_lab.py catches all {len(planted)} planted mistakes", r.returncode == 1 and not missed,
     f"missed: {missed}\n{r.stdout}{r.stderr}")

print("\nall passed" if not fails else f"\n{len(fails)} failed")
sys.exit(1 if fails else 0)
