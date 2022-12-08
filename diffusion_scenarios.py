from units import Mass, BaseLength, MultiUnit, Time
from typing import Literal
from math import exp, pi

def three_d_pulse_decay(initial_mass: Mass, distance: BaseLength, diffusion_coefficient: MultiUnit,
                        time: Time, shape: Literal["cube", "hemisphere"]):
    if shape == "hemisphere":
        initial_mass = 2 * initial_mass
    elif shape == "cube":
        initial_mass = 8 * initial_mass
        
    top = initial_mass * exp((-distance**2)/(4*diffusion_coefficient*time))
    bottom = (diffusion_coefficient*time)**(3/2)
    
    C = top/bottom
    
    return C

if __name__ == "__main__":
    ans = three_d_pulse_decay(Mass(5000, "kg"), BaseLength(50, "m"),
                              MultiUnit(1E-1,"m^2/s"),Time(120, "s"), "cube")
    print(ans)