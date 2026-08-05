"""
test_workbook.py — every chalkboard in the Student Edition, checked.

Each test name matches a stamp printed on a chalkboard in the workbook.
A board stamped [FORCED - verified: test_3_2] means: find `test_3_2` here,
run it, watch it pass. If you cannot run the check, the book has not earned
your belief. That contract cuts both ways — these same checks are how you
catch our mistakes.

Runs with plain `python tests/run.py` (no installation) or with pytest.
"""

import sys, os
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mol.carrier import Carrier, F
from mol import logics

HALF = Fraction(1, 2)


# =====================================================================
# CHAPTER 1 — What Can Something Even Be?
# =====================================================================

def test_1_1():
    """Designated values: on {0,1/2,1} the rule 'counts if v > 0' designates
    exactly {1/2, 1}, and 0 alone fails to count. Enumerated, not asserted."""
    V = [F(0), HALF, F(1)]
    designated = [v for v in V if v > 0]
    assert designated == [HALF, F(1)], designated
    assert [v for v in V if not (v > 0)] == [F(0)]

    # and the consequence the workbook cares about: which values count is a
    # CHOICE, and swapping the rule changes the answer without touching V.
    strict = [v for v in V if v == 1]
    assert strict == [F(1)]
    assert strict != designated, "different rule must give a different answer"


def test_1_2():
    """A carrier must be non-empty to say anything, and a one-value carrier
    cannot be informative — nothing can be false in it."""
    one = Carrier("single", [1], lambda v: v, min, max, [1])
    assert one.audit().sealed
    # every value is designated => nothing can fail => no information
    assert all(one.is_designated(v) for v in one.V)
    try:
        Carrier("empty-designation", [0, 1], lambda v: 1 - v, min, max, [2])
        assert False, "designating a value outside V must be refused"
    except ValueError:
        pass


# =====================================================================
# CHAPTER 2 — Three Tools for Everything
# =====================================================================

def test_2_1():
    """The classic wiring on {0,1}: NOT flips, AND needs both, OR takes either."""
    c = logics.classical()
    assert c.NOT(0) == 1 and c.NOT(1) == 0
    assert c.AND(1, 1) == 1
    assert c.AND(1, 0) == 0
    assert c.AND(0, 0) == 0
    assert c.OR(0, 0) == 0
    assert c.OR(1, 0) == 1
    assert c.OR(1, 1) == 1
    assert c.audit().sealed


def test_2_2():
    """Same carrier, different AND. On {0,1} min and product are twins.
    On {0,1/2,1} the mask comes off: 1/2 vs 1/4 — and 1/4 is not in V."""
    for a in (F(0), F(1)):
        for b in (F(0), F(1)):
            assert min(a, b) == a * b, "min and product must agree on {0,1}"

    assert min(HALF, HALF) == HALF
    assert HALF * HALF == Fraction(1, 4)
    assert min(HALF, HALF) != HALF * HALF, "the third value exposes the choice"
    assert Fraction(1, 4) not in [F(0), HALF, F(1)], "and the leak is real"


def test_2_3():
    """Implication is not a fourth primitive: A -> B := OR(NOT A, B).
    False exactly when A is true and B is false."""
    c = logics.classical()
    assert c.IMPLIES(0, 0) == 1
    assert c.IMPLIES(0, 1) == 1
    assert c.IMPLIES(1, 0) == 0
    assert c.IMPLIES(1, 1) == 1


# =====================================================================
# CHAPTER 3 — Laws That Can't Break
# =====================================================================

def test_3_0():
    """THE TRAP. product-AND on {0,1/2,1} reads perfectly and leaks 1/4.
    The audit names the failing part rather than flashing a red light."""
    trap = logics.product_and_trap()
    result = trap.audit()
    assert not result.sealed, "the trap must fail its audit"
    leaked = {l.result for l in result.leaks}
    assert Fraction(1, 4) in leaked, f"expected 1/4 among leaks, got {leaked}"
    # the specific board in the book
    assert trap.AND(HALF, HALF) == Fraction(1, 4)


def test_3_1():
    """THE REPAIR. Swap AND to min and the same carrier seals shut.
    This repaired machine has a name: Kleene's K3."""
    k3 = logics.kleene_k3()
    assert k3.audit().sealed, str(k3.audit())
    assert k3.AND(HALF, HALF) == HALF
    assert k3.V == [F(0), HALF, F(1)], "same carrier as the trap"


def test_3_2():
    """LNC (value reading, as the book prints it): AND(v, NOT v) should hit
    the bottom of V. Forced on {0,1}. Fails at 1/2 on {0,1/2,1}."""
    c = logics.classical()
    holds, fails = c.lnc(reading="value")
    assert holds and not fails

    k3 = logics.kleene_k3()
    holds, fails = k3.lnc(reading="value")
    assert not holds, "LNC must not be forced once a middle value exists"
    assert fails == [(HALF, HALF)], fails

    # HONESTY: the designation reading disagrees, and the book says which it
    # uses. Under designation, 1/2 is not designated, so LNC survives.
    holds_d, _ = k3.lnc(reading="designation")
    assert holds_d, "the two readings genuinely disagree — that is the lesson"


def test_3_3():
    """LEM (value reading): OR(v, NOT v) should hit the top of V.
    Forced on {0,1}. Fails at 1/2 on {0,1/2,1}."""
    c = logics.classical()
    holds, fails = c.lem(reading="value")
    assert holds and not fails

    k3 = logics.kleene_k3()
    holds, fails = k3.lem(reading="value")
    assert not holds
    assert fails == [(HALF, HALF)], fails

    # under the designation reading LEM also fails here, so both agree
    holds_d, _ = k3.lem(reading="designation")
    assert not holds_d


def test_3_4():
    """Double Negation survives every carrier, because it depends only on the
    formula for NOT. Pure algebra: 1-(1-v) = v."""
    for name in ("classical", "k3", "l3", "lp"):
        c = logics.build(name)
        holds, fails = c.dn()
        assert holds, f"DN must hold in {name}, failed at {fails}"

    # and on a much finer carrier, to make the point that it is not luck
    fine = Carrier("101-point", [Fraction(i, 100) for i in range(101)],
                   lambda v: 1 - v, min, max, [1])
    assert fine.dn()[0]
    assert fine.audit().sealed


# =====================================================================
# CHAPTER 4 — The Three Knobs
# =====================================================================

def test_4_1():
    """Classical and K3 differ in V ALONE. Same G, same theta. One knob."""
    c, k = logics.classical(), logics.kleene_k3()

    # same operations, verified on the values they share
    for a in (F(0), F(1)):
        assert c.NOT(a) == k.NOT(a)
        for b in (F(0), F(1)):
            assert c.AND(a, b) == k.AND(a, b)
            assert c.OR(a, b) == k.OR(a, b)

    # same threshold
    assert c.designated == k.designated == frozenset({F(1)})

    # different V — and that alone changes what is forced
    assert set(k.V) - set(c.V) == {HALF}
    assert c.lem(reading="value")[0] is True
    assert k.lem(reading="value")[0] is False


# =====================================================================
# CHAPTER 5 — Everything Costs Something
# =====================================================================

def test_5_1():
    """The receipt for the middle value: you gain a way to say 'maybe',
    you pay with the Law of Excluded Middle. Both halves computable."""
    c, k = logics.classical(), logics.kleene_k3()

    # GAINED: a value that is its own opposite — somewhere for 'maybe' to sit
    assert k.NOT(HALF) == HALF
    assert not any(c.NOT(v) == v for v in c.V), "classical has no such value"

    # PAID: LEM was forced, and is not any more
    assert c.lem(reading="value")[0] is True
    assert k.lem(reading="value")[0] is False

    # the price is not a bug in K3 — the machine is still perfectly sealed
    assert k.audit().sealed


# =====================================================================
# CHAPTER 6 — A Third Option: Maybe
# =====================================================================

def test_6_1():
    """Lukasiewicz's strong AND: two half-truths make a flat zero — and that
    stinginess is exactly what buys back both classical laws."""
    l3 = logics.lukasiewicz_l3()
    assert l3.audit().sealed, str(l3.audit())
    assert l3.AND(HALF, HALF) == 0, "strong AND: 1/2+1/2 does not BEAT 1"
    assert l3.OR(HALF, HALF) == 1, "strong OR: 1/2+1/2 reaches the top"

    # the payoff he was buying
    assert l3.lem(reading="value")[0], "L3 keeps excluded middle"
    assert l3.lnc(reading="value")[0], "L3 keeps non-contradiction"


def test_6_2():
    """Same three values. Same NOT. The two machines differ in exactly one
    AND cell — and that one cell is the whole difference between them."""
    l3, k3 = logics.lukasiewicz_l3(), logics.kleene_k3()

    assert l3.V == k3.V, "identical carrier"
    for v in l3.V:
        assert l3.NOT(v) == k3.NOT(v), "identical NOT"

    # find every cell where the two ANDs disagree
    diffs = [(a, b) for a in l3.V for b in l3.V if l3.AND(a, b) != k3.AND(a, b)]
    assert diffs == [(HALF, HALF)], f"expected exactly one differing cell, got {diffs}"

    assert l3.AND(HALF, HALF) == 0
    assert k3.AND(HALF, HALF) == HALF

    # and that single cell flips a law
    assert l3.lem(reading="value")[0] is True
    assert k3.lem(reading="value")[0] is False


# =====================================================================
# CHAPTER 7 — When Systems Break
# =====================================================================

def test_7_1():
    """Hunting the Liar's home. It needs v = NOT(v). No such value exists on
    {0,1} — that homelessness IS the paradox. On {0,1/2,1} it sits at 1/2."""
    c = logics.classical()
    assert c.liar() == [], "no fixed point: the Liar spins forever"
    assert c.NOT(0) != 0 and c.NOT(1) != 1

    k3 = logics.kleene_k3()
    assert k3.liar() == [HALF], "exactly one home"
    assert k3.NOT(HALF) == HALF

    # a finer carrier does not add more homes — 1/2 is the only fixed point
    fine = Carrier("quarters", [Fraction(i, 4) for i in range(5)],
                   lambda v: 1 - v, min, max, [1])
    assert fine.liar() == [HALF]


def test_7_2():
    """Priest's one move: take K3 and change ONLY theta, so the middle value
    counts. LEM holds, LNC fails, and modus ponens is the bill."""
    k3, lp = logics.kleene_k3(), logics.priest_lp()

    # V and G identical — verified cell by cell, not asserted
    assert k3.V == lp.V
    for a in k3.V:
        assert k3.NOT(a) == lp.NOT(a)
        for b in k3.V:
            assert k3.AND(a, b) == lp.AND(a, b)
            assert k3.OR(a, b) == lp.OR(a, b)

    # theta is the only difference
    assert k3.designated == frozenset({F(1)})
    assert lp.designated == frozenset({HALF, F(1)})

    # and that single change rewrites the logic
    assert lp.lem()[0] is True, "LP keeps excluded middle"
    assert lp.lnc()[0] is False, "LP gives up non-contradiction"
    assert lp.modus_ponens()[0] is False, "and pays for it with modus ponens"


def test_7_3():
    """LP blocks explosion, and we exhibit the countermodel that blocks it.
    A designated contradiction does NOT force every conclusion."""
    lp = logics.priest_lp()
    explodes, witness = lp.explosion()
    assert not explodes, "LP must not explode"
    v, contradiction, q = witness
    assert lp.is_designated(contradiction), "the contradiction is assertible"
    assert not lp.is_designated(q), "yet some conclusion still is not"

    # classical logic, by contrast, has no designated contradiction at all
    c = logics.classical()
    assert all(not c.is_designated(c.AND(v, c.NOT(v))) for v in c.V)


# =====================================================================
# CHAPTER 8 — One Machine, Many Masks
# =====================================================================

def test_8_1():
    """The whole book on one board: four famous logics, four knob settings,
    every difference readable off (V, G, theta)."""
    c = logics.classical()
    k = logics.kleene_k3()
    l = logics.lukasiewicz_l3()
    p = logics.priest_lp()

    # all four are legal machines
    for m in (c, k, l, p):
        assert m.audit().sealed, f"{m.name} must be closed"

    # the signature table the book prints (value reading for the laws,
    # designation reading for LP where the threshold is the whole point)
    assert (c.lem("value")[0], c.lnc("value")[0]) == (True, True)
    assert (k.lem("value")[0], k.lnc("value")[0]) == (False, False)
    assert (l.lem("value")[0], l.lnc("value")[0]) == (True, True)
    assert (p.lem()[0], p.lnc()[0]) == (True, False)

    # and the knob that distinguishes each pair
    assert set(k.V) != set(c.V), "K3 differs from classical in V"
    assert l.V == k.V and l.AND(HALF, HALF) != k.AND(HALF, HALF), "L3 differs in G"
    assert p.V == k.V and p.designated != k.designated, "LP differs in theta"
    for a in k.V:
        for b in k.V:
            assert p.AND(a, b) == k.AND(a, b), "LP shares K3's G exactly"
