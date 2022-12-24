from math import exp, pi, sin
from cheme_calculations.heat_transfer.non_steady_state_conduction import lumped_parameter
from cheme_calculations.units.units import Length, MultiUnit, Temperature, Time, Volume
import pytest
from cheme_calculations.units.property_units import Area, Cp, Density
from cheme_calculations.heat_transfer.unit_types import HeatTransferCoefficient, ThermalConductivity
from cheme_calculations.heat_transfer import finite_slab_conduction
from pytest import approx

def test_planar_finite_conduction():
    rho = Density(1050, "kg/m^3")
    cp = Cp(800, "J/kg*K")
    k = ThermalConductivity(1.8, "W/m*K")
    time = Time(180, "s")
    Ts = Temperature(30, "C").convert_to("K")
    To = Temperature(90, "C").convert_to("K")
    s = Length(.04, "m")
    z = Length(.02, "m")
    
    T = finite_slab_conduction(Ts, To, z, s, k, rho, cp, time, 100).convert_to("C")
    
    assert(T == Temperature(approx(59.9, rel=0.1), "C"))
    
def test_lumped_parameter():
    
    h = HeatTransferCoefficient(5, "W/m^2*K")
    time = Time(100, "s")
    s = Length(0.002, "m")
    Tf = Temperature(102, "C").convert_to("K")
    To = Temperature(20, "C").convert_to("K")
    A = Area(1, "m^2")
    V = Volume(.002, "m^3")
    k = ThermalConductivity(0.138, "W/m*K")
    alpha = MultiUnit(0.000345, "m^2/hr").convert_to("m^2/s")
    rho = Density(600, "kg/m^3")
    rho_cp = k/alpha
    cp = rho_cp/rho
    
    T = lumped_parameter(Tf, To, h, A, rho, cp, V, time).convert_to("C")
    
    assert(T == Temperature(approx(33.2, rel=0.2), "C"))
    