#!/usr/bin/env python3
"""
DEMO 1 - Build a carrier. (Workbook Chapter 1)

The first knob: what values is something allowed to be?
Run me:  python demos/01_build_a_carrier.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mol import Carrier

print(__doc__)
print("A light switch has two options. A traffic light has three.\n")

switch = Carrier("Light switch", [0, 1], lambda v: 1 - v, min, max, [1],
                 note="OFF=0, ON=1. Only ON counts as 'lit'.")
print(switch.report(), "\n")

traffic = Carrier("Traffic light", [0, "1/2", 1], lambda v: 1 - v, min, max, [1],
                  note="RED=0, YELLOW=1/2, GREEN=1. Only GREEN counts as 'go'.")
print(traffic.report(), "\n")

print("Now the SAME traffic light, different question - 'should I be alert?'")
print("Nothing about the values changes. Only which ones count.\n")

alert = Carrier("Traffic light (alert?)", [0, "1/2", 1], lambda v: 1 - v,
                min, max, ["1/2", 1],
                note="YELLOW and GREEN both count now.")
print(alert.report(), "\n")

print("-" * 62)
print("Notice: `traffic` and `alert` have identical V and identical G.")
print("They differ only in theta - which values count. And look what that")
print("did to the law checks. One knob. Different logic.")
print()
print("YOUR TURN: change the carrier below and re-run this file.")
print("  Try a homework tracker: not-started / in-progress / done.")
print("  Which values should count as 'can I submit it'?")
