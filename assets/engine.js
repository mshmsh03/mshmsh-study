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
