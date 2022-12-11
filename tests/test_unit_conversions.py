from units import Velocity, MultiUnit, DynamicViscosity
import pytest

@pytest.mark.parametrize("unit1,unit2,expected", [(Velocity(3, 'm/s'),"cm/s",Velocity(300.0, 'cm/s')),
                                                        (DynamicViscosity(1, 'cP'), "kg/s*m", DynamicViscosity(1/1000, 'kg/m*s')),
                                                        ])
def test_multi_unit_conversion(unit1, unit2, expected):
    a = unit1.convert_to(unit2)
    assert(a == expected)