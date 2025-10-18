"""
Physics-based drilling models package.
Contains first-principles equations for drilling mechanics and hydraulics.
"""

from .drilling_mechanics import DrillingMechanics
from .drilling_hydraulics import DrillingHydraulics

__all__ = ['DrillingMechanics', 'DrillingHydraulics']
