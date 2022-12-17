import pytest
from cheme_calculations.units import Pressure, MultiUnit, Time, Unit

def test_deconstruct_cancel():
    P = Pressure(50, "Pa")
    m = MultiUnit(50,"kg/m*s^2")
    
    r = m/P
    assert(r == 1.0)

@pytest.mark.parametrize("unit1,unit2,expected", [(MultiUnit(1, "kg^2/m*s^3"), MultiUnit(1, "kg/s"), Unit(1.0, "Pa")),
                                                  (MultiUnit(1, "J^2/s^2"), MultiUnit(1, "J/s"), Unit(1.0, "W"))
                                                        ])
def test_unit_simplification(unit1, unit2, expected):
    print(unit1/unit2)
    assert(unit1/unit2 == expected)
    
def test_unit_simplification2():
    k = MultiUnit(1, "kg/m*s")
    t = Time(1,"s")
    p = k/t
    assert(p.__repr__() == "1.0 Pa")
    