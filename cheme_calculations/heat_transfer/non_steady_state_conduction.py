from turtle import left
from cheme_calculations.units.property_units import Area, Density, Cp
from cheme_calculations.units import MultiUnit, Temperature, Length, Time, Volume
from cheme_calculations.units.heat_transfer import HeatTransferCoefficient, ThermalConductivity
from math import erf, exp, pi, sin, sqrt

from cheme_calculations.units.units import Energy

__all__ = ["pseudo_steady_time", "semi_infinite_slab_conduction",
           "lumped_parameter", "finite_slab_conduction", "finite_slab_total_heat"]



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
    
    >>> from cheme_calculations.heat_transfer import pseudo_steady_time
    >>> d = Density(990, "kg/m^3")
    >>> hf = MultiUnit(330, "J/kg")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> T_s = Temperature(323.15, "K")
    >>> T_m = Temperature(273.15, "K")
    >>> lo = Length(.01, "m")
    >>> lf = Length(1, "m")
    >>> time = pseudo_steady_time(d, hf, k, T_s, T_m, lo, lf)
    >>> print(time)
    >>> 5444.4555 s
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
    
    >>> from cheme_calculations.heat_transfer import semi_infinite_slab_conduction
    >>> Ts = Temperature(300, "F")
    >>> To = Temperature(100, "F")
    >>> z = Length(1, "ft")
    >>> time = Time(5, "hr")
    >>> rho = Density(78, "lb/ft^3")
    >>> cp = Cp(1, "BTU/lb*F")
    >>> k = ThermalConductivity(10, "BTU/hr*ft*F")
    >>> T = semi_infinite_slab_conduction(Ts, To, z, time, rho, cp, k)
    >>> print(T)
    >>> 175.42822795740176 F
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
    
    >>> from cheme_calculations.heat_transfer import lumped_parameter
    >>> Tf = Temperature(400, "K")
    >>> To = Temperature(300, "K")
    >>> h = HeatTransferCoefficient(5, "W/m^2*K")
    >>> A = Area(1, "m^2")
    >>> rho = Density(800, "kg/m^3")
    >>> cp = Cp(1, "J/kg*K")
    >>> V = Volume(.5, "m^3")
    >>> time = Time(100, "s")
    >>> T = lumped_parameter(Tf, To, h, A, V, time)
    >>> print(T)
    >>> 371.349520313981 K
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
    :param s: distance to no flux line from surface
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
    
    >>> rho = Density(1050, "kg/m^3")
    >>> cp = Cp(800, "J/kg*K")
    >>> k = ThermalConductivity(1.8, "W/m*K")
    >>> time = Time(180, "s")
    >>> Ts = Temperature(30, "C").convert_to("K")
    >>> To = Temperature(90, "C").convert_to("K")
    >>> s = Length(.04, "m")
    >>> z = Length(.02, "m")
    >>> T = finite_slab_conduction(Ts, To, z, s, k, rho, cp, time, 100).convert_to("C")
    >>> print(T)
    >>> 59.885417513377774 C
    """
    alpha = k/(rho*Cp)
    right_side = 0
    
    
    for n in range(0, iterations+1):
        right_side += (1/(2*n+1))*sin(((2*n+1)*pi*x)/(2*s))*exp(-((2*n+1)*(pi/2))**2*((alpha*time)/s**2))
        
    T = Ts - (Ts-To)*(4/pi)*right_side
    
    return T
        
    
def finite_slab_total_heat(s: Length, rho: Density, cp: Cp, Ts: Temperature,
                           To: Temperature, k: ThermalConductivity, time: Time, area: Area, iterations: int=10)-> Energy:
    """Calculates the total heat that has been transferred through a slab in a given time period.
    Uses an iterative formula.

    :param s: Distance to the no flux line
    :type s: Length
    :param rho: Density of the material
    :type rho: Density
    :param cp: Heat capacity of the material
    :type cp: Cp
    :param Ts: Surface temperature of the thing heating the material
    :type Ts: Temperature
    :param To: Initial temperature of the material at time = 0
    :type To: Temperature
    :param k: Thermal conductivity of the slab
    :type k: ThermalConductivity
    :param time: Time since conduction has started
    :type time: Time
    :param arae: ARea conduction occurred in 
    :type area: Area
    :param iterations: _description_
    :type iterations: int
    :return: _description_
    :rtype: Energy
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import finite_slab_total_heat
    >>> s = Length(1, "m")
    >>> rho = Density(1000, "kg/m^3")
    >>> cp = Cp(4.18, "kJ/kg*K")
    >>> Ts = Temperature(400, "K")
    >>> To = Temperature(300, "K")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> time = Time(300, "s")
    >>> area = Area(1, "m^2")
    >>> ans = finite_slab_total_heat
    >>> print(ans)
    >>> 357477.6685683244 J
    
    
    """
    
    left_side = (8*s*rho*cp*(Ts-To)*area)/(pi**2)
    alpha = k/(rho*cp)
    right_side = 0
    
    for n in range(iterations):
        right_side += (1/(2*n+1)**2)*(1-exp(-((2*n+1)*(pi/2))**2 * ((alpha*time)/s**2)))
        
    return left_side*right_side
    
    
      


    