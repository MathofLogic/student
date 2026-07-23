"""
logics.py — four famous logics, built as settings of the same three knobs.

This is the payoff of the student workbook, in code. Classical logic,
Kleene's K3, Lukasiewicz's L3 and Priest's LP were built by four people
across a century, in different countries, for completely different reasons.
They are the SAME MACHINE at four settings:

    logic       V              G (the AND)        theta (designated)
    ---------   ------------   ----------------   -------------------
    Classical   {0,1}          min                {1}
    Kleene K3   {0,1/2,1}      min                {1}
    Lukasz. L3  {0,1/2,1}      strong (a+b-1)     {1}
    Priest LP   {0,1/2,1}      min                {1/2, 1}   <-- only theta moved

Read down the columns. K3 changes V from classical. L3 changes G from K3.
LP changes ONLY theta from K3 — same values, same operations — and that
single move turns "excluded middle fails" into "contradictions are usable".

Also included: the broken machine (product-AND on three values), because
the workbook's most important lesson is that a machine can look perfect
and be dead on arrival. You audit before you admire.
"""

from fractions import Fraction
from .carrier import Carrier, F

__all__ = [
    "classical", "kleene_k3", "lukasiewicz_l3", "priest_lp",
    "product_and_trap", "ALL", "build",
]

# --- the operations ------------------------------------------------------
# NOT is the same flip everywhere in this book: NOT(v) = 1 - v.
_flip = lambda v: 1 - v

# AND, two designs. On {0,1} they are indistinguishable. On {0,1/2,1} they
# split apart — which is the workbook's proof that G is a separate choice.
_min_and = lambda a, b: min(a, b)
_product_and = lambda a, b: a * b

# Lukasiewicz's "strong" AND: the amount by which a+b beats 1, floored at 0.
# It makes truth expensive on purpose — two half-truths give a flat zero —
# and that is exactly what buys him back the classical laws.
_strong_and = lambda a, b: max(Fraction(0), a + b - 1)
_strong_or = lambda a, b: min(Fraction(1), a + b)

_max_or = lambda a, b: max(a, b)


# --- the four settings ---------------------------------------------------

def classical():
    """George Boole's world. Two values, everything forced, no middle."""
    return Carrier(
        "Classical (CL2)", [0, 1], _flip, _min_and, _max_or, [1],
        note="Boole 1854 / Shannon 1937. The tidy two-value machine.",
    )


def kleene_k3():
    """Stephen Kleene, 1938-52. The middle value means UNDEFINED —
    a computation that has not returned. It spreads like a taint."""
    return Carrier(
        "Kleene K3", [0, "1/2", 1], _flip, _min_and, _max_or, [1],
        note="middle = 'still loading'. Plain min/max lets it propagate.",
    )


def lukasiewicz_l3():
    """Jan Lukasiewicz, 1918-20. The middle value means NOT YET DECIDED —
    built to make room for an open future, and for free will."""
    return Carrier(
        "Lukasiewicz L3", [0, "1/2", 1], _flip, _strong_and, _strong_or, [1],
        note="middle = 'undecided'. Strong AND keeps LEM and LNC alive.",
    )


def priest_lp():
    """Graham Priest, 1979. K3's exact tables — only theta moved, so the
    middle value COUNTS. Contradictions become usable instead of fatal."""
    return Carrier(
        "Priest LP", [0, "1/2", 1], _flip, _min_and, _max_or, ["1/2", 1],
        note="K3's machine with the threshold lowered. Only theta changed.",
    )


def product_and_trap():
    """THE TRAP. Reads perfectly on paper. Dead on arrival.

    Multiplying truth values feels obvious, and on {0,1} it is even correct.
    Add a middle value and AND(1/2,1/2) = 1/4, which is not in V. The machine
    leaks. Nobody catches this by reading it. The audit catches it.
    """
    return Carrier(
        "product-AND trap", [0, "1/2", 1], _flip, _product_and, _max_or, [1],
        note="the machine that looks right and leaks. Audit before you admire.",
    )


ALL = {
    "classical": classical,
    "k3": kleene_k3,
    "l3": lukasiewicz_l3,
    "lp": priest_lp,
    "trap": product_and_trap,
}


def build(name):
    """Build a named logic. `build('lp')` -> Priest's LP."""
    if name not in ALL:
        raise KeyError(f"unknown logic {name!r}; try one of {sorted(ALL)}")
    return ALL[name]()
