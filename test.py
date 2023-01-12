from pprint import pprint
from cheme_calculations.heat_transfer import condensation_transfer_coefficient
from cheme_calculations.heat_transfer.heat_transfer_coefficients import htc_cross_sphere
from cheme_calculations.heat_transfer.phase_changes import flux_max_boiling
from cheme_calculations.heat_transfer.radiation import radiative_heat_flow
from cheme_calculations.heat_transfer.steady_state_conduction import planar_flux
from cheme_calculations.units import Temperature, Length, Time, ThermalConductivity, HeatTransferCoefficient
from cheme_calculations.units.mass_transfer import Concentration, DiffusionCoefficient
from cheme_calculations.units.property_units import Density, Cp, DynamicViscosity, Gravity, Hvap, MolecularWeight, Velocity 
from cheme_calculations.units.units import BaseUnit, Force, Mass, MultiUnit, Pressure, Volume, Area

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
mu = MultiUnit(0.0007563, "kg/m*s")
k = ThermalConductivity(0.6, "kW/m*K")


from cheme_calculations.reactions import balance_equation
eq1 = "Al + O2 -> Al2O3"
eq2 = "KI + Pb(NO3)2 -> KNO3 + PbI2"
eq3 = "H3PO4 + (NH4)2MoO4 + HNO3 -> (NH4)3PO4Mo12O36 + NH4NO3 + H2O"
balanced1 = balance_equation(eq1)
balanced2 = balance_equation(eq2)
balanced3 = balance_equation(eq3)
print(balanced1)

print(balanced2)

print(balanced3)
    










