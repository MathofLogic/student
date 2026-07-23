"""
manifest.py — the book grades itself.

The student workbook stamps every claim with a tier. This module holds the
ledger and computes the verdict by the weakest-link principle: no honest
composite verdict outranks its weakest support.

If this repo ever printed "VERDICT: FORCED" it would be lying, because the
tier order itself is a choice, the reading of reach-as-accessibility is a
choice, and the encoding of values as numbers is a choice. PASS/STIPULATED
is the correct grade, and the point of computing it in code is that you can
catch us if we ever quietly upgrade ourselves.
"""

__all__ = ["TIERS", "CLAIMS", "verdict", "summary"]

# Ordered strongest to weakest. This ORDER is itself a stipulation — we are
# the ones who decided proof beats measurement beats analogy. Say it out loud.
TIERS = ["FORCED", "EMPIRICAL", "ANALOGY", "STIPULATED", "SPECULATION"]


def _c(tier, claim, test=None, note=""):
    return {"tier": tier, "claim": claim, "test": test, "note": note}


CLAIMS = [
    # ---- Chapter 1 : carriers -------------------------------------------
    _c("STIPULATED", "Calling the value space a 'carrier set' is vocabulary",
       note="a naming choice, not a discovery"),
    _c("STIPULATED", "Encoding YELLOW as 0.5 rather than 0.8",
       note="a different map-maker draws it differently; the workbook says so"),
    _c("FORCED", "Designation rule 'v > 0' on {0,1/2,1} designates exactly {1/2,1}",
       test="test_1_1"),

    # ---- Chapter 2 : operations -----------------------------------------
    _c("FORCED", "NOT/AND/OR tables on {0,1} are as printed", test="test_2_1"),
    _c("FORCED", "min-AND and product-AND agree on {0,1} but split on {0,1/2,1}",
       test="test_2_2", note="the binary carrier HIDES the choice of G"),
    _c("FORCED", "Implication is definable from the three: A->B = OR(NOT A, B)",
       test="test_2_3"),

    # ---- Chapter 3 : forced laws ----------------------------------------
    _c("FORCED", "product-AND on {0,1/2,1} leaks 1/4 and fails the closure audit",
       test="test_3_0", note="the machine that reads perfectly and is dead on arrival"),
    _c("FORCED", "Swapping AND to min seals the machine — this is Kleene's K3",
       test="test_3_1"),
    _c("FORCED", "LNC is forced on {0,1} and not forced on {0,1/2,1} (value reading)",
       test="test_3_2"),
    _c("FORCED", "LEM is forced on {0,1} and not forced on {0,1/2,1} (value reading)",
       test="test_3_3"),
    _c("FORCED", "Double Negation survives every carrier while NOT = 1-v",
       test="test_3_4"),

    # ---- Chapter 4 : the three knobs ------------------------------------
    _c("FORCED", "Classical and K3 differ in V alone, with G and theta identical",
       test="test_4_1"),
    _c("STIPULATED", "That V, G, theta are the RIGHT three knobs to cut the space with",
       note="a productive framing; other decompositions are possible"),

    # ---- Chapter 5 : everything costs -----------------------------------
    _c("FORCED", "Adding 1/2 to the carrier costs LEM — the receipt is computable",
       test="test_5_1"),

    # ---- Chapter 6 : the middle value -----------------------------------
    _c("FORCED", "Lukasiewicz's strong AND gives AND(1/2,1/2)=0 and keeps LEM+LNC",
       test="test_6_1"),
    _c("FORCED", "L3 and K3 differ in exactly one AND cell", test="test_6_2"),
    _c("ANALOGY", "The middle value 'means' undecided (L3) or still-loading (K3)",
       note="the arithmetic is forced; what the value MEANS is interpretation"),

    # ---- Chapter 7 : paradox --------------------------------------------
    _c("FORCED", "The Liar has no fixed point in {0,1} and exactly one in {0,1/2,1}",
       test="test_7_1"),
    _c("FORCED", "LP is K3 with only theta moved; LNC and MP fail, LEM holds",
       test="test_7_2"),
    _c("FORCED", "LP blocks explosion — a countermodel is exhibited", test="test_7_3"),
    _c("ANALOGY", "Reading a paradox as 'the carrier ran out of shelves'",
       note="a good picture; it does not referee natural language"),

    # ---- Chapter 8 : one machine ----------------------------------------
    _c("FORCED", "All four logics are settings of the same three knobs",
       test="test_8_1"),

    # ---- the modal derivation -------------------------------------------
    _c("STIPULATED", "Reading the seed's reach as an accessibility relation",
       note="THE load-bearing interpretive step of the modal derivation"),
    _c("FORCED", "Reflexive reach forces T, and T fails without it", test="test_modal_T"),
    _c("FORCED", "Transitive reach forces 4, and 4 fails without it", test="test_modal_4"),
    _c("FORCED", "Equivalence reach forces 5, and 5 fails without it", test="test_modal_5"),
    _c("FORCED", "K holds on every frame with no constraint at all", test="test_modal_K"),
    _c("FORCED", "Standard correspondences reproduce: refl-T, trans-4, symm-B, eucl-5",
       test="test_modal_correspondence"),

    # ---- the seed --------------------------------------------------------
    _c("FORCED", "Load is gradient-relative: distinct histories can share a load",
       test="test_seed_relative"),
    _c("FORCED", "Past the boundary a propagation reconfigures rather than accreting",
       test="test_seed_reconfigure"),
    _c("STIPULATED", "That the seed pattern is the right mechanism to build from",
       note="it works; that is not the same as it being the only or true one"),

    # ---- the repo about itself -------------------------------------------
    _c("STIPULATED", "The tier ORDER (forced > empirical > analogy > stipulated)",
       note="we chose this ranking. It is not handed down."),
    _c("STIPULATED", "Exact Fractions rather than floats",
       note="an engineering choice; it buys exact equality and costs speed"),
]


def verdict(claims=None):
    """Weakest-link verdict over the ledger."""
    claims = CLAIMS if claims is None else claims
    worst = 0
    for c in claims:
        worst = max(worst, TIERS.index(c["tier"]))
    return TIERS[worst]


def summary(claims=None):
    """Counts per tier, plus how many claims are backed by a runnable test."""
    claims = CLAIMS if claims is None else claims
    counts = {t: 0 for t in TIERS}
    for c in claims:
        counts[c["tier"]] += 1
    backed = sum(1 for c in claims if c.get("test"))
    return {
        "total": len(claims),
        "counts": counts,
        "test_backed": backed,
        "verdict": verdict(claims),
    }


def render():
    """The manifest, as the workbook prints it."""
    s = summary()
    lines = []
    lines.append("=" * 64)
    lines.append(" THE MANIFEST — this repo grades itself")
    lines.append("=" * 64)
    tiers = "  ".join(f"{t}={s['counts'][t]}" for t in TIERS if s["counts"][t])
    lines.append(f" Claims in ledger : {s['total']}")
    lines.append(f" By tier          : {tiers}")
    lines.append(f" Backed by a test : {s['test_backed']}")
    lines.append(f" Weakest link     : {s['verdict']}")
    lines.append(f" REPO VERDICT     : PASS / {s['verdict']}")
    lines.append("")
    lines.append(" Why it cannot be higher: reading reach as accessibility is a")
    lines.append(" choice, the tier order is a choice, and the number-encoding of")
    lines.append(" values is a choice. A repo that graded itself FORCED would be")
    lines.append(" lying — and you own the code that would catch it.")
    return "\n".join(lines)
