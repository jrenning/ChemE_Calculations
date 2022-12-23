from turtle import left
from cheme_calculations.units.property_units import Area, Density, Cp
from cheme_calculations.units import MultiUnit, Temperature, Length, Time, Volume
from .unit_types import HeatTransferCoefficient, ThermalConductivity
from math import erf, exp, pi, sin, sqrt

__all__ = ["pseudo_steady_time", "semi_infinite_slab_conduction",
           "lumped_parameter", "finite_slab_conduction"]



def pseudo_steady_time(density: Density, heat_of_fusion: MultiUnit, k: ThermalConductivity,
                       T_surface: Temperature, T_melt: Temperature, initial_length: Length,
                       final_length: Length)-> Time:
    """Calculates the time needed to melt a section of material based on the pseudo steady state assumptions

    Makes assumption that all the heat is going towards melting the material and none towards heating the already melted stuff
    Makes assumption that the melting is happening in a planar system
    
    :param density: Density of the melted material
    :type density: Density
    :param heat_of_fusion: Heat of fusion
    :type heat_of_fusion: MultiUnit
    :param k: The thermal conductivity of the melted material
    :type k: ThermalConductivity
    :param T_surface: Temperature of the surface doing the melting
    :type T_surface: Temperature
    :param T_melt: Melting point of the material
    :type T_melt: Temperature
    :param initial_length: Initial thickness of the melted material layer
    :type initial_length: Length
    :param final_length: ending thickness of the melted material layer
    :type final_length: Length
    :return: _Time to get from initial to end thickness
    :rtype: Time
    
    :Example:
    
    >>> 
    """
    term1 = (density*heat_of_fusion)/(k*(T_surface-T_melt))
    term2 = (final_length**2-initial_length**2)/2
    t = term1*term2
    return t


def semi_infinite_slab_conduction(Ts: Temperature, To: Temperature, z: Length,
                       time: Time, rho: Density,
                       Cp: Cp, k: ThermalConductivity)-> Temperature:
    """Calculates the temperature of a slab at a given time with a semi-infinite assumption

    :param Ts: Surface temperature
    :type Ts: Temperature
    :param To: Initial temperature of the material
    :type To: Temperature
    :param z: Distance to measuring point from the surface
    :type z: Length
    :param time: Time since surface was heated to Ts
    :type time: Time
    :param rho: Density of the material
    :type rho: Density
    :param Cp: Heat capacity of the material
    :type Cp: Cp
    :param k: Thermal conductivity of the material
    :type k: ThermalConductivity
    :return: The temperature at distance z into the planar slab
    :rtype: Temperature
    
    :Example:
    
    >>> 
    """
    
    alpha = k/(rho*Cp)
    T = Ts - (Ts-To)*erf(z/((4*alpha*time)**(1/2)))
    
    return T

def lumped_parameter(Tf: Temperature, To: Temperature, 
                     h: HeatTransferCoefficient, A: Area,
                     rho: Density, cP: Cp, V: Volume, 
                     time: Time)-> Temperature:
    """Calculates the temperature of a slab after a given period of time 
    
    NOTE: only for use with low biot numbers (~0.1 or lower) \n
    Assumption: neglects the conductive resistance of the material
    
    :param Tf: Temperature of the fluid around the material
    :type Tf: Temperature
    :param To: Initial temperature
    :type To: Temperature
    :param h: Heat transfer coefficient of the fluid heating the object 
    :type h: HeatTransferCoefficient
    :param A: Area of the surface
    :type A: Area
    :param rho: Density of the material
    :type rho: Density
    :param cP: Heat capacity of the material
    :type cP: Cp
    :param V: Volume of the object
    :type V: Volume
    :param time: Time the heat transfer has been happening
    :type time: Time
    :return: Final temperature of the material
    :rtype: Temperature
    
    :Example:
    
    >>>
    """
    
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
    
    :Example:
    
    >>> 
    """
    alpha = k/(rho*Cp)
    right_side = 0
    
    
    for n in range(0, iterations+1):
        right_side += (1/(2*n+1))*sin(((2*n+1)*pi*x)/(2*s))*exp(-((2*n+1)*(pi/2))**2*((alpha*time)/s**2))
        
    T = Ts - (Ts-To)*(4/pi)*right_side
    
    return T
        
    
    


    