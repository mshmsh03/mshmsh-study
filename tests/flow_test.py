import json, re, sys, pathlib
from playwright.sync_api import sync_playwright
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
url = PAGE.resolve().as_uri()
D = json.loads(re.search(r'id="lab-data">(.*?)</script>', PAGE.read_text(encoding="utf-8"), re.S).group(1))
errors, fails = [], []
def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)
MOCK = """window.claude = {use: async n => n === 'sample' ? Object.assign(async () => ({text: ''}),
  {json: async (p) => { window.__prompt = p; return {covered: [1, 3], wrong: 'SJF is never preemptive', tip: 'Mention SRTF.'}; }}) : null};"""
with sync_playwright() as pw:
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={"width": 1100, "height": 900})
    ctx.add_init_script(MOCK)
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: m.type == "error" and errors.append(m.text))
    pg.goto(url + "#topic-1"); pg.wait_for_timeout(300)
    quiz = pg.locator('[data-quiz="t1"]')
    for n, q in enumerate(D["quiz"]["t1"]):
        right = q[1][q[2]]
        opts = quiz.locator(".opt")
        texts = [t.strip() for t in opts.all_inner_texts()]
        idx = [k for k, t in enumerate(texts) if t.endswith(right)][0]
        pick = idx if n else (idx + 1) % len(texts)          # miss the first question on purpose
        opts.nth(pick).click()
        fb = quiz.locator(".fb").inner_text()
        if n == 0:
            check("Not quite" in fb and quiz.locator(".opt.ok").count() == 1 and quiz.locator(".opt.no").count() == 1, "wrong answer marked, right one shown")
            check("Slide" in fb, "explanation shows the slide ref")
        quiz.locator(".next").click()
    check("5 / 6" in quiz.inner_text(), "topic score 5/6: " + quiz.locator(".score").inner_text())
    check("1 mistakes" in pg.locator("#pips").inner_text(), "pips count 1 mistake: " + pg.locator("#pips").inner_text())
    st = pg.evaluate("JSON.parse(localStorage.getItem('sx:' + JSON.parse(document.getElementById('lab-data').textContent).title))")
    check(st["best"].get("t1") == 83 and len(st["miss"]) == 1, "best 83 and one mistake stored")
    # mistakes: right twice clears it
    pg.goto(url + "#mistakes"); pg.wait_for_timeout(200)
    mq = pg.locator('[data-quiz="mistakes"]'); q0 = D["quiz"]["t1"][0]
    for rnd in range(2):
        check("Question 1 of 1" in mq.inner_text(), f"mistakes round {rnd+1} has the missed question")
        mq.locator(".opt", has_text=q0[1][q0[2]]).click(); mq.locator(".next").click()
        mq.locator(".retry").click()
    check("Nothing here yet" in mq.inner_text(), "mistake cleared after two right answers")
    # keyboard on topic 2 quiz
    pg.goto(url + "#topic-2"); pg.wait_for_timeout(200)
    pg.locator("body").click(position={"x": 5, "y": 5})
    pg.keyboard.press("1")
    q2 = pg.locator('[data-quiz="t2"]')
    check(q2.locator(".opt:disabled").count() == 4, "key 1 answers the quiz")
    pg.keyboard.press("Enter")
    check("Question 2 of 6" in q2.inner_text(), "Enter goes to the next question")
    # practice: wrong twice then reveal, then a right answer
    pr = pg.locator('[data-gen="t2"]')
    pr.locator(".ans").fill("99999"); pr.locator(".check").click()
    check("Not yet" in pr.inner_text(), "first wrong try gives a second chance")
    pr.locator(".ans").fill("88888"); pr.locator(".check").click()
    check("Not quite" in pr.inner_text() and pr.locator(".work li").count() == 2, "second wrong try shows the worked solution")
    pr.locator(".new").click()
    txt = pr.locator(".prompt").inner_text()
    b = [int(x) for x in re.search(r"bursts ([\d, ]+) ms", txt).group(1).split(", ")]
    w, t = [], 0
    for x in b: w.append(t); t += x
    pr.locator(".ans").fill(str(round(sum(w) / len(b), 2))); pr.locator(".check").click()
    check("Right" in pr.inner_text() and "Streak 1" in pr.inner_text(), "correct answer accepted: " + txt)
    # written: self-check and mocked Claude check
    wr = pg.locator('[data-written="t2"]')
    wr.locator(".show").click(); wr.locator(".pt input").nth(0).check(); wr.locator(".pt input").nth(2).check()
    check("2 of 4 key points" in wr.inner_text(), "self-check tally")
    check(wr.locator(".ask").is_visible(), "Check with Claude visible when sample exists")
    wr.locator("textarea").fill("FCFS runs in arrival order. SJF picks the shortest burst and is optimal for waiting time.")
    wr.locator(".ask").click(); pg.wait_for_timeout(200)
    check(wr.locator(".marks .hit").count() == 2 and wr.locator(".marks .gap").count() == 2 and "SRTF" in wr.inner_text(), "Claude result rendered")
    check("Key points" in pg.evaluate("window.__prompt"), "prompt carries the key points")
    # steps
    fig = pg.locator("figure[data-steps]")
    check(pg.evaluate("getComputedStyle(document.querySelector('[data-from=\"3\"]')).visibility") == "hidden", "step 1 hides P3")
    fig.locator(".fwd").click(); fig.locator(".fwd").click()
    check("Step 3 of 3" in fig.inner_text() and fig.locator(".fwd").is_disabled(), "steps reach the end")
    # game + reveal
    pg.goto(url + "#topic-1"); pg.wait_for_timeout(200)
    gm = pg.locator('[data-game="g1"]')
    for _ in range(5):
        gm.locator(".choice").first.click(); gm.locator(".next").click()
    check("sorted right" in gm.inner_text(), "game finishes: " + gm.locator(".score").inner_text())
    rv = pg.locator(".rv").first; rv.click()
    check(rv.locator(".ra").is_visible() and "YES" in rv.inner_text(), "reveal card opens with verdict")
    # flashcards
    pg.goto(url + "#cards"); pg.wait_for_timeout(200)
    deck = pg.locator("#deck")
    check("18 left" in deck.inner_text(), "deck starts with 18 due")
    pg.locator("body").click(position={"x": 5, "y": 5})
    pg.keyboard.press(" "); check(deck.locator(".rate").is_visible(), "Space flips the card")
    pg.keyboard.press("2"); check("17 left" in deck.inner_text(), "Got it removes the card")
    pg.keyboard.press(" "); pg.keyboard.press("1"); check("17 left" in deck.inner_text(), "Again keeps it in the deck")
    deck.locator("select").select_option("t2"); line = deck.locator("p.muted").first.inner_text()
    check(line in ("9 left", "8 left · 1 due later"), "topic filter: " + line)
    # final
    pg.goto(url + "#final"); pg.wait_for_timeout(200)
    fq = pg.locator('[data-quiz="final"]'); fq.locator(".begin").click()
    gens = 0
    for _ in range(10):
        if fq.locator(".ans").count():
            gens += 1; fq.locator(".ans").fill("1"); fq.locator(".check").click()
        else:
            fq.locator(".opt").first.click()
        fq.locator(".next").click()
    check(re.search(r"\d+ / 10", fq.inner_text()) is not None and " in " in fq.locator(".score").inner_text(), "final ends with score and time: " + fq.locator(".score").inner_text())
    check(gens == 1, f"final includes {gens} generated problem")
    # sheet
    pg.goto(url + "#sheet"); pg.wait_for_timeout(200)
    check(pg.locator("#sheetbox dt").count() == 18 and pg.locator("#sheetbox .trap").count() == 3, "sheet lists all cards and traps")
    # without the mock: no Claude button, no errors
    pg2 = br.new_page(); pg2.on("pageerror", lambda e: errors.append("no-mock: " + str(e)))
    pg2.goto(url + "#topic-2"); pg2.wait_for_timeout(300)
    check(not pg2.locator(".ask").first.is_visible(), "Check with Claude hidden without the capability")
    br.close()
check(not errors, "no JS errors " + str(errors[:3]))
sys.exit(1 if fails else 0)
