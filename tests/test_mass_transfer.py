from cheme_calculations.units import Temperature, DynamicViscosity, Length
from cheme_calculations.mass_transfer import stokes_einstein
from cheme_calculations.units.units import MultiUnit
from pytest import approx

def test_stokes_einstein():
    T = Temperature(298, "K")
    mu_b = DynamicViscosity(8.91E-3, "g/cm*s").convert_to("kg/m*s")
    R_a = Length(3.56E-7, "cm").convert_to("m")
    ans = stokes_einstein(T, mu_b, R_a)
    assert(ans == MultiUnit(approx(6.89E-11), "m^2/s"))