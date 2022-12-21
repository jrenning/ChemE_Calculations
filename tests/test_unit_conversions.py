from cheme_calculations.units import Temperature
from cheme_calculations.units.property_units import Density, DynamicViscosity, Velocity
from cheme_calculations.units.units import MultiUnit, Pressure, Unit, Volume
import pytest
from pytest import approx

@pytest.mark.parametrize("unit1,unit2,expected", [(Velocity(3, 'm/s'),"cm/s",Velocity(300.0, 'cm/s')),
                                                        (DynamicViscosity(1, 'cP'), "kg/s*m", DynamicViscosity(1/1000, 'kg/m*s')),
                                                        (MultiUnit(5, "m^3"), "cm^3", MultiUnit(approx(5E6), "cm^3")),
                                                        (MultiUnit(1, "W/m^2*K"), "BTU/hr*ft^2*F", MultiUnit(approx(.17611), "BTU/hr*ft^2*F")),
                                                        (MultiUnit(1, "g/cm*s"), "kg/m*s", MultiUnit(.1, "kg/m*s")),
                                                        (MultiUnit(1, "W/m*K"), "BTU/hr*ft*F", MultiUnit(approx(0.5777892), "BTU/hr*ft*F")),
                                                        (Density(1, "g/cm^3"), "kg/m^3", Density(approx(1000.0), "kg/m^3")),
                                                        (DynamicViscosity(1, "g/cm*s"), "kg/s*m", DynamicViscosity(approx(.1), "kg/s*m")),
                                                        (MultiUnit(1000, "L/s"), "m^3/s", MultiUnit(approx(1), "m^3/s")),
                                                        (MultiUnit(1, "L/s"), "cm^3/s", MultiUnit(approx(1000), "cm^3/s"))
                                                        ])
def test_multi_unit_conversion(unit1, unit2, expected):
    a = unit1.convert_to(unit2)
    print(a.__class__)
    print(expected)
    assert(a == expected)
    
@pytest.mark.parametrize("unit1,unit2,expected", [(Temperature(300, 'C'), "K", Temperature(573.15, "K")),
                                                        (Temperature(300, "C"), "F", Temperature(572, "F")),
                                                        (Temperature(350, "C"), "R", Temperature(1121.67, "R")),
                                                        (Temperature(300, "F"), "K", Temperature(approx(422.039), "K")),
                                                        (Temperature(300, 'F'), "C", Temperature(approx(148.889), "C")),
                                                        (Temperature(350, "F"), "R", Temperature(approx(809.67), "R")),
                                                        (Temperature(350, "K"), "C", Temperature(350-273.15, "C")),
                                                        (Temperature(350, "K"), "F", Temperature(approx(170.33), "F")),
                                                        (Temperature(350, "K"), "R", Temperature(630, "R")),
                                                        (Temperature(350, "R"), "C", Temperature(approx(-78.7056), "C")),
                                                        (Temperature(350, "R"), "F", Temperature(approx(-109.67), "F")),
                                                        (Temperature(350, "R"), "K", Temperature(approx(194.444, rel=1E-3), "K")),
                                                        (Temperature(350, "K", 2), "K^2", Temperature(350, "K", 2)),
                                                        (Temperature(275.15, "K", 2), "C^2", Temperature(4.0, "C", 2))
                                                        ])
def test_temperature_conversions(unit1, unit2, expected):
    a = unit1.convert_to(unit2)
    assert(a == expected)
    
@pytest.mark.parametrize("unit1,unit2,expected", [(Pressure(1, "atm"), "Pa", Pressure(101325, "Pa")),
                                                  (Pressure(1, "atm"), "bar", Pressure(1.01325, "bar")),
                                                  (Pressure(1, "atm"), "kPa", Pressure(101.325, "kPa")),
                                                  (Pressure(1, "atm"), "mmHg", Pressure(approx(760.002), "mmHg")),
                                                  (Pressure(1, "atm"), "psi", Pressure(approx(14.69594), "psi")),
                                                  (Pressure(101325, "Pa"), "atm", Pressure(1, "atm")),
                                                  (Pressure(101.325, "kPa"), "atm", Pressure(1, "atm")),
                                                  (Pressure(1.01325, "bar"), "atm", Pressure(approx(1), "atm")),
                                                  (Pressure(760, "mmHg"), "atm", Pressure(approx(1, rel=1E-3), "atm")),
                                                  (Pressure(14.696, "psi"), "atm", Pressure(approx(1, rel=1E-3), "atm")),
                                                  ])
def test_pressure_conversions(unit1, unit2, expected):
    a = unit1.convert_to(unit2)
    assert(a == expected)