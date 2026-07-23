# Contributing

**The best contribution to this repo is a failing test.**

That is not a slogan. The workbook's whole contract is that its claims are
checkable and therefore falsifiable. A test that proves a chalkboard wrong
is worth more than a polite issue, and it is worth more than a feature.

## Found a mistake?

1. Write the test that fails.
2. Open a PR with it, even if you have no fix.
3. If you know the fix, include it — but the test is the valuable half.

A PR titled *"test_6_2 is wrong and here is the enumeration that shows it"*
will get merged faster than anything else in the queue.

## Before you open a PR

```bash
python tests/run.py          # must exit 0
for f in demos/*.py; do python "$f" >/dev/null || echo "BROKE: $f"; done
```

No dependencies to install. If your change adds one to `mol/`, it will be
declined — the stdlib-only rule is what makes this usable by a student on a
school laptop with no admin rights.

## House rules

**Every claim carries a tier.** If you add a claim to `mol/manifest.py`,
give it the honest tier:

| tier | means |
|---|---|
| `FORCED` | proved by complete enumeration or direct construction; cite the test |
| `EMPIRICAL` | a measured fact about the world; cite the measurement |
| `ANALOGY` | a structural correspondence, true inside a stated construction |
| `STIPULATED` | a design choice; show the alternative so it reads as a choice |
| `SPECULATION` | worth having, not asserted, never load-bearing |

If you are unsure between two tiers, **take the weaker one**. The verdict is
computed by weakest link, so over-claiming anywhere corrupts the whole
grade — which is exactly what the grade exists to prevent.

**`mol/seed.py` stays poor.** It may know about propagation, load,
gradients, venting, confluence, drag and boundaries. It may not know about
truth values, operators, designation or axioms.
`test_seed_has_no_logic_in_it` enforces this on the executable code. If you
need logic vocabulary in the seed, the design is wrong, not the test.

**`mol/modal.py` may import only `mol/seed.py`.**
`test_modal_provenance` enforces it. The moment modal reaches for a logic
library, the derivation stops being a derivation and becomes a decoration.

**Derivations need both halves.** If you add a frame condition, check that
it *forces* the axiom **and** that the axiom *fails without* it. The first
alone proves only compatibility. `mol.modal.forces()` returns both; use it.

**No floats in law checks.** Use `Fraction` via `mol.carrier.F`. A logic
library that fails its own equality checks because `0.1 + 0.2 != 0.3` would
be a bad joke.

## Style

- Plain functions and asserts in tests; they run under `python tests/run.py`
  *and* under pytest. Do not add a pytest-only feature to the core suite.
- Docstrings explain **why**, especially where a choice was made. If you
  chose something that could have gone another way, say so in the
  docstring — that is the house discipline, applied to the code.
- Comments that name a trade-off are welcome. Comments that restate the
  code are not.

## Adding a new carrier

Put it in `mol/logics.py` with:

- a docstring naming the person, the year, and **the problem they were
  actually solving**
- a `note=` giving the one-line intuition
- a test in `tests/test_workbook.py` establishing its signature by
  enumeration (which laws hold, which fail, and the witness value)
- a ledger entry in `mol/manifest.py`

Historical framing is welcome and should be accurate. If a date or
motivation is disputed among historians, say so rather than picking one
silently — the same rigor discipline applies to the history as to the maths.

## Code of conduct

Be decent. Argue with the tests, not the person. Someone finding a real bug
in this repo has done it a favour, and the correct response is thanks.
