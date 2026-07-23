#!/usr/bin/env python3
"""
DEMO 4 - Hunt the Liar. (Workbook Chapter 7)

"This sentence is false." Where can it live?
Run me:  python demos/04_liar_hunt.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mol import Carrier, logics
from fractions import Fraction

print(__doc__)
print("The Liar demands a value where  v = NOT(v).  Let us hunt it.\n")

for name in ["classical", "k3", "l3", "lp"]:
    c = logics.build(name)
    fp = c.liar()
    where = f"lives at {fp[0]}" if fp else "NO HOME - it spins forever"
    print(f"  {c.name:<20} {where}")

print("\nDoes a bigger carrier give it more homes? Let us check.\n")
for n in (2, 3, 5, 9, 101):
    V = [Fraction(i, n - 1) for i in range(n)]
    c = Carrier(f"{n}-value", V, lambda v: 1 - v, min, max, [1])
    fp = c.liar()
    print(f"  {n:>4} values -> fixed points: {[str(x) for x in fp] or 'none'}")

print()
print("-" * 62)
print("Exactly one home, always at 1/2, and only when the carrier stocks it.")
print("The 'paradox' was never a crack in reality. It was a two-value")
print("carrier being asked for a value it did not stock.")
print()
print("A map can leave a mountain off the map. The hikers should still be")
print("told which map they are holding.")
