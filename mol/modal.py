"""
modal.py — the modal ladder K -> T -> S4 -> S5, derived from the seed.

HOUSE RULE FOR THIS FILE: it may import only `seed`. No logic-specific
primitive may be added by hand. If the modal family needs machinery the
seed does not have, the derivation has failed and `tests/test_modal.py`
reports it. A derivation you cannot fail is decoration, not derivation.

THE DERIVATION
--------------
The seed gives us propagations whose drag REACHES some regions of a context
and not others. Call the regions `eddies`. "Eddy i reaches eddy j" means a
pattern in i drags j. That reach relation, with nothing added, is a frame:

    eddies                          -> worlds
    "i reaches j"                   -> accessibility relation R
    coheres in EVERY reached eddy   -> NECESSARY   (box)
    coheres in SOME reached eddy    -> POSSIBLE    (diamond)

Then the ladder is a sequence of physical facts about how reach behaves.
Each fact is a constraint on R, and each constraint BUYS exactly one axiom:

    K   reach is whatever it is.        no constraint    -> K axiom (free)
    T   every eddy reaches itself       reflexive        -> box p -> p
    S4  reach chains through            + transitive     -> box p -> box box p
    S5  reach is mutual                 + symmetric      -> dia p -> box dia p

RIGOR SPLIT, stated plainly (workbook labelling discipline):

    STIPULATED : the reading "R = reach". That is an interpretation of the
                 seed. It could be read otherwise; we say so rather than
                 smuggling it in as discovery.
    FORCED     : everything after the reading. Each correspondence below is
                 checked by complete enumeration over EVERY relation on
                 n <= 3 eddies, in both directions:
                   (a) the constraint forces the axiom, AND
                   (b) the axiom FAILS on some frame without the constraint.
                 (b) is the honest half. Without it you have only shown the
                 constraint is compatible with the axiom, not that it is
                 doing the work.
"""

from itertools import product

__all__ = [
    "all_frames", "reflexive", "transitive", "symmetric", "euclidean",
    "equivalence", "no_constraint", "box", "dia",
    "AXIOMS", "CONSTRAINTS", "LADDER",
    "forces", "derive_ladder", "countermodel_for",
]


# --- frames: every possible way reach can be arranged ---------------------

def all_frames(n):
    """Every reach relation on n eddies. There are 2^(n*n) of them."""
    pairs = [(i, j) for i in range(n) for j in range(n)]
    for bits in product((0, 1), repeat=len(pairs)):
        yield frozenset(p for p, b in zip(pairs, bits) if b)


# --- constraints: physical facts about how reach behaves ------------------

def no_constraint(R, n):
    """K: reach is whatever it is."""
    return True


def reflexive(R, n):
    """T: every eddy reaches itself — a pattern always perturbs its own region."""
    return all((i, i) in R for i in range(n))


def transitive(R, n):
    """S4: reach chains — a through-current means i reaches k if i->j->k."""
    return all((i, k) in R
               for i in range(n) for j in range(n) for k in range(n)
               if (i, j) in R and (j, k) in R)


def symmetric(R, n):
    """S5: reach is mutual — a counter-current means j reaches i if i reaches j."""
    return all((j, i) in R for (i, j) in R)


def euclidean(R, n):
    """If i reaches both j and k, then j reaches k."""
    return all((j, k) in R
               for i in range(n) for j in range(n) for k in range(n)
               if (i, j) in R and (i, k) in R)


def equivalence(R, n):
    """Reflexive + transitive + symmetric. The S5 frame."""
    return reflexive(R, n) and transitive(R, n) and symmetric(R, n)


def preorder(R, n):
    """Reflexive + transitive. The S4 frame."""
    return reflexive(R, n) and transitive(R, n)


# --- the two operators, straight off the seed's reach ---------------------

def box(V, R, i):
    """NECESSARY at eddy i: coheres in every eddy that i reaches."""
    return all(V[j] for j in range(len(V)) if (i, j) in R)


def dia(V, R, i):
    """POSSIBLE at eddy i: coheres in some eddy that i reaches."""
    return any(V[j] for j in range(len(V)) if (i, j) in R)


# --- the axioms, as checks over every coherence assignment ----------------
# A "coherence assignment" V is a tuple of booleans: does the pattern
# cohere in each eddy? We check the axiom at every eddy, for every possible
# assignment. That is complete enumeration — the workbook's proof technique.

def ax_K(R, n):
    """K: box(p -> q) -> (box p -> box q). Necessity respects implication.
    Needs TWO propositions, so we enumerate both."""
    for Vp in product((True, False), repeat=n):
        for Vq in product((True, False), repeat=n):
            Vimp = tuple((not Vp[k]) or Vq[k] for k in range(n))
            for i in range(n):
                if box(Vimp, R, i) and box(Vp, R, i) and not box(Vq, R, i):
                    return False
    return True


def ax_T(R, n):
    """T: box p -> p. What is necessary here is actually true here."""
    for V in product((True, False), repeat=n):
        for i in range(n):
            if box(V, R, i) and not V[i]:
                return False
    return True


def ax_4(R, n):
    """4: box p -> box box p. If it is necessary, that is itself necessary."""
    for V in product((True, False), repeat=n):
        for i in range(n):
            if box(V, R, i):
                if not all(box(V, R, j) for j in range(n) if (i, j) in R):
                    return False
    return True


def ax_5(R, n):
    """5: dia p -> box dia p. If it is possible, that is necessarily so."""
    for V in product((True, False), repeat=n):
        for i in range(n):
            if dia(V, R, i):
                if not all(dia(V, R, j) for j in range(n) if (i, j) in R):
                    return False
    return True


def ax_B(R, n):
    """B: p -> box dia p. What is true is necessarily possible."""
    for V in product((True, False), repeat=n):
        for i in range(n):
            if V[i]:
                if not all(dia(V, R, j) for j in range(n) if (i, j) in R):
                    return False
    return True


AXIOMS = {
    "K": (ax_K, "box(p->q) -> (box p -> box q)"),
    "T": (ax_T, "box p -> p"),
    "4": (ax_4, "box p -> box box p"),
    "5": (ax_5, "dia p -> box dia p"),
    "B": (ax_B, "p -> box dia p"),
}

CONSTRAINTS = {
    "none": (no_constraint, "reach is whatever it is"),
    "reflexive": (reflexive, "every eddy reaches itself"),
    "transitive": (transitive, "reach chains through"),
    "symmetric": (symmetric, "reach is mutual"),
    "euclidean": (euclidean, "reach fans out consistently"),
    "preorder": (preorder, "reflexive + transitive"),
    "equivalence": (equivalence, "reflexive + transitive + symmetric"),
}

# The ladder as the workbook presents it: each rung adds one physical fact
# about reach, and collects one new axiom.
LADDER = [
    ("K",  "none",        "K", "raw reach, no constraint at all"),
    ("T",  "reflexive",   "T", "every eddy reaches itself"),
    ("S4", "preorder",    "4", "reach chains through"),
    ("S5", "equivalence", "5", "reach is mutual"),
]


# --- the honest check: forces AND fails without --------------------------

def forces(constraint, axiom, n=3):
    """Does `constraint` force `axiom` on n eddies — and does the axiom
    actually FAIL somewhere without it?

    Returns (holds_under, fails_without). Both must be True for the
    constraint to be doing real work. `fails_without` is the half that
    makes this a derivation instead of a coincidence.
    """
    frames = list(all_frames(n))
    holds_under = all(axiom(R, n) for R in frames if constraint(R, n))
    fails_without = any(not axiom(R, n) for R in frames if not constraint(R, n))
    return holds_under, fails_without


def countermodel_for(constraint, axiom, n=3):
    """Find an actual frame where the axiom fails because the constraint is
    absent. This is the witness — the thing you can point at."""
    for R in all_frames(n):
        if not constraint(R, n) and not axiom(R, n):
            return R
    return None


def derive_ladder(n=3):
    """Walk the ladder, checking each rung. Returns a list of result dicts."""
    out = []
    for system, cname, aname, story in LADDER:
        constraint = CONSTRAINTS[cname][0]
        axiom, formula = AXIOMS[aname]
        holds, fails_without = forces(constraint, axiom, n)
        cm = None if cname == "none" else countermodel_for(constraint, axiom, n)
        out.append({
            "system": system,
            "constraint": cname,
            "story": story,
            "axiom": aname,
            "formula": formula,
            "forced": holds,
            # for K there is nothing to fail without, since there is no
            # constraint — K is free on every frame. We mark that honestly
            # instead of pretending the check applies.
            "fails_without": fails_without if cname != "none" else None,
            "countermodel": cm,
        })
    return out
