# Roadmap

Everything here is and stays **free**, **MIT**, and **runnable without
installing anything**. Those three constraints are not marketing — they are
design rules, and they shape what gets built.

## Shipped — `mathoflogic/student`

The Student Edition. High-school level, no maths background assumed.

- The three knobs: `V`, `G`, `theta`
- Closure auditing (the trap that reads perfectly and leaks)
- Forced vs. chosen laws — LNC, LEM, DN by complete enumeration
- The middle value, two ways: Łukasiewicz and Kleene
- The Liar, and Priest's one-knob move to LP
- The modal ladder K → T → S4 → S5, derived from the seed's reach
- 34 checks, self-grading manifest, six editable demos

## Next — `mathoflogic/advanced`

For readers who finished the student edition and want the machinery.

- **More carriers**: Belnap's FOUR (told-true × told-false), Bochvar's
  external/internal tiers, weak Kleene, fuzzy families (min/product/
  Łukasiewicz t-norms) on the continuous interval
- **Intuitionistic logic** as Knob 2 done properly — LEM not *false* but
  *unreachable*, because the parts to state it were never manufactured
- **Load and cost**: the price of a distinction, chained-AND accumulation,
  the generalised rule with shared information
- **The four failure modes** with their receipts: Liar (no fixed point),
  divergence (the Gödel silhouette, honestly labelled), Russell (level
  collapse, run on real hardware), Yablo (no seed state)
- **The full modal family**: B, GL and provability, temporal, deontic,
  epistemic — each as a constraint on reach
- **De-reified Peano**: arithmetic as what the axioms force, with the
  induction wall and the Gödel wall named rather than crossed

## Next — `mathoflogic/coding`

Logic for people who write software, taught the same way.

- Three-valued logic is already in your database: `NULL` is Kleene's middle
  value, and every `WHERE` clause you write is a designation choice
- Short-circuit evaluation is strong vs. weak Kleene, in production
- Paraconsistent handling of inconsistent data sources — keep answering
  queries instead of exploding
- Type systems as carriers; the closure audit as a linter
- Property-based testing as complete enumeration on a budget
- Building your own checked carrier for a real domain, end to end

## Standing rules for every repo in this series

1. **Runnable with zero installation.** Stdlib only in the core. If a
   course needs a dependency, it goes in an optional extra, never the path
   a beginner walks first.
2. **Every claim carries a stamp**, and every stamp resolves to a test that
   runs. A claim with no runnable check is labelled `STIPULATED` and says
   so out loud.
3. **The repo grades itself** by weakest link, and can never honestly print
   a verdict stronger than its weakest support.
4. **Exact arithmetic** where equality matters. No float comparisons in law
   checks.
5. **Derivations must be falsifiable.** If a module claims to derive
   something from a seed, a provenance test enforces what it may import,
   and the "fails without the constraint" half is checked, not assumed.
6. **MIT, forever.** Fork it, teach with it, build a paid course on top of
   it. The licence does not change.

## How to help

The most valuable contribution to any of these is a **failing test** — a
chalkboard that is wrong, a claim mis-tiered, a derivation that leaks a
primitive it should not have. See `CONTRIBUTING.md`.

The framework does not need defenders. It needs users, auditors, and the
occasional cheerful demolition.
