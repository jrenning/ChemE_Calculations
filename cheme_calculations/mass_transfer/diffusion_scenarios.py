from cheme_calculations.units import Mass, Length, MultiUnit, Time
from typing import Literal
from math import exp, pi

from cheme_calculations.units.mass_transfer import DiffusionCoefficient

__all__ = ["three_d_pulse_decay"]

def three_d_pulse_decay(initial_mass: Mass, distance: Length, diffusion_coefficient: DiffusionCoefficient,
                        time: Time, shape: Literal["cube", "hemisphere"])-> MultiUnit:
    """Calculates the concentration at a certain point away from a point source of concentration. 
    This function does so in a 3D manner where the stuff can diffuse in all directions

    :param initial_mass: Initial mass of the point source multiplied by the number of dimensions it can diffuse ie 2 for hemisphere, 8 for a cube
    :type initial_mass: Mass
    :param distance: Distance away from the point source
    :type distance: Length
    :param diffusion_coefficient: Diffusion coefficient of the point source material in the current medium
    :type diffusion_coefficient: MultiUnit
    :param time: Time after point source was added
    :type time: Time
    :param shape: Shape of dispersion ie where can the point source go
    :type shape: Literal[&quot;cube&quot;, &quot;hemisphere&quot;]
    :return: Concentration at the given point
    :rtype: MultiUnit
    """
    if shape == "hemisphere":
        initial_mass = 2 * initial_mass
    elif shape == "cube":
        initial_mass = 8 * initial_mass
        
    top = initial_mass * exp((-distance**2)/(4*diffusion_coefficient*time))
    bottom = (diffusion_coefficient*time)**(3/2)
    
    C = top/bottom
    
    return C

