#!/usr/bin/env python3
"""
DEMO 5 - The modal ladder, derived from the pattern.

K -> T -> S4 -> S5, from one fact: how far a pattern's influence REACHES.
Run me:  python demos/05_modal_ladder.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mol.modal import derive_ladder, all_frames, forces, CONSTRAINTS, AXIOMS

print(__doc__)

N = 3
print(f"Enumerating EVERY way reach can be arranged on {N} eddies:")
print(f"  {len(list(all_frames(N)))} frames. Not a sample. All of them.\n")
print("  eddies                    -> worlds")
print("  'i reaches j'             -> accessibility R")
print("  coheres in EVERY reached  -> NECESSARY (box)")
print("  coheres in SOME reached   -> POSSIBLE  (diamond)\n")

print("=" * 70)
for r in derive_ladder(N):
    print(f"  {r['system']:<4} {r['story']}")
    print(f"       constraint : {r['constraint']}")
    print(f"       buys axiom : {r['axiom']}   {r['formula']}")
    print(f"       forced     : {r['forced']}")
    if r["fails_without"] is None:
        print("       without it : n/a - K needs no constraint, it is the floor")
    else:
        print("       without it : FAILS  (constraint is doing real work)")
        cm = r["countermodel"]
        print(f"       witness    : R = {sorted(cm) if cm else '-'}")
    print()

print("=" * 70)
print("The 'without it' line of each rung is the honest one.")
print("Showing an axiom HOLDS under a constraint proves only compatibility.")
print("Showing it FAILS without the constraint proves the constraint is")
print("doing the work. That is the difference between a derivation and a")
print("coincidence, and it is why this demo enumerates both directions.\n")

print("Cross-check against standard correspondence theory")
print("(these pairings are textbook and predate this repo):")
for c, a in [("reflexive", "T"), ("transitive", "4"),
             ("symmetric", "B"), ("euclidean", "5")]:
    h, f = forces(CONSTRAINTS[c][0], AXIOMS[a][0], N)
    print(f"  {c:<12} <-> {a}:  forced={h}, fails without={f}")
