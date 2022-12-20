import pytest
from cheme_calculations.units import MultiUnit, BaseUnit

def test_unit_prefix_deconstruction():
    a = MultiUnit(1, "kW/km")
    top_half, bottom_half, factor = a.deconstruct_unit_prefixes(a._top_half, a._bottom_half)
    
    assert(top_half == [BaseUnit("W")])
    assert(bottom_half == [BaseUnit("m")])
    assert(factor == 1)
    
    
def test_op_w_prefixes():
    a = MultiUnit(1, "MW/Mm")
    b = MultiUnit(1, "kg/s")
    
    c = a/b
    
    assert(c == MultiUnit(1.0, "m/s^2"))
    
    
def test_op_w_prefixes2():
    a = MultiUnit(1, "kJ/s")
    b = MultiUnit(1, "J/s")
    
    c = a * b
    
    print(c)
    
    assert(c == MultiUnit(1000, "W^2"))
    
    
    

