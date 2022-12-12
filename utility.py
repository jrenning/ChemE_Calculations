from itertools import chain, combinations
from typing import Literal

from units import MultiUnit

# found here https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1)))

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