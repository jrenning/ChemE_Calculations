from cheme_calculations.units import Area, Temperature
from cheme_calculations.units.heat_transfer import Power
from cheme_calculations.utility.constants import RADIATION_CONSTANT

__all__ = ["radiative_heat_flow"]

def radiative_heat_flow(area: Area, view_factor: float, T1: Temperature, T2: Temperature)-> Power:
    """Calculates the heat flow from oen object to another due to radiation 

    :param area: Area of the radiating object
    :type area: Area
    :param view_factor: The view factor of the radiating object to the other object
    :type view_factor: float
    :param T1: The temperature of the radiating object
    :type T1: Temperature
    :param T2: The temperature of the other object
    :type T2: Temperature
    :return: The heat flow due to radiation to the other object
    :rtype: Power
    """
    val = RADIATION_CONSTANT*area*view_factor*(T1**4-T2**4)
    return Power(val._value, "W")

