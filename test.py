from pprint import pprint
from cheme_calculations.heat_transfer import condensation_transfer_coefficient
from cheme_calculations.heat_transfer.heat_transfer_coefficients import htc_cross_sphere
from cheme_calculations.heat_transfer.phase_changes import flux_max_boiling
from cheme_calculations.heat_transfer.radiation import radiative_heat_flow
from cheme_calculations.heat_transfer.steady_state_conduction import planar_flux
from cheme_calculations.units import Temperature, Length, Time, ThermalConductivity, HeatTransferCoefficient
from cheme_calculations.units.fluids import VolumetricFlowrate
from cheme_calculations.units.mass_transfer import Concentration, DiffusionCoefficient, MassFlowRate
from cheme_calculations.units.property_units import Density, Cp, DynamicViscosity, Gravity, Hvap, MolecularWeight, Velocity 
from cheme_calculations.units.units import BaseUnit, Force, Mass, MultiUnit, Pressure, Volume, Area

from cheme_calculations.thermodynamics.cubic_equations import peng_robinson, rendlich_kwong, soave_rendlich_kwong, van_der_waals

from cheme_calculations.process_safety import max_vessel_pressure
from cheme_calculations.utility.get_chemical_properties import get_water_properties



from cheme_calculations.process_safety import enclosure_concentration, ppm_to_other
from cheme_calculations.utility import get_gas_constant
M = MolecularWeight(65, "g/mol")
Qm = MassFlowRate(.7, "g/s")
Rg = get_gas_constant("K", "m^3", "Pa")
T = Temperature(300, "K")
k = 0.35
Qv = VolumetricFlowrate(5, "m^3/s")
P = Pressure(1, "atm").convert_to("Pa")

cppm = enclosure_concentration(Qm, Rg, T, k, Qv, P, M)
print(cppm)
# 1514.820930364972

# convert to another concentration
C = ppm_to_other(cppm, Rg, T, P, M)
print(C)
# 0.4 g / m³
    










