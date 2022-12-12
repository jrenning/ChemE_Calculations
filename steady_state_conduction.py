from heat_transfer_coefficients import ThermalConductivity
from units import Temperature, Length, MultiUnit, BaseUnit
from property_units import Area
from typing import List
from math import pi
import math


class HeatFlux(MultiUnit):
    def __init__(self,value:float, unit: str="", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super().__init__(value, top_half=top_half, bottom_half=bottom_half)
        else:
            super().__init__(value, unit)
            
class Power(MultiUnit):
    pass

def planar_flux(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                A: Area,
                thickness: Length)-> HeatFlux:
    
    q = -k * A*((T2-T1)/thickness)
    return q

def pipe_flux(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                length: Length, thickness: Length)-> HeatFlux:
    
    print(length*k)
    
    q = -2*pi*length*k*((T2-T1)/(math.log(thickness._value)))
    return q

def sphere_flux(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                outer_radius: Length, inner_radius: Length):
    q = -4*pi*inner_radius*outer_radius*((T2-T1)/(outer_radius-inner_radius))
    return q

if __name__ == "__main__":
    
    
    k = ThermalConductivity(0.5, "W/m*K")
    length = Length(8, "m")
    A = Area(200,"m^2")
    T2 = Temperature(400, "K")
    T1 = Temperature(350, "K")
    thickness = Length(0.5, "m")
    
    
    
    q = planar_flux(k, T1, T2,A, thickness)
    q2 = pipe_flux(k, T1, T2, length, thickness)
    
    print(q2)
    