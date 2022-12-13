import pytest
from cheme_calculations.units import Pressure, MultiUnit, BaseUnit, Energy, Time, Unit

def test_deconstruct_cancel():
    P = Pressure(50, "Pa")
    m = MultiUnit(50,"kg/m*s^2")
    
    r = m/P
    assert(r == 1.0)
    
def test_unit_simplification():
    k = MultiUnit(1, "kg^2/m*s^3")
    e = MultiUnit(1, "kg/s")
    w = k/e
    assert(w == Unit(1.0,"Pa"))
    
def test_unit_simplification2():
    k = MultiUnit(1, "kg/m*s")
    t = Time(1,"s")
    p = k/t
    assert(p.__repr__() == "1.0 Pa")
    