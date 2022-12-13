from cheme_calculations.units.property_units import Density
from cheme_calculations.units import MultiUnit, Temperature, Length, Time
from .unit_types import ThermalConductivity

def pseudo_steady_time(density: MultiUnit, heat_of_vaporization: MultiUnit, k: ThermalConductivity,
                       T_surface: Temperature, T_melt: Temperature, initial_length: Length,
                       final_length: Length):
    term1 = (density*heat_of_vaporization)/(k*(T_surface-T_melt))
    term2 = (final_length**2-initial_length**2)/2


def semi_infinite_slab(Ts: Temperature, To: Temperature, z: Length,
                       time: Time, thermal_diffusivity: MultiUnit):
    pass


    