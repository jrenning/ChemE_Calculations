from .unit_types import ThermalConductivity, HeatFlux
from cheme_calculations.units import Temperature, Length
from cheme_calculations.units.property_units import Area
from cheme_calculations.utility import solvable_for
from math import pi
import math



@solvable_for(solvable=["T1", "T2", "thickness", "q"])
def planar_flux(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                A: Area,
                thickness: Length)-> HeatFlux:
    
    q = -k * A*((T2-T1)/thickness)
    return q

def pipe_flux(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                length: Length, thickness: Length)-> HeatFlux:
    
    q = -2*pi*length*k*((T2-T1)/(math.log(thickness._value)))
    return q

def sphere_flux(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                outer_radius: Length, inner_radius: Length):
    q = -4*pi*inner_radius*outer_radius*((T2-T1)/(outer_radius-inner_radius))
    return q


    