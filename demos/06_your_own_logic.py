#!/usr/bin/env python3
"""
DEMO 6 - Build your own logic, then audit it. (Workbook Chapter 8 challenge)

This file is a TEMPLATE. Edit it. Break it. Re-run it.
Run me:  python demos/06_your_own_logic.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mol import Carrier

print(__doc__)

# ====================================================================
# STEP 1 - pick a job. This one: a group-chat hangout tracker.
# STEP 2 - turn the three knobs.
# ====================================================================
mine = Carrier(
    name="Hangout tracker",
    V=[0, "1/2", 1],                 # KNOB 1: out / maybe / in
    not_=lambda v: 1 - v,            # KNOB 2: NOT, AND, OR
    and_=min,                        #   "are we BOTH in?"
    or_=max,                         #   "is EITHER of us in?"
    designated=[1],                  # KNOB 3: only a firm yes is a plan
    note="out=0, maybe=1/2, in=1",
)

print("STEP 3 - the audit (always before you admire it):")
print(" ", mine.audit(), "\n")

print("STEP 4 - what your choices force:")
print(mine.report())
print()

print("STEP 5 - name your price:")
lem_holds, lem_fails = mine.lem(reading="value")
if not lem_holds:
    v, r = lem_fails[0]
    print("  You gained a 'maybe' value.")
    print(f"  You paid excluded middle: at v={v}, OR(v, NOT v) = {r}, not {mine.top}.")
    print("  'You're either in or out' is no longer forced. That is the bill.")
else:
    print("  LEM survived - so find what you paid somewhere else. Something always is.")
print()

print("STEP 6 - stay honest. What does this map ignore?")
print("  Everything about WHY someone is a maybe, how strongly, and whether")
print("  they will flake. Real friends are richer than three values.")
print("  The logic is a useful map. It is not the friendship.")
print()
print("-" * 62)
print("NOW EDIT THIS FILE. Suggestions:")
print("  * add a fourth value and re-run the audit")
print("  * swap `and_=min` for `and_=lambda a,b: a*b` and watch it leak")
print("  * move `designated` to ['1/2', 1] and see which laws flip")
