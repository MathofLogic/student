# The Math of Logic — Student Edition

**Every claim in the student workbook, checked by code you can run.**

```bash
git clone https://github.com/mathoflogic/student
cd student
python tests/run.py
```

No installation. No dependencies. Python 3.8+ and nothing else — because a
book about checking things for yourself should not open with *"first,
install these seven packages."*

---

## What this is

The workbook teaches one idea: **a logic is a machine with three knobs, and
every famous logic is a setting of them.**

```
V      the value space   — what values are allowed
G      the operations    — how you combine them (NOT, AND, OR)
theta  the threshold     — which values count as "yes"
```

This repo is that machine — **344 lines of executable code**, plus 322 lines
of docstrings explaining why each choice was made, plus a test for every
chalkboard the book prints. The docstring ratio is deliberate: in a project
about not mistaking your map for the territory, the reasoning behind a
choice is not decoration.

| logic | V | AND | designated | who and why |
|---|---|---|---|---|
| Classical | `{0,1}` | `min` | `{1}` | Boole 1854 — reasoning as algebra |
| Kleene K3 | `{0,½,1}` | `min` | `{1}` | Kleene 1938–52 — "computation hasn't returned" |
| Łukasiewicz Ł3 | `{0,½,1}` | `max(0,a+b−1)` | `{1}` | Łukasiewicz 1918–20 — room for an open future |
| Priest LP | `{0,½,1}` | `min` | `{½,1}` | Priest 1979 — contradictions you can use |

Read down the columns. K3 changes **V**. Ł3 changes **G**. LP changes
**only theta** — same values, same operations — and that one move turns
"excluded middle fails" into "contradictions are usable."

```python
from mol import build

build("lp").report()
# Priest LP
#   V = {0, 1/2, 1}
#   designated = {1/2, 1}
#   closure : CLOSED
#   LNC     : FAILS      <- contradictions are assertible
#   LEM     : holds
#   MP      : FAILS      <- and that is the bill LP pays
#   liar    : resolves at [1/2]
```

## The modal ladder, derived from the pattern

`mol/modal.py` builds K → T → S4 → S5 from **one** fact about the seed
pattern: how far a propagation's influence **reaches**.

```
eddies                    ->  worlds
"i reaches j"             ->  accessibility relation R
coheres in EVERY reached  ->  NECESSARY  (box)
coheres in SOME reached   ->  POSSIBLE   (diamond)
```

Then each rung is a physical fact about reach, and each fact buys exactly
one axiom:

| system | fact about reach | buys |
|---|---|---|
| K | reach is whatever it is | `box(p→q) → (box p → box q)` |
| T | every eddy reaches itself | `box p → p` |
| S4 | reach chains through | `box p → box box p` |
| S5 | reach is mutual | `dia p → box dia p` |

**The honest half.** For each rung we check *two* things: the constraint
**forces** the axiom, **and** the axiom **fails without** the constraint —
by enumerating all 512 relations on three eddies and exhibiting the
countermodel. The first check alone shows only compatibility. The second
shows the constraint is doing the work.

`modal.py` is allowed to import **only** `seed.py`, and
`test_modal_provenance` fails the build if that rule is ever broken. A
derivation you cannot fail is a decoration.

As an external check, the enumeration independently reproduces standard
correspondence theory — reflexive↔T, transitive↔4, symmetric↔B,
euclidean↔5 — which was established long before this repo existed.

## Demos

Runnable, editable, each tied to a chapter:

```bash
python demos/01_build_a_carrier.py    # Ch 1 — the first knob
python demos/02_audit_the_trap.py     # Ch 3 — the pretty machine that leaks
python demos/03_four_logics.py        # Ch 8 — one machine, four masks
python demos/04_liar_hunt.py          # Ch 7 — where the Liar can live
python demos/05_modal_ladder.py       # the modal derivation, narrated
python demos/06_your_own_logic.py     # the final challenge — a template to edit
```

`06_your_own_logic.py` is meant to be **edited**. Break it. Watch the audit
catch you.

## The repo grades itself

`tests/run.py` ends by computing its own verdict from the claims ledger in
`mol/manifest.py`, using the weakest-link principle:

```
 Claims in ledger : 33
 By tier          : FORCED=24  ANALOGY=2  STIPULATED=7
 Backed by a test : 24
 Weakest link     : STIPULATED
 REPO VERDICT     : PASS / STIPULATED
```

It cannot honestly grade higher, and it says why: reading reach as
accessibility is a **choice**, the tier order is a **choice**, and encoding
values as numbers is a **choice**. A repo that graded itself `FORCED` would
be lying — and you own the code that would catch it.

## The rule the whole project runs on

> A formal system is a **map**. Building one is map-making — choosing what
> to represent, what to ignore, and what the representation costs. Maps are
> tools. The moment a map demands belief instead of testing, it has stopped
> being a tool and started being a dogma, and you should put it down.
>
> **Including this one.**

Two design decisions, named out loud because the book says to name them:

1. **Exact `Fraction` arithmetic, never floats.** `0.1 + 0.2 != 0.3` in
   floating point, and a logic library that fails its own equality checks
   would be a bad joke. Costs speed, buys exactness.
2. **Law checks have two readings** (`value` and `designation`) and they
   **disagree** in K3. We implement both and surface the disagreement
   instead of quietly picking a side. See `docs/STAMPS.md`.

## Layout

```
mol/
  carrier.py    the three knobs, closure audit, law checks
  logics.py     classical / K3 / Ł3 / LP + the deliberately broken one
  seed.py       the pattern — propagation, load, gradient, drag, boundary
  modal.py      K→T→S4→S5 derived from reach (imports only seed)
  manifest.py   the claims ledger and weakest-link verdict
tests/
  run.py            THE GATE — run this
  test_workbook.py  every chalkboard stamp
  test_modal.py     the modal derivation, both directions
  test_seed.py      the mechanism and its anti-reification commitments
demos/            six runnable, editable teaching scripts
docs/
  STAMPS.md     chalkboard -> test index
  ROADMAP.md    what comes next (advanced, coding — all free)
```

## Coming next

Advanced and coding courses, same standard, same licence, all free. See
[`docs/ROADMAP.md`](docs/ROADMAP.md).

## Licence

MIT. Use it, fork it, teach with it, sell a course built on it. See
[`LICENSE`](LICENSE).

The workbook PDF that accompanies this repo is released separately by the
author.

## Contributing

The best contribution is a **failing test**. If a chalkboard is wrong, the
test that proves it is worth more than a polite issue. See
[`CONTRIBUTING.md`](CONTRIBUTING.md).

> The framework does not need defenders. It needs users, auditors, and the
> occasional cheerful demolition.
