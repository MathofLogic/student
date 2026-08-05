"""
test_seed.py — the pattern everything else is derived from.

The seed's job is to be POOR. It must carry the mechanism and nothing else:
no truth values, no operators, no numbers-as-objects. These tests check the
mechanism works and, just as importantly, that its anti-reification
commitments are real rather than decorative.
"""

import sys, os, inspect

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mol import seed
from mol.seed import (Propagation, Gradient, REST, UNIFORM,
                      confluence, drag, same_load)


def test_seed_accumulates():
    """Perturbation accumulates loaded history."""
    p = REST.perturb().perturb().perturb()
    assert UNIFORM.load(REST) == 0
    assert UNIFORM.load(p) == 3


def test_seed_confluence():
    """Two propagations meeting carry both histories."""
    a = REST.perturb().perturb()
    b = REST.perturb().perturb().perturb()
    assert UNIFORM.load(confluence(a, b)) == 5
    assert drag(a, b) == 5


def test_seed_relative():
    """LOAD IS GRADIENT-RELATIVE. Two DIFFERENT histories can carry the same
    load if the gradient vents their difference.

    This is the anti-intrinsicality commitment made mechanical: there is no
    gradient-free fact about how loaded a pattern is. An object would have an
    intrinsic size. A propagation does not."""
    steam = Gradient(vent=frozenset(["x"]))
    a = Propagation((".", "x", "."))   # 3 marks, one vented
    b = Propagation((".", "."))        # 2 marks

    assert a.history != b.history, "genuinely different histories"
    assert steam.load(a) == steam.load(b) == 2
    assert same_load(a, b, steam), "same load on this gradient"
    assert not same_load(a, b, UNIFORM), "and NOT on a gradient that vents nothing"


def test_seed_sameness_needs_a_gradient():
    """You cannot ask whether two propagations are the same without saying in
    which gradient. The signature enforces it."""
    sig = inspect.signature(same_load)
    assert "g" in sig.parameters, "sameness must take a gradient"


def test_seed_reconfigure():
    """Past the stability boundary a propagation RECONFIGURES to something
    simpler rather than accreting forever. A pile of objects would only grow;
    a pattern under drag breaks down and vents simplicity."""
    cup = Gradient(boundary=3)
    big = Propagation((".",) * 9)

    assert not cup.coheres(big), "9 exceeds a boundary of 3"
    settled = cup.reconfigure(big)
    assert cup.load(settled) < 9, "it must come down, not keep climbing"
    assert cup.coheres(settled), "and land somewhere stable"

    small = Propagation((".",) * 2)
    assert cup.coheres(small)
    assert cup.reconfigure(small) is small, "within bounds, nothing happens"


def test_seed_has_no_logic_in_it():
    """The seed must not know about logic. If someone adds a truth value or a
    logical operator here, the derivations downstream stop being derivations.

    NOTE we scan EXECUTABLE CODE ONLY — identifiers and operators, with
    comments and docstrings stripped. Prose explaining what the seed
    deliberately lacks is allowed to name the thing it lacks; code is not.
    (The first version of this test scanned raw source and failed on its own
    docstring. Left in the history as a lesson: a check can be right in
    spirit and wrong in scope.)
    """
    import io, tokenize

    src = inspect.getsource(seed)
    identifiers = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.NAME:
            identifiers.append(tok.string.lower())

    banned = ("truth", "designated", "tautology", "boolean", "axiom",
              "conjunction", "disjunction", "negation")
    hits = [b for b in banned if any(b in ident for ident in identifiers)]
    assert not hits, f"the seed's CODE mentions {hits} — it should not"

    # positive half: the seed must actually contain the mechanism
    for required in ("propagation", "gradient", "load", "confluence",
                     "reconfigure", "vent", "boundary"):
        assert any(required in i for i in identifiers), \
            f"the seed is missing its own mechanism: {required!r}"


def test_seed_origin_is_not_an_object():
    """REST is the absence of accumulated history, not an object called zero."""
    assert REST.history == ()
    assert UNIFORM.load(REST) == 0
    # and it is reachable only by having no perturbations, not by construction
    assert Propagation(()) == REST
