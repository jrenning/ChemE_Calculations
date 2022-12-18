from cheme_calculations.units import Temperature, MultiUnit, Length, Unit
import pytest

@pytest.mark.parametrize("operand1,operand2,expected", [(Temperature(350, 'K'),50,Temperature(400, 'K')),
                                                        (Temperature(350, 'K'), Temperature(350, 'K'), Temperature(700, 'K')),
                                                        ])
def test_unit_addition(operand1, operand2, expected):
    T = operand1 + operand2
    assert(T == expected)
    

@pytest.mark.parametrize("operand1, operand2", [(Unit(1, "K"), MultiUnit(2, "K/W")),
                                                (Unit(1, "K"), Unit(1, "Pa")), 
                                                (MultiUnit(2, "K/W"), MultiUnit(4, "m/s"))])
def test_improper_addition(operand1, operand2):
    
    # e info makes sure it doesn't fail for just displaying a message 
    with pytest.raises(TypeError) as e_info:
        operand1 + operand2

@pytest.mark.parametrize("operand1, operand2", [(Unit(1, "K"), MultiUnit(2, "K/W")),
                                                (Unit(1, "K"), Unit(1, "Pa")), 
                                                (MultiUnit(2, "K/W"), MultiUnit(4, "m/s"))])    
def test_improper_subtraction(operand1, operand2):
    # e info makes sure it doesn't fail for just displaying a message 
    with pytest.raises(TypeError) as e_info:
        operand1 - operand2


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
                                                        (Temperature(350, 'K', 2), Temperature(2, 'K'), Temperature(175.0,'K')),
                                                        (MultiUnit(50, "m^2/s^2"), MultiUnit(10, "m/s"), MultiUnit(5, "m/s")),
                                                        (Temperature(50, "K"), MultiUnit(50, "K/s"), Unit(1.0, "s")),
                                                        (MultiUnit(1, "m/kg^2"), MultiUnit(1, "m/kg"), Unit(1.0, "kg", -1))
                                                        ])
def test_unit_division(operand1, operand2, expected):
    print(operand1/operand2)
    assert(operand1 / operand2 == expected)

    
    
def test_renolyds():
    d = Length(1, 'm')
    rho = MultiUnit(1.5,"kg/m^3")
    v = MultiUnit(2, "m/s")
    mu = MultiUnit(3, "kg/m*s")
    r = (rho*v*d)/mu
    assert(r == 1.0)

def test_equality():
    mu = MultiUnit(3, "kg/m*s")
    mu2 = MultiUnit(3, "kg/s*m")
    assert(mu == mu2)
    
    
def test_negation_unit():
    u = -Unit(5, "m")
    assert(u._value == -5)
    
def test_negation_multiunit():
    u = -MultiUnit(5, "W/m")
    assert(u._value == -5)
    