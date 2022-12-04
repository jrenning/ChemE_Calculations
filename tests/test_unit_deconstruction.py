import pytest
from units import Pressure, MultiUnit, BaseUnit, Energy, Time, Unit

# def test_deconstruct_cancel():
#     P = Pressure(50, "Pa")
#     m = MultiUnit(50,[BaseUnit("kg")], [BaseUnit("m"), BaseUnit("s", 2)])
    
#     r = m/P
#     assert(r == 1.0)
    
# def test_unit_simplification():
#     k = MultiUnit(1, [BaseUnit("kg",2)], [BaseUnit("m"), BaseUnit("s",3)])
#     e = MultiUnit(1, [BaseUnit("kg")], [BaseUnit("s")])
#     w = k/e
#     assert(w == Unit(1.0,"Pa"))
    
# def test_unit_simplification2():
#     k = MultiUnit(1, [BaseUnit("kg")], [BaseUnit("m"), BaseUnit("s")])
#     t = Time(1,"s")
#     p = k/t
#     assert(p.__repr__() == "1.0 Pa")
    