# The stamp map

Every chalkboard in the Student Edition carries a stamp like
`[FORCED — verified: test_3_2]`. This file is the index: stamp → what it
claims → where it runs.

The contract: **if you cannot run the check, the book has not earned your
belief.** It cuts both ways — these same checks are how you catch *our*
mistakes. They exist. They always exist.

Run everything:

```bash
python tests/run.py
```

Run one stamp:

```bash
python -c "import sys; sys.path[:0]=['.','tests']; import test_workbook as t; t.test_3_2(); print('test_3_2 PASSED')"
```

---

## Chapter 1 — What Can Something Even Be?

| Stamp | Claim on the board | File |
|---|---|---|
| `test_1_1` | On `{0,1/2,1}` the rule "counts if v > 0" designates exactly `{1/2, 1}` | `tests/test_workbook.py` |
| `test_1_2` | A carrier needs at least one distinction to be informative; you cannot designate a value that is not in V | `tests/test_workbook.py` |

## Chapter 2 — Three Tools for Everything

| Stamp | Claim on the board | File |
|---|---|---|
| `test_2_1` | The NOT / AND / OR tables on `{0,1}` are as printed | `tests/test_workbook.py` |
| `test_2_2` | min-AND and product-AND **agree** on `{0,1}` and **split** on `{0,1/2,1}` (1/2 vs 1/4) | `tests/test_workbook.py` |
| `test_2_3` | Implication is definable from the three: `A→B := OR(NOT A, B)` | `tests/test_workbook.py` |

## Chapter 3 — Laws That Can't Break

| Stamp | Claim on the board | File |
|---|---|---|
| `test_3_0` | **The trap.** product-AND on `{0,1/2,1}` leaks `1/4` and fails the closure audit | `tests/test_workbook.py` |
| `test_3_1` | **The repair.** Swapping AND to `min` seals the machine — this is Kleene's K3 | `tests/test_workbook.py` |
| `test_3_2` | LNC forced on `{0,1}`, not forced on `{0,1/2,1}` | `tests/test_workbook.py` |
| `test_3_3` | LEM forced on `{0,1}`, not forced on `{0,1/2,1}` | `tests/test_workbook.py` |
| `test_3_4` | Double Negation survives every carrier while `NOT = 1−v` | `tests/test_workbook.py` |

> **Reading note, and it matters.** `test_3_2` and `test_3_3` use the
> **value reading** of the laws — "`AND(v, NOT v)` equals the bottom of V" —
> because that is what the Student Edition prints on the board.
>
> There is a second, equally standard **designation reading**: "`AND(v, NOT v)`
> is never *designated*." The two **disagree** in K3: `AND(1/2,1/2) = 1/2`,
> which is not the bottom (value reading fails) but is also not designated
> (designation reading holds).
>
> `test_3_2` asserts **both**, so the disagreement is on the record rather
> than hidden. Any book that reports one reading without saying which has
> quietly picked a side for you. `Carrier.lnc(reading=...)` lets you pick
> yours.

## Chapter 4 — The Three Knobs

| Stamp | Claim on the board | File |
|---|---|---|
| `test_4_1` | Classical and K3 differ in **V alone** — G and theta verified identical cell by cell | `tests/test_workbook.py` |

## Chapter 5 — Everything Costs Something

| Stamp | Claim on the board | File |
|---|---|---|
| `test_5_1` | The receipt: you gain a self-opposite value, you pay excluded middle. Both halves computed | `tests/test_workbook.py` |

## Chapter 6 — A Third Option: Maybe

| Stamp | Claim on the board | File |
|---|---|---|
| `test_6_1` | Łukasiewicz's strong AND gives `AND(1/2,1/2) = 0`, and that stinginess keeps LEM **and** LNC | `tests/test_workbook.py` |
| `test_6_2` | Ł3 and K3 differ in **exactly one AND cell** — found by scanning all nine | `tests/test_workbook.py` |

## Chapter 7 — When Systems Break

| Stamp | Claim on the board | File |
|---|---|---|
| `test_7_1` | The Liar has **no** fixed point in `{0,1}` and **exactly one** in `{0,1/2,1}` | `tests/test_workbook.py` |
| `test_7_2` | LP is K3 with **only theta moved**; LEM holds, LNC fails, modus ponens is the bill | `tests/test_workbook.py` |
| `test_7_3` | LP **blocks explosion**, with the countermodel exhibited | `tests/test_workbook.py` |

## Chapter 8 — One Machine, Many Masks

| Stamp | Claim on the board | File |
|---|---|---|
| `test_8_1` | All four logics are settings of the same three knobs, with the distinguishing knob identified for each pair | `tests/test_workbook.py` |

---

## The modal derivation

Not stamped in the Student Edition (the modals are the next course), but
included here in full because the derivation from the pattern is the thing
this project is actually about.

| Stamp | Claim | File |
|---|---|---|
| `test_modal_provenance` | `modal.py` imports **only** the seed — no logic library smuggled in | `tests/test_modal.py` |
| `test_modal_frames_enumerated` | All 512 relations on 3 eddies, not a sample | `tests/test_modal.py` |
| `test_modal_K` | K holds on **every** frame — no constraint needed | `tests/test_modal.py` |
| `test_modal_T` | Reflexive reach forces T, **and T fails without it** | `tests/test_modal.py` |
| `test_modal_4` | Transitive reach forces 4; S4 does **not** already give 5 | `tests/test_modal.py` |
| `test_modal_5` | Equivalence reach forces 5, and keeps the lower rungs | `tests/test_modal.py` |
| `test_modal_correspondence` | Reproduces textbook correspondence: refl↔T, trans↔4, symm↔B, eucl↔5 | `tests/test_modal.py` |
| `test_modal_operators_are_reach` | box/dia really are "every/some reached eddy", checked on a hand-built frame | `tests/test_modal.py` |

**The half that makes it a derivation.** For each rung we check *two*
things: the constraint **forces** the axiom, and the axiom **fails without**
the constraint. The first alone shows only compatibility. The second shows
the constraint is doing the work. A derivation you cannot fail is a
decoration.

## The seed

| Stamp | Claim | File |
|---|---|---|
| `test_seed_relative` | Load is gradient-relative — distinct histories can share a load | `tests/test_seed.py` |
| `test_seed_sameness_needs_a_gradient` | You cannot ask "same?" without saying "in which gradient" | `tests/test_seed.py` |
| `test_seed_reconfigure` | Past the boundary a pattern reconfigures rather than accreting | `tests/test_seed.py` |
| `test_seed_has_no_logic_in_it` | The seed's **executable code** contains no logic vocabulary, and does contain the mechanism | `tests/test_seed.py` |
| `test_seed_origin_is_not_an_object` | The origin is absence-of-load, not an object called zero | `tests/test_seed.py` |
