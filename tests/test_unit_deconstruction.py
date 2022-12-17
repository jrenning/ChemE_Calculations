from typing import List
from cheme_calculations.heat_transfer.unit_types import Power
from cheme_calculations.units.units import BaseUnit
import pytest
from cheme_calculations.units import Pressure, MultiUnit, Time, Unit


@pytest.mark.parametrize("unit1,unit2,expected", [(MultiUnit(1, "kg^2/m*s^3"), MultiUnit(1, "kg/s"), Unit(1.0, "Pa")),
                                                  (MultiUnit(1, "J^2/s^2"), MultiUnit(1, "J/s"), Unit(1.0, "W")),
                                                  (Pressure(50, "Pa"), MultiUnit(50, "kg/m*s^2"), 1.0),
                                                  (MultiUnit(50, "kg/m*s^2"), Pressure(50, "Pa"), 1.0),
                                                  (Pressure(50, "Pa"), MultiUnit(50, "kg/m"), Unit(1, "s", -2)),
                                                  (Power(50, "W"), MultiUnit(50, "J/s"), 1.0),
                                                  (Power(50, "W"), Time(50, "s", -1), Unit(1, "J"))
                                                        ])
def test_unit_deconstruct_division_cancel(unit1, unit2, expected):
    print(unit1/unit2)
    assert(unit1/unit2 == expected)

@pytest.mark.parametrize("unit,expected", [(MultiUnit(1.0, "J/s"), MultiUnit(1.0, top_half=[BaseUnit("W")])),
                                           (MultiUnit(1.0, "kg*m^2/s^3"), MultiUnit(1.0, top_half=[BaseUnit("W")]))])
def test_unit_simplification(unit: MultiUnit, expected: MultiUnit):
   top_half, bottom_half = unit.simplify_units(unit._top_half, unit._bottom_half)
   new_unit = MultiUnit(unit._value, top_half=top_half, bottom_half=bottom_half)
   assert(new_unit == expected)
   
   
    