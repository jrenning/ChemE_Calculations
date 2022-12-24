from pprint import pprint
from cheme_calculations.heat_transfer import condensation_transfer_coefficient, ThermalConductivity, HeatTransferCoefficient
from cheme_calculations.heat_transfer.phase_changes import flux_max_boiling
from cheme_calculations.heat_transfer.steady_state_conduction import planar_flux
from cheme_calculations.heat_transfer.unit_types import HeatFlux, Power
from cheme_calculations.units import Temperature, Length, Time
from cheme_calculations.units.property_units import Density, Cp, Area, DynamicViscosity, Gravity, Hvap, Velocity 
from cheme_calculations.units.units import BaseUnit, Mass, MultiUnit, Pressure, Volume

from cheme_calculations.thermodynamics.cubic_equations import peng_robinson, rendlich_kwong, soave_rendlich_kwong, van_der_waals

from cheme_calculations.process_safety import max_vessel_pressure
from cheme_calculations.utility.get_chemical_properties import get_water_properties


k = ThermalConductivity(0.6, "kW/m*K")
T1 = Temperature(10, 'K')
T2 = Temperature(100, 'K')
thickness = Length(.2, "m")
length = Length(5, "m")
t = Time(5, "s")
d = Density(994.7, "kg/m^3")
cp = Cp(50, "J/kg*K")
h = HeatTransferCoefficient(1, "W/m^2*K")
A = Area(15, "m^2")
V = Volume(5, "m^3")
x = Length(0.04, "m")
s = Length(1, "m")
g = Gravity(9.81, "m/s^2")
hvap = Hvap(2250000, "J/kg")

# ans = semi_infinite_slab(T2, T1, length, t, d, cp, k)
# ans = lumped_parameter(T2, T1, h, A, d, cp, 
#                        V, t)

# ans = finite_slab_conduction(T2, T1, x, s, k, d, cp, t, 3)


mu = MultiUnit(0.0007563, "kg/m*s")
k = ThermalConductivity(0.6, "kW/m*K")

# ans = flux_max_boiling(hvap, Density(0.623, "kg/m^3"), Density(957.7, "kg/m^3"), 
#                        MultiUnit(.058, "kg/s^2"), g)


# mat_strength = Pressure(85000, "psi")
# wall_thickness = Length(1.9E-3, "m")
# radius = Length(1.25, "m")


# ans = max_vessel_pressure(mat_strength, wall_thickness, 
#                           radius, "sphere")

# j = MultiUnit(1, "J^2/s^2")
# j2 = MultiUnit(1, "J/s")

# d = Length(1, 'm')
# rho = MultiUnit(1.5,"kg/m^3")
# v = MultiUnit(2, "m/s")
# mu = MultiUnit(3, "kg/m*s")
# r = (rho*v*d)/mu

#ans = planar_flux(k, T1, T2, x)

w = get_water_properties(275)

print(w._density)











