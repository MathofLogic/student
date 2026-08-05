#!/usr/bin/env python3
"""
run.py — THE GATE. Run this. It runs everything and grades itself.

    python tests/run.py

No installation, no pytest, no dependencies. Python 3.8+ and nothing else,
because a book about checking things for yourself should not open with
"first, install these seven packages".

(pytest also works if you prefer it: `pytest tests/`.)

Exit code 0 means every claim stamped on a chalkboard was checked and held.
Exit code 1 means the book lost to the tests, which is the correct outcome
when the book is wrong.
"""

import sys, os, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import test_workbook, test_modal, test_seed          # noqa: E402
from mol import manifest                              # noqa: E402

SUITES = [
    ("Workbook chalkboards", test_workbook,
     "every board stamped in the Student Edition"),
    ("Modal from the seed", test_modal,
     "K -> T -> S4 -> S5, derived and checked both directions"),
    ("The seed pattern", test_seed,
     "the mechanism, and its anti-reification commitments"),
]


def run_suite(module):
    names = sorted(n for n in dir(module) if n.startswith("test_"))
    passed, failed = [], []
    for n in names:
        try:
            getattr(module, n)()
            passed.append(n)
        except Exception:
            failed.append((n, traceback.format_exc()))
    return passed, failed


def main():
    t0 = time.time()
    print()
    print("=" * 64)
    print(" THE MATH OF LOGIC — Student Edition")
    print(" Running every check the workbook cites.")
    print("=" * 64)

    total_pass, total_fail = 0, []
    for title, module, blurb in SUITES:
        print(f"\n  {title}")
        print(f"  {blurb}")
        print("  " + "-" * 58)
        passed, failed = run_suite(module)
        for n in passed:
            print(f"    [ok]   {n}")
        for n, tb in failed:
            print(f"    [FAIL] {n}")
        total_pass += len(passed)
        total_fail.extend(failed)

    print()
    print("=" * 64)
    if total_fail:
        print(f" {len(total_fail)} CHECK(S) FAILED — the book loses to the tests.")
        print("=" * 64)
        for n, tb in total_fail:
            print(f"\n--- {n} ---\n{tb}")
        return 1

    print(f" ALL {total_pass} CHECKS PASSED   ({time.time()-t0:.2f}s)")
    print("=" * 64)
    print()
    print(manifest.render())
    print()
    print(" Every chalkboard in the Student Edition is backed by a test above.")
    print(" Disagree with a result? Change the code and re-run. If your run")
    print(" disagrees with the book, trust your run and then find the bug —")
    print(" in the book or in your change. That is the whole epistemology.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
