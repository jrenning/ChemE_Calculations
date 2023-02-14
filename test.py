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


from cheme_calculations.reactions import integral_method


time_data = [0, 10, 20, 30, 40]
reaction_data = [0.624, 0.446, 0.318, 0.224, 0.164]
ans = integral_method(time_data, reaction_data, (0, 4, .5))
print(ans)










