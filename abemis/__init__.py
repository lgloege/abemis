"""Set up module access for the base package."""

from . import stationary_energy
from . import ippu
from . import transportation
from . import waste
from . import afolu
from . import constants
from . import efdb

from .activity_based import general_formula

__all__ = [
    "stationary_energy",
    "efdb",
    "ippu",
    "transportation",
    "waste",
    "afolu",
    "constants",
    "general_formula",
]
