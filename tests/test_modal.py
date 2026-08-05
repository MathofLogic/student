"""
test_modal.py — the modal ladder, derived from the seed's reach.

The load-bearing test in this file is not "does the axiom hold". It is
`fails_without`: does the axiom actually FAIL somewhere when the constraint
is removed? Without that half you have only shown the constraint is
compatible with the axiom. With it, you have shown the constraint is doing
the work — which is what "derived" is supposed to mean.

We also cross-check against standard correspondence theory (reflexive-T,
transitive-4, symmetric-B, euclidean-5). Those correspondences were
established long before this repo existed, so reproducing them from our own
enumeration is an external check on the derivation, not a self-graded one.
"""

import sys, os, inspect

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mol import modal
from mol.modal import (all_frames, forces, derive_ladder, countermodel_for,
                       reflexive, transitive, symmetric, euclidean,
                       equivalence, preorder, no_constraint,
                       ax_K, ax_T, ax_4, ax_5, ax_B, box, dia)

N = 3  # every relation on 3 eddies: 512 frames, fully enumerated


def test_modal_provenance():
    """HOUSE RULE: modal.py may import ONLY the seed. If it reaches for a
    logic library, the derivation is a decoration and this test fails."""
    src = inspect.getsource(modal)
    imports = [l.strip() for l in src.splitlines()
               if l.strip().startswith(("import ", "from "))]
    allowed = ("itertools", "seed", "__future__", "dataclasses", "fractions")
    smuggled = [i for i in imports if not any(a in i for a in allowed)]
    assert not smuggled, f"modal.py smuggled non-seed imports: {smuggled}"


def test_modal_frames_enumerated():
    """We really do check every frame, not a sample."""
    frames = list(all_frames(N))
    assert len(frames) == 2 ** (N * N) == 512


def test_modal_K():
    """K is free. Necessity respects implication on EVERY frame — no
    constraint on reach required at all. That is why K is the floor."""
    holds, _ = forces(no_constraint, ax_K, N)
    assert holds, "K must hold on every frame"


def test_modal_T():
    """Reflexive reach (every eddy reaches itself) forces T: box p -> p.
    And T genuinely fails without reflexivity — countermodel exhibited."""
    holds, fails_without = forces(reflexive, ax_T, N)
    assert holds, "reflexive reach must force T"
    assert fails_without, "T must fail somewhere without reflexivity"

    cm = countermodel_for(reflexive, ax_T, N)
    assert cm is not None
    assert not reflexive(cm, N), "the countermodel must be non-reflexive"
    assert not ax_T(cm, N), "and T must actually fail on it"


def test_modal_4():
    """Transitive reach (drag chains through) forces 4: box p -> box box p."""
    holds, fails_without = forces(transitive, ax_4, N)
    assert holds, "transitive reach must force 4"
    assert fails_without, "4 must fail somewhere without transitivity"

    # and on the S4 frame proper (reflexive + transitive) both T and 4 hold
    holds_T, _ = forces(preorder, ax_T, N)
    holds_4, _ = forces(preorder, ax_4, N)
    assert holds_T and holds_4, "S4 frames must give both T and 4"

    # but S4 does NOT get 5 for free — that is the next rung's whole point
    holds_5, _ = forces(preorder, ax_5, N)
    assert not holds_5, "S4 must not already force 5"


def test_modal_5():
    """Equivalence reach (mutual drag) forces 5: dia p -> box dia p."""
    holds, fails_without = forces(equivalence, ax_5, N)
    assert holds, "equivalence reach must force 5"
    assert fails_without, "5 must fail somewhere without equivalence"

    # S5 keeps everything below it on the ladder
    for ax in (ax_T, ax_4, ax_5, ax_B):
        assert forces(equivalence, ax, N)[0], "S5 must retain the lower rungs"


def test_modal_correspondence():
    """External check: reproduce standard correspondence theory from our own
    enumeration. These pairings are textbook and predate this repo, so
    matching them is evidence the derivation is sound, not self-flattery."""
    pairs = [
        (reflexive, ax_T, "reflexive <-> T"),
        (transitive, ax_4, "transitive <-> 4"),
        (symmetric, ax_B, "symmetric <-> B"),
        (euclidean, ax_5, "euclidean <-> 5"),
    ]
    for constraint, axiom, label in pairs:
        holds, fails_without = forces(constraint, axiom, N)
        assert holds, f"{label}: constraint must force the axiom"
        assert fails_without, f"{label}: axiom must fail without the constraint"


def test_modal_ladder_complete():
    """The whole ladder, as the workbook presents it: each rung forced, and
    each rung's constraint doing real work."""
    results = derive_ladder(N)
    assert [r["system"] for r in results] == ["K", "T", "S4", "S5"]
    for r in results:
        assert r["forced"], f"{r['system']} rung not forced"
        if r["constraint"] != "none":
            assert r["fails_without"], f"{r['system']} constraint does no work"
            assert r["countermodel"] is not None


def test_modal_operators_are_reach():
    """box and dia really are 'every reached eddy' / 'some reached eddy' —
    not smuggled truth tables. Checked on a hand-built frame."""
    # eddy 0 reaches 1 and 2; eddy 1 reaches nothing; eddy 2 reaches itself
    R = frozenset({(0, 1), (0, 2), (2, 2)})
    V = (False, True, True)  # pattern coheres in eddies 1 and 2

    assert box(V, R, 0) is True, "coheres in every eddy 0 reaches"
    assert dia(V, R, 0) is True
    # eddy 1 reaches nothing: 'necessary' is vacuously true, 'possible' false
    assert box(V, R, 1) is True, "vacuous truth over an empty reach"
    assert dia(V, R, 1) is False, "nothing reached, so nothing is possible"

    V2 = (False, False, True)
    assert box(V2, R, 0) is False, "eddy 1 is reached and fails to cohere"
    assert dia(V2, R, 0) is True, "but eddy 2 still coheres"
