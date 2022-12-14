from cheme_calculations.heat_transfer import condensation_transfer_coefficient, ThermalConductivity, HeatTransferCoefficient
from cheme_calculations.units import Temperature, Length, Time
from cheme_calculations.units.property_units import Density, Cp, Area, DynamicViscosity, Gravity, Hvap, Volume


k = ThermalConductivity(0.06, "W/m*K")
T1 = Temperature(200, 'K')
T2 = Temperature(300, 'K')
thickness = Length(.2, "m")
length = Length(5, "m")
t = Time(5, "s")
d = Density(800, "kg/m^3")
cp = Cp(50, "J/kg*K")
h = HeatTransferCoefficient(1, "W/m^2*K")
A = Area(15, "m^2")
V = Volume(5, "m^3")
x = Length(0.5, "m")
s = Length(1, "m")
g = Gravity(9.81, "m/s^2")
mu = DynamicViscosity(0.01, "kg/m*s")
hvap = Hvap(2000, "J/kg")

# ans = semi_infinite_slab(T2, T1, length, t, d, cp, k)
# ans = lumped_parameter(T2, T1, h, A, d, cp, 
#                        V, t)

# ans = finite_slab_conduction(T2, T1, x, s, k, d, cp, t, 3)

ans = condensation_transfer_coefficient(k, d, g, hvap, 4, T2, T1, x, mu)

print(ans)










