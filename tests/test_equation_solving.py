from cheme_calculations.units import ThermalConductivity, Temperature, Area, Length
from cheme_calculations.units.heat_transfer import Power
from cheme_calculations.utility.equation_solving import OverSpecifiedProblem, SolutionNotSupported, UnsolvableEquation
from .standard_values import std
from cheme_calculations.heat_transfer import planar_heat
import pytest


def test_planar_heat_solving_errors():
    thickness = std.Length
    k = std.ThermalConductivity
    T1 = std.Temperature
    T2 = Temperature(400, "K")
    area = Area(1, "m^2")
    q = Power(500, "W")
    with pytest.raises(OverSpecifiedProblem) as e_info:
        planar_heat(k, T1, T2, area, thickness, q)
    with pytest.raises(UnsolvableEquation) as e_info:
        planar_heat(k, None, T2, area, thickness)
    with pytest.raises(SolutionNotSupported) as e_info:
        planar_heat(None, T1, T2, area, thickness, q)
        
def test_heat_exchanger_solving_errors():
    pass
    
    
    
    