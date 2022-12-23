from cheme_calculations.units import Mass, Length, MultiUnit, Time
from typing import Literal
from math import exp, pi

__all__ = ["three_d_pulse_decay"]

def three_d_pulse_decay(initial_mass: Mass, distance: Length, diffusion_coefficient: MultiUnit,
                        time: Time, shape: Literal["cube", "hemisphere"]):
    if shape == "hemisphere":
        initial_mass = 2 * initial_mass
    elif shape == "cube":
        initial_mass = 8 * initial_mass
        
    top = initial_mass * exp((-distance**2)/(4*diffusion_coefficient*time))
    bottom = (diffusion_coefficient*time)**(3/2)
    
    C = top/bottom
    
    return C

