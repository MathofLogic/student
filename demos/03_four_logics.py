#!/usr/bin/env python3
"""
DEMO 3 - Four famous logics, one machine. (Workbook Chapter 8)

Run me:  python demos/03_four_logics.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mol import logics
from fractions import Fraction

print(__doc__)

built = [logics.build(n) for n in ["classical", "k3", "l3", "lp"]]
for c in built:
    print(c.report())
    print()

print("=" * 70)
print("THE WHOLE BOOK ON ONE TABLE")
print("=" * 70)
h = Fraction(1, 2)
print(f"{'logic':<20}{'V':<16}{'AND(1/2,1/2)':<15}{'designated':<14}")
print("-" * 70)
for c in built:
    V = "{" + ",".join(str(v) for v in c.V) + "}"
    andv = str(c.AND(h, h)) if h in c.V else "-"
    des = "{" + ",".join(str(v) for v in sorted(c.designated)) + "}"
    print(f"{c.name:<20}{V:<16}{andv:<15}{des:<14}")

print()
print("Read down the columns:")
print("  K3 differs from Classical in V     (added a middle value)")
print("  L3 differs from K3        in G     (one AND cell: 0 instead of 1/2)")
print("  LP differs from K3        in theta (the middle value now counts)")
print()
print("Four people. Four countries. A century apart.")
print("One machine, four settings.")
