from units import Temperature, MultiUnit, Pressure, BaseUnit, BaseLength, Time, Unit, Velocity
import pytest

@pytest.mark.parametrize("operand1,operand2,expected", [(Temperature(350, 'K'),50,Temperature(400, 'K')),
                                                        (Temperature(350, 'K'), Temperature(350, 'K'), Temperature(700, 'K')),
                                                        ])
def test_unit_addition(operand1, operand2, expected):
    T = operand1 + operand2
    assert(T == expected)

@pytest.mark.parametrize("operand1,operand2,expected", [(Temperature(350, 'K'),50,Temperature(300, 'K')),
                                                        (Temperature(350, 'K'), Temperature(350, 'K'), Temperature(0, 'K')),
                                                        ]) 
def test_unit_subtraction(operand1, operand2, expected):
    assert(operand1 - operand2 == expected)
    

@pytest.mark.parametrize("operand1,operand2,expected", [(Temperature(350, 'K'),2,Temperature(700, 'K')),
                                                        (Temperature(350, 'K'), Temperature(2, 'K'), Temperature(700, 'K', 2)),
                                                        (MultiUnit(350, "J/s"), Unit(1, "s"), Unit(350, "J"))])
def test_unit_multiplication(operand1, operand2, expected):
    assert(operand1 * operand2 == expected)

@pytest.mark.parametrize("operand1,operand2,expected", [(Temperature(350, 'K'),2,Temperature(175, 'K')),
                                                        (Temperature(350, 'K'), Temperature(2, 'K'), 175.0),
                                                        (Temperature(350, 'K', 2), Temperature(2, 'K'), Temperature(175.0,'K'))
                                                        ])
def test_unit_division(operand1, operand2, expected):
    assert(operand1 / operand2 == expected)

    
def test_temperature_conversion():
    T = Temperature(350, 'K')
    T2 = T.convert_to('C')
    assert(T2._unit == 'C')
    assert(T2._value == 350-273.15)

def test_temperature_comversion2():
    T = Temperature(350, 'C')
    T2 = T.convert_to('R')
    assert(T2._unit == "R")
    assert(T2._value == 1121.67)
    
    
def test_renolyds():
    d = BaseLength(1, 'm')
    rho = MultiUnit(1.5,"kg/m^3")
    v = MultiUnit(2, "m/s")
    mu = MultiUnit(3, "kg/m*s")
    r = (rho*v*d)/mu
    assert(r == 1.0)

# def test_equaility():
#     mu = MultiUnit(3, [BaseUnit("kg")], [BaseUnit("m"), BaseUnit("s")])
#     mu2 = MultiUnit(3, [BaseUnit("kg")], [BaseUnit("s"), BaseUnit("m")])
#     assert(mu == mu2)
    