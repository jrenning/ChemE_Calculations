from units import Temperature


def test_temperature_float_addition():
    T = Temperature(350,'K')
    T = T + 50
    assert(T._value == 400)
    assert(T.__repr__() == "400 K")

def test_temperature_float_multiplication():
    T = Temperature(350,'K')
    T = T * 2
    assert(T._value == 700)
    assert(T.__repr__() == "700 K")

def test_temperature_float_division():
    T = Temperature(350,'K')
    T = T / 2
    assert(T._value == 175)
    assert(T.__repr__() == "175.0 K")

def test_temperature_temperature_addition():
    T = Temperature(350,'K')
    T2 = T = Temperature(350,'K')
    T3 = T + T2
    assert(T3._value == 700)
    assert(T3.__repr__() == "700 K")
def test_temperature_temperature_subtraction():
    T = Temperature(350,'K')
    T2 = Temperature(150,'K')
    T3 = T - T2
    assert(T3._value == 200)
    assert(T3.__repr__() == "200 K")
def test_temperature_temperature_multiplication():
    T = Temperature(350,'K')
    T2 = Temperature(1,'K')
    T3 = T * T2
    assert(T3._value == 350)
    assert(T3.__repr__() == "350 K^2")
def test_temperature_temperature_division():
    T = Temperature(350,'K')
    T2 = Temperature(50,'K')
    T3 = T / T2
    assert(T3 == 7.0)
    
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