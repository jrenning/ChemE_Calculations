from turtle import left
from cheme_calculations.units.property_units import Area, Density, Cp
from cheme_calculations.units import MultiUnit, Temperature, Length, Time, Volume
from .unit_types import HeatTransferCoefficient, ThermalConductivity
from math import erf, exp, pi, sin, sqrt

__all__ = ["pseudo_steady_time", "semi_infinite_slab_conduction",
           "lumped_parameter", "finite_slab_conduction"]



def pseudo_steady_time(density: MultiUnit, heat_of_vaporization: MultiUnit, k: ThermalConductivity,
                       T_surface: Temperature, T_melt: Temperature, initial_length: Length,
                       final_length: Length)-> Time:
    term1 = (density*heat_of_vaporization)/(k*(T_surface-T_melt))
    term2 = (final_length**2-initial_length**2)/2
    t = term1*term2
    return t


def semi_infinite_slab_conduction(Ts: Temperature, To: Temperature, z: Length,
                       time: Time, rho: Density,
                       Cp: Cp, k: ThermalConductivity)-> Temperature:
    
    alpha = k/(rho*Cp)
    T = Ts - (Ts-To)*erf(z/((4*alpha*time)**(1/2)))
    
    return T

def lumped_parameter(Tf: Temperature, To: Temperature, 
                     h: HeatTransferCoefficient, A: Area,
                     rho: Density, cP: Cp, V: Volume, 
                     time: Time)-> Temperature:
    
    T = Tf-(Tf-To)*exp(-(h*A*time)/(rho*cP*V))
    
    return T

def finite_slab_conduction(Ts: Temperature, To: Temperature, 
                           x: Length, s: Length, k: ThermalConductivity,
                           rho: Density, Cp: Cp, time: Time, iterations: int=3)-> Temperature:
    """Calculates the temperature for a slab after a period of time 
    using an approximation of a finite slab

    :param Ts: surface temperature
    :type Ts: Temperature
    :param To: initial temperature
    :type To: Temperature
    :param x: distance from measuring point to the no flux line
    :type x: Length
    :param s: distance to no flux line from surface_
    :type s: Length
    :param k: Thermal conductivity value 
    :type k: ThermalConductivity
    :param rho: density of the object conduction is occurring in
    :type rho: Density
    :param Cp: heat capacity of the conduction object
    :type Cp: Cp
    :param time: time for conduction
    :type time: Time
    """
    alpha = k/(rho*Cp)
    right_side = 0
    
    
    for n in range(0, iterations+1):
        right_side += (1/(2*n+1))*sin(((2*n+1)*pi*x)/(2*s))*exp(-((2*n+1)*(pi/2))**2*((alpha*time)/s**2))
        
    T = Ts - (Ts-To)*(4/pi)*right_side
    
    return T
        
    
    


    