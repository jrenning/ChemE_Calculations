
from cheme_calculations.units.heat_transfer import ThermalConductivity, Power, HeatFlux
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
    """Function to solve the heat flow through a planar surface at steady state
    
    .. math:: q = -k * A * \dfrac{T2-T1}{thickness}
    
    Can solve for other parameters as long as there is only one unknown
    
    Supply [k, T1, T2, A, thickness] -> q (Power) \n
    Supply [k, T1, T2, A, q] -> thickness (Length) \n
    Supply [k, T2, A, thickness, q] -> T1 (Temperature) \n
    Supply [k, T1, A, thickness, q] -> T2 (Temperature) \n
    

    :param k: Thermal conductivity of the planar surface
    :type k: ThermalConductivity
    :param T1: Temperature on side heat flow starts from 
    :type T1: Union[Temperature, None]
    :param T2: Temperature on the side heat flow goes to
    :type T2: Union[Temperature, None]
    :param A: Area of the surface
    :type A: Area
    :param thickness: Thickness of the surface
    :type thickness: Union[Length, None]
    :param q: The heat flow through the surface, defaults to None
    :type q: Power, optional
    :return: See chart above
    :rtype: Union[Power, Temperature, Length]
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import planar_heat
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> T1 = Temperature(500, "K")
    >>> T2 = Temperature(300, "K")
    >>> A = Area(15, "m^2")
    >>> thickness = Length(1, "m")
    >>> q = planar_heat(k, T1, T2, A, thickness)
    >>> print(q)
    >>> 1800 W
    >>> thickness = planar_heat(k, T1, T2, A,None,q)
    >>> print(thickness)
    >>> 1.0 m
    
    """
    
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
    
@solvable_for(solvable=["qA", "T1", "T2", "thickness"])
def planar_flux(k: ThermalConductivity, T1: Union[Temperature, None], T2: Union[Temperature, None],
                thickness: Union[Length, None], qA: HeatFlux = None, **kwargs)-> Union[HeatFlux, Temperature, Length]:
    """Function to solve the heat flux through a planar surface at steady state
    
    Can solve for other parameters as long as there is only one unknown
    
    .. math:: \dfrac{q}{A} = -k* \dfrac{T2-T1}{thickness}
    
    Supply [k, T1, T2, thickness] -> qA (HeatFlux) \n
    Supply [k, T1, T2, qA] -> thickness (Length) \n
    Supply [k, T2, thickness, qA] -> T1 (Temperature) \n
    Supply [k, T1, thickness, qA] -> T2 (Temperature) \n
    

    :param k: Thermal conductivity of the planar surface
    :type k: ThermalConductivity
    :param T1: Temperature on side heat flow starts from 
    :type T1: Union[Temperature, None]
    :param T2: Temperature on the side heat flow goes to
    :type T2: Union[Temperature, None]
    :param A: Area of the surface
    :type A: Area
    :param thickness: Thickness of the surface
    :type thickness: Union[Length, None]
    :param q: The heat flow through the surface, defaults to None
    :type q: Power, optional
    :return: See chart above
    :rtype: Union[Power, Temperature, Length]
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import planar_flux
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> T1 = Temperature(500, "K")
    >>> T2 = Temperature(300, "K")
    >>> thickness = Length(1, "m")
    >>> qA = planar_heat(k, T1, T2, thickness)
    >>> print(qA)
    >>> 120.0 W / m²
    >>> thickness = planar_heat(k, T1, T2, None,qA)
    >>> print(thickness)
    >>> 1.0 m
    
    """
    
    solving_for = kwargs["solving_for"]
    
    if solving_for == "qA":
        qA = -k * ((T2-T1)/thickness)
        return qA
    if solving_for == "thickness":
        thickness = (-k*(T2-T1))/qA
        return thickness
    if solving_for == "T2":
        T2 = ((thickness*qA)/(-k)) + T1
        return T2
    if solving_for == "T1":
        T1 = -((thickness*qA)/(-k)) + T2
        return T1

def pipe_heat(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                length: Length, r2: Length, r1: Length)-> Power:
    """Calculates the heat transfer through a pipe at steady state
    
    .. math:: q = -2*\pi*L*k* \dfrac{T2-T1}{ln(\dfrac{r_2}{r_1})}

    :param k: Thermal conductivity of the pipe
    :type k: ThermalConductivity
    :param T1: Temperature the heat is coming from
    :type T1: Temperature
    :param T2: Temperature the heat is going to 
    :type T2: Temperature
    :param length: Length of the pipe
    :type length: Length
    :param r2: Outer radius of the pipe
    :type r2: Length
    :param r1: Inner radius of the pipe
    :type r1: Length
    :return: Heat transfer through the pipe
    :rtype: Power
    
    :Example:
    
    >>>
    """
    
    q = -2*pi*length*k*((T2-T1)/(math.log(r2/r1)))
    return q

def sphere_heat(k: ThermalConductivity, T1: Temperature, T2: Temperature,
                outer_radius: Length, inner_radius: Length)-> Power:
    """Calculates the heat transfer through a sphere at steady state

    :param k: Thermal conductivity of the material
    :type k: ThermalConductivity
    :param T1: Temperature the heat is flowing from
    :type T1: Temperature
    :param T2: Temperature the heat is flowing to
    :type T2: Temperature
    :param outer_radius: Outer radius of the sphere
    :type outer_radius: Length
    :param inner_radius: Inner radius of the sphere
    :type inner_radius: Length
    :return: The heat transfer through the sphere
    :rtype: Power
    
    :Example:
    
    >>>
    """
    q = -4*pi*inner_radius*outer_radius*((T2-T1)/(outer_radius-inner_radius))
    return q


    