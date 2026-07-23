"""
carrier.py — the three knobs, in code.

A formal system is completely specified by three things:

    V      the value space   — what values are allowed
    G      the operations    — how you combine them (NOT, AND, OR)
    theta  the threshold     — which values count as "yes" (designated)

Everything in the student workbook is a setting of those three knobs.
This module is the machine; `logics.py` supplies the settings.

Two design decisions worth knowing about, because the workbook says to
name your choices out loud:

  1. We use exact `Fraction` arithmetic, never floats. `0.1 + 0.2 != 0.3`
     in floating point, and a logic library that fails its own equality
     checks would be a bad joke. Fractions make every check exact.

  2. Law checks come in two readings, and we implement BOTH because they
     disagree and the disagreement is a teaching moment (see `lnc`).
     Hiding it would be exactly the reification the workbook warns about.
"""

from fractions import Fraction
from itertools import product

__all__ = ["F", "Carrier", "Leak", "AuditResult"]


def F(x):
    """Make an exact value. F('1/2'), F(0.5), F(1) all work."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, float):
        # go through the string so 0.5 -> 1/2, not 4503599627370496/9007199254740992
        return Fraction(str(x))
    return Fraction(x)


class Leak(tuple):
    """A single closure failure: which op, which inputs, what leaked out."""

    def __new__(cls, op, inputs, result):
        return super().__new__(cls, (op, inputs, result))

    op = property(lambda s: s[0])
    inputs = property(lambda s: s[1])
    result = property(lambda s: s[2])

    def __str__(self):
        ins = ", ".join(str(i) for i in self.inputs)
        return f"{self.op}({ins}) = {self.result}  <-- not in V"


class AuditResult:
    """The outcome of a closure audit. Truthy iff the machine is sealed."""

    def __init__(self, leaks):
        self.leaks = list(leaks)

    def __bool__(self):
        return not self.leaks

    @property
    def sealed(self):
        return not self.leaks

    def __str__(self):
        if self.sealed:
            return "CLOSED — no leaks. Every operation stays inside V."
        head = f"LEAKS — {len(self.leaks)} operation(s) escaped V:"
        body = "\n".join("    " + str(l) for l in self.leaks[:8])
        more = "" if len(self.leaks) <= 8 else f"\n    ... and {len(self.leaks)-8} more"
        return head + "\n" + body + more


class Carrier:
    """A formal system: values V, operations G, threshold theta.

    theta is given as a *set of designated values* — the values that count
    as "yes" for your purpose. That is the honest form: the workbook's
    "designated iff v > 0" is just one rule for producing this set.
    """

    def __init__(self, name, V, not_, and_, or_, designated, note=""):
        self.name = name
        self.V = [F(v) for v in V]
        self.not_ = not_
        self.and_ = and_
        self.or_ = or_
        self.designated = frozenset(F(d) for d in designated)
        self.note = note
        undeclared = self.designated - set(self.V)
        if undeclared:
            raise ValueError(
                f"{name}: designated values {sorted(undeclared)} are not in V. "
                "You cannot designate a value the carrier does not have."
            )

    # ---- the operations, exposed with names students recognise ----------
    def NOT(self, v):
        return F(self.not_(F(v)))

    def AND(self, a, b):
        return F(self.and_(F(a), F(b)))

    def OR(self, a, b):
        return F(self.or_(F(a), F(b)))

    def IMPLIES(self, a, b):
        """Implication is not a fourth primitive — it is built from the three.
        A -> B  :=  OR(NOT A, B).   (Workbook Ch 2.)"""
        return self.OR(self.NOT(a), b)

    def is_designated(self, v):
        return F(v) in self.designated

    @property
    def top(self):
        return max(self.V)

    @property
    def bottom(self):
        return min(self.V)

    # ---- the audit: run this BEFORE admiring any machine -----------------
    def audit(self):
        """Closure audit. Every operation must map V into V.

        The workbook's rule: an operation that leaks outside V is not an
        operation ON V. A law about a leaky carrier is a law about nothing.

        Returns an AuditResult that *names the failing parts*, not just a
        red light — design your tools for the mechanic, not the dashboard.
        """
        Vs = set(self.V)
        leaks = []
        for v in self.V:
            r = self.NOT(v)
            if r not in Vs:
                leaks.append(Leak("NOT", (v,), r))
        for a, b in product(self.V, repeat=2):
            r = self.AND(a, b)
            if r not in Vs:
                leaks.append(Leak("AND", (a, b), r))
            r = self.OR(a, b)
            if r not in Vs:
                leaks.append(Leak("OR", (a, b), r))
        return AuditResult(leaks)

    # ---- law checks, by complete enumeration ----------------------------
    # Each returns (holds, witnesses) where witnesses are the failing values.

    def lnc(self, reading="designation"):
        """Law of Non-Contradiction: nothing is both true and its opposite.

        TWO READINGS, and they can disagree — this is not a bug, it is the
        subject being honest:

          "designation" : AND(v, NOT v) is never DESIGNATED.
          "value"       : AND(v, NOT v) always equals the bottom of V.

        In classical logic both agree. In Kleene's K3 they disagree, because
        AND(1/2, 1/2) = 1/2, which is not the bottom (value reading fails)
        but is also not designated (designation reading holds). Any book that
        reports one without saying which has quietly picked a side for you.
        """
        fails = []
        for v in self.V:
            r = self.AND(v, self.NOT(v))
            bad = self.is_designated(r) if reading == "designation" else (r != self.bottom)
            if bad:
                fails.append((v, r))
        return (not fails), fails

    def lem(self, reading="designation"):
        """Law of Excluded Middle: everything is true or false, no third way.

          "designation" : OR(v, NOT v) is always DESIGNATED.
          "value"       : OR(v, NOT v) always equals the top of V.
        """
        fails = []
        for v in self.V:
            r = self.OR(v, self.NOT(v))
            bad = (not self.is_designated(r)) if reading == "designation" else (r != self.top)
            if bad:
                fails.append((v, r))
        return (not fails), fails

    def dn(self):
        """Double Negation: NOT(NOT(v)) == v. Depends only on NOT."""
        fails = [(v, self.NOT(self.NOT(v))) for v in self.V
                 if self.NOT(self.NOT(v)) != v]
        return (not fails), fails

    def modus_ponens(self):
        """If A is designated and (A -> B) is designated, is B designated?

        Classical logic says obviously yes. Priest's LP says: not always —
        and that is the bill LP pays for tolerating contradictions.
        """
        fails = []
        for a, b in product(self.V, repeat=2):
            if self.is_designated(a) and self.is_designated(self.IMPLIES(a, b)):
                if not self.is_designated(b):
                    fails.append((a, b))
        return (not fails), fails

    def explosion(self):
        """Ex falso: does a designated contradiction force EVERYTHING?

        Returns (explodes, witness). If some contradiction is designated
        while some conclusion is not, explosion is BLOCKED and we hand back
        the countermodel that blocks it.
        """
        for v in self.V:
            contradiction = self.AND(v, self.NOT(v))
            if self.is_designated(contradiction):
                for q in self.V:
                    if not self.is_designated(q):
                        return False, (v, contradiction, q)
        return True, None

    def liar(self):
        """The Liar sentence demands v == NOT(v). Where can it live?

        Returns the list of fixed points. Empty list = no home = the
        sentence spins forever, which is the whole of the 'paradox'.
        """
        return [v for v in self.V if self.NOT(v) == v]

    # ---- reporting -------------------------------------------------------
    def report(self, reading="designation"):
        """Human-readable summary. Used by the demos."""
        lines = [f"{self.name}"]
        if self.note:
            lines.append(f"  {self.note}")
        lines.append(f"  V = {{{', '.join(str(v) for v in self.V)}}}")
        lines.append(f"  designated = {{{', '.join(str(v) for v in sorted(self.designated))}}}")
        a = self.audit()
        lines.append(f"  closure : {'CLOSED' if a.sealed else 'LEAKS'}")
        for label, (holds, _) in (
            ("LNC", self.lnc(reading)),
            ("LEM", self.lem(reading)),
            ("DN ", self.dn()),
            ("MP ", self.modus_ponens()),
        ):
            lines.append(f"  {label}     : {'holds' if holds else 'FAILS'}")
        fp = self.liar()
        lines.append(f"  liar    : {'resolves at ' + str(fp) if fp else 'no fixed point'}")
        return "\n".join(lines)

    def __repr__(self):
        return f"<Carrier {self.name} |V|={len(self.V)}>"
