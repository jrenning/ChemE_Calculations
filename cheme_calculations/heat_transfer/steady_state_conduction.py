
from .unit_types import Power, ThermalConductivity, HeatFlux
from cheme_calculations.units import Temperature, Length
from cheme_calculations.units.property_units import Area
from cheme_calculations.utility import solvable_for
from math import pi
from typing import Union
import math

__all__ = ["planar_heat", "planar_flux", "pipe_heat", "sphere_heat"]

@solvable_for(solvable=["q", "T1", "T2", "thickness"])
def planar_heat(k: ThermalConductivity, T1: Union[Temperature, None], T2: Union[Temperature, None],
                A: Area, thickness: Union[Length, None], q: Power = None, **kwargs)-> Union[Power, Temperature, Length]:
    
    solving_for = kwargs["solving_for"]
    
    
    if solving_for == "q":
        q = -k * A*((T2-T1)/thickness)
        return q
    if solving_for == "thickness":
        thickness = (-k*A*(T2-T1))/q
        return thickness
    if solving_for == "T2":
        T2 = ((thickness*q)/(-k * A)) + T1
        return T2
    if solving_for == "T1":
        T1 = -((thickness*q)/(-k * A)) + T2
        return T1
    
@solvable_for(solvable=["q", "T1", "T2", "thickness"])
def planar_flux(k: ThermalConductivity, T1: Union[Temperature, None], T2: Union[Temperature, None],
                thickness: Union[Length, None], q: HeatFlux = None, **kwargs)-> Union[HeatFlux, Temperature, Length]:
    
    solving_for = kwargs["solving_for"]
    
    if solving_for == "q":
        q = -k * ((T2-T1)/thickness)
        return q
    if solving_for == "thickness":
        thickness = (-k*(T2-T1))/q
        return thickness
    if solving_for == "T2":
        T2 = ((thickness*q)/(-k)) + T1
        return T2
    if solving_for == "T1":
        T1 = -((thickness*q)/(-k)) + T2
        return T1

def pipe_heat(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                length: Length, thickness: Length)-> HeatFlux:
    
    q = -2*pi*length*k*((T2-T1)/(math.log(thickness._value)))
    return q

def sphere_heat(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                outer_radius: Length, inner_radius: Length):
    q = -4*pi*inner_radius*outer_radius*((T2-T1)/(outer_radius-inner_radius))
    return q


    