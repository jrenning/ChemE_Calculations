from collections import namedtuple
from cheme_calculations.units import Temperature, Density, Cp, DynamicViscosity
from cheme_calculations.units.units import Length

StandardValues = namedtuple('StandardValues', ["Temperature", "Density", "Cp", "Viscosity", "Length"])

std = StandardValues(Temperature(298.25, "K"), Density(1000, "kg/m^3"), Cp(4.18, "kJ/kg*K"), DynamicViscosity(.0001, "kg/m*s"), Length(1, "m"))
