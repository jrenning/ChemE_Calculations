from cheme_calculations.units import Temperature
from cheme_calculations.units.property_units import DynamicViscosity, Velocity
from cheme_calculations.units.units import MultiUnit, Unit
import pytest
from pytest import approx

@pytest.mark.parametrize("unit1,unit2,expected", [(Velocity(3, 'm/s'),"cm/s",Velocity(300.0, 'cm/s')),
                                                        (DynamicViscosity(1, 'cP'), "kg/s*m", DynamicViscosity(1/1000, 'kg/m*s')),
                                                        (MultiUnit(5, "m^3"), "cm^3", MultiUnit(5E6, "cm^3")),
                                                        (MultiUnit(1, "W/m^2*K"), "BTU/hr*ft^2*F", MultiUnit(approx(.17611), "BTU/hr*ft^2*F"))
                                                        ])
def test_multi_unit_conversion(unit1, unit2, expected):
    a = unit1.convert_to(unit2)
    assert(a == expected)
    
@pytest.mark.parametrize("unit1,unit2,expected", [(Temperature(300, 'C'), "K", Temperature(573.15, "K")),
                                                        (Temperature(300, 'F'), "C", Temperature(approx(148.889), 'C')),
                                                        (Temperature(350, "K"), "C", Temperature(350-273.15, "C")),
                                                        (Temperature(350, "C"), "R", Temperature(1121.67, "R"))
                                                        ])
def test_unit_conversions(unit1, unit2, expected):
    a = unit1.convert_to(unit2)
    assert(a == expected)