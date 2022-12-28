from typing import Literal
from cheme_calculations.units import MultiUnit
from cheme_calculations.units.units import Unit

__all__ = ["getR_constant"]


BOLTZMANS_CONSTANT = MultiUnit(1.380649E-23, "m^2*kg/s^2*K")
AVAGADROS_CONSTANT = Unit(6.02214076E23, "mol", -1)
PLANCKS_CONSTANT = MultiUnit(6.62607015E-34, "m^2*kg/s")
RADIATION_CONSTANT = MultiUnit(5.670E-8, "W/m^2*K^4")
FARADAYS_CONSTANT = MultiUnit(96500, "C/mol")

def getR_constant(temperature_units: Literal["K", "C", "F", "R"],
                  volume_units: Literal["cm^3", "m^3", "L"],
                  pressure_units: Literal["Pa", "kPa", "bar", "atm", "mmHg", "torr"],
                  generic=False):
    if generic:
        return MultiUnit(8.314, "J/mol*K")
    if volume_units == "m^3" and pressure_units == "Pa" and temperature_units == "K":
        return MultiUnit(8.314, "m^3*Pa/mol*K")
    if volume_units == "L" and pressure_units == "atm" and temperature_units == "K":
        return MultiUnit(0.08205, "L*atm/mol*K")
    if volume_units == "m^3" and pressure_units == "atm" and temperature_units == "K":
        return MultiUnit(8.205746E-5, "m^3*atm/mol*K")
    
    raise ValueError("The units supplied to R are not defined in a known constant")