""" This package holds on the SQLModel pydantic/database models

Treat models as a package: https://docs.python.org/3/tutorial/modules.html#packages
"""

# * Note: Add all module names to this list and import for easier imports outside this module

__all__ = ["count", "team"]

from .count import Count
from .team import Team
