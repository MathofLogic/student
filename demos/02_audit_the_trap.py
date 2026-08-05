#!/usr/bin/env python3
"""
DEMO 2 - Audit before you admire. (Workbook Chapter 3)

The prettiest machine in this subject is broken, and you will not catch it
by reading. Run me:  python demos/02_audit_the_trap.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mol import logics

print(__doc__)
print("Multiplying truth values feels obvious. AND(a,b) = a * b.")
print("On {0,1} it is even correct - min and product agree perfectly.\n")

trap = logics.product_and_trap()
print(f"Now put it on three values: {trap.name}")
print(f"  AND(1/2, 1/2) = {trap.AND('1/2','1/2')}")
print("\nRun the audit:\n")
print(trap.audit())
print()
print("-" * 62)
print("Nobody catches that by reading. The AUDIT catches it.")
print("Note the audit NAMES the failing parts - design your tools for the")
print("mechanic, not the dashboard.\n")

print("The repair: swap AND to min. Same carrier, same NOT.\n")
k3 = logics.kleene_k3()
print(f"{k3.name}: {k3.audit()}")
print(f"  AND(1/2, 1/2) = {k3.AND('1/2','1/2')}  <- stays inside V")
print()
print("That repaired machine has a name: Kleene's strong three-valued logic.")
print("Good fixes are like that - every teaching point survives the repair.")
