"""
seed.py — THE PATTERN. The mechanism everything else is a setting of.

This module is deliberately impoverished. It knows about six things, and
not one of them is a truth value, an operator, a number, or a logic:

    propagation   a pattern carrying a loaded history
    gradient      the support available in a context; it VENTS some
                  perturbations back to simplicity
    load          accumulated history, measured RELATIVE to a gradient
    confluence    two propagations meeting
    drag          one loaded history's demands meeting another's
    boundary      past which a propagation RECONFIGURES to something simpler

That is the whole physics. Nothing here mentions logic.

The point of keeping it this bare is that `modal.py` may import ONLY this
module. If the modal ladder needs a primitive the seed does not have, the
derivation failed and the test suite says so out loud. A derivation you
cannot fail is not a derivation, it is a decoration.

The reading (workbook Ch 4): a logic is a setting of three knobs, and the
knobs themselves are readings of this mechanism —

    V      = which plateaus stabilise in the gradient
    G      = confluence, read as combination
    theta  = the stability boundary
"""

from dataclasses import dataclass

__all__ = ["Propagation", "Gradient", "REST", "confluence", "drag", "same_load"]


@dataclass(frozen=True)
class Propagation:
    """A pattern carrying a loaded history.

    NOTE what is deliberately absent: identity. A propagation is not an
    object with an intrinsic name. Two propagations are "the same" only
    relative to a gradient (see `same_load`) — sameness is a relation here,
    never an essence. That is the anti-reification rule made mechanical.
    """

    history: tuple = ()

    def perturb(self, mark="."):
        """One more differential propagation: accumulate load."""
        return Propagation(self.history + (mark,))

    def __repr__(self):
        return f"Propagation(load={len(self.history)})"


REST = Propagation(())  # no accumulated history. Not an object called zero.


@dataclass(frozen=True)
class Gradient:
    """The support available in a context.

    `vent` is the set of marks this context dissipates back to simplicity —
    they accumulate no persisting load. `boundary` is how much load the
    context can hold before the pattern reconfigures.

    The same propagation has DIFFERENT load in different gradients. There is
    no gradient-free fact about load. That is the whole anti-intrinsicality
    commitment, in one field.
    """

    vent: frozenset = frozenset()
    boundary: float = float("inf")

    def load(self, p):
        """Loaded history relative to THIS gradient: marks not vented."""
        return sum(1 for m in p.history if m not in self.vent)

    def coheres(self, p):
        """Does this pattern stay stable here, or has drag exceeded room?"""
        return self.load(p) <= self.boundary

    def reconfigure(self, p):
        """Past the boundary the pattern breaks down into simpler coherent
        structure, venting simplicity back into the field."""
        L = self.load(p)
        if L <= self.boundary:
            return p
        room = int(self.boundary) + 1
        return Propagation((".",) * (L % room))


UNIFORM = Gradient()  # vents nothing; pure accumulation


def confluence(a, b):
    """Two propagations meeting: b's accumulation carried on from a."""
    out = a
    for mark in b.history:
        out = out.perturb(mark)
    return out


def drag(a, b, g=UNIFORM):
    """Loaded-history demand meeting loaded-history demand."""
    return g.load(confluence(a, b))


def same_load(a, b, g=UNIFORM):
    """The only sameness the seed permits: equal load on a gradient.

    Note the signature: you cannot ask whether two propagations are the same
    without saying *in which gradient*. Two different histories can be the
    same here if the gradient vents their difference.
    """
    return g.load(a) == g.load(b)
