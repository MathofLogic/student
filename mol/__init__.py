"""
The Math of Logic — Student Edition, verified.

Every chalkboard in the student workbook is checked here by complete
enumeration. Nothing is asserted that is not run.

    from mol import build
    build("lp").report()

Stdlib only. No installation. Python 3.8+.
"""
from .carrier import Carrier, F, Leak, AuditResult
from .logics import (classical, kleene_k3, lukasiewicz_l3, priest_lp,
                     product_and_trap, build, ALL)

__version__ = "1.0.0"
__all__ = ["Carrier", "F", "Leak", "AuditResult", "classical", "kleene_k3",
           "lukasiewicz_l3", "priest_lp", "product_and_trap", "build", "ALL"]
