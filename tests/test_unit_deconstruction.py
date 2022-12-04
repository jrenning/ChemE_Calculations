import pytest
from units import Pressure, MultiUnit, BaseUnit

def test_deconstruct_cancel():
    P = Pressure(50, "Pa")
    m = MultiUnit(50,[BaseUnit("kg")], [BaseUnit("m"), BaseUnit("s", 2)])
    
    r = m/P
    assert(r == 1.0)