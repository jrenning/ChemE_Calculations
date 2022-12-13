from cheme_calculations.heat_transfer import pipe_flux, ThermalConductivity
from cheme_calculations.units import Temperature, Length


k = ThermalConductivity(0.6, "W/m*K")
T1 = Temperature(400, 'K')
T2 = Temperature(600, 'K')
thickness = Length(.2, "m")
length = Length(5, "m")
ans = pipe_flux(k, T1, T2, length, thickness)

print(ans)
