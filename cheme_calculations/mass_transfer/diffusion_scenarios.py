from cheme_calculations.units import Mass, Length, MultiUnit, Time
from typing import Literal
from math import exp, pi

from cheme_calculations.units.mass_transfer import Concentration, DiffusionCoefficient
from cheme_calculations.units.property_units import Area

__all__ = ["three_d_pulse_decay", "two_d_pulse_decay", "one_d_pulse_decay"]

def three_d_pulse_decay(initial_mass: Mass, distance: Length, D: DiffusionCoefficient,
                        time: Time, shape: Literal["cube", "hemisphere"])-> Concentration:
    """Calculates the concentration at a certain point away from a point source of concentration. 
    This function does so in a 3D manner where the stuff can diffuse in all directions
    
    .. math:: C = \dfrac{m_o e^{\dfrac{-r^2}{4Dt}}}{(4 \pi Dt)^{3/2}}

    :param initial_mass: Initial mass of the point source multiplied by the number of dimensions it can diffuse ie 2 for hemisphere, 8 for a cube
    :type initial_mass: Mass
    :param distance: Distance away from the point source
    :type distance: Length
    :param D: Diffusion coefficient of the point source material in the current medium
    :type D: DiffusionCoefficient
    :param time: Time after point source was added
    :type time: Time
    :param shape: Shape of dispersion ie where can the point source go
    :type shape: Literal[&quot;cube&quot;, &quot;hemisphere&quot;]
    :return: Concentration at the given point
    :rtype: Concentration
    
    >>> from cheme_calculations.mass_transfer import three_d_pulse_decay
    >>> mo = Mass(2000, "kg")
    >>> distance = Length(50, "m")
    >>> D = DiffusionCoefficient(3E-3, "cm^2/s")
    >>> time = Time(30000, "s")
    >>> ans = three_d_pulse_decay(mo, distance, D, time, "cube")
    >>> print(ans)
    >>> 0.0004055155574020115 kg / m³
    """
    if shape == "hemisphere":
        initial_mass = 2 * initial_mass
    elif shape == "cube":
        initial_mass = 8 * initial_mass
        
    top = initial_mass * exp((-distance**2)/(4*D*time))
    bottom = (4*pi*D*time)**(3/2)
    
    C = top/bottom
    
    return C


def two_d_pulse_decay(initial_mass: Mass, L: Length, distance: Length, D: DiffusionCoefficient,
                        time: Time)-> Concentration:
    """Calculates the concentration at a given point after a pulse of concentration has been released after
    a certain period of time. This model is for two-dimensional scenarios where mass can diffuse 
    in two dimensions.
    
    .. math:: C = \dfrac{m_o e^{\dfrac{-r^2}{4Dt}}}{(4 \pi Dt)}

    :param initial_mass: The initial mass released
    :type initial_mass: Mass
    :param L: The length the release occurred on
    :type L: Length
    :param distance: Distance away to measuring point
    :type distance: Length
    :param D: Diffusion coefficient of the released material in the medium
    :type D: DiffusionCoefficient
    :param time: Time after release
    :type time: Time
    :return: The concentration at point z after time t
    :rtype: MultiUnit
    
    :Example:
    
    >>> from cheme_calculations.mass_transfer import two_d_pulse_decay
    >>> mo = Mass(2000, "kg")
    >>> L = Length(1, "m")
    >>> distance = Length(50, "m")
    >>> D = DiffusionCoefficient(3E-3, "cm^2/s")
    >>> time = Time(30000, "s")
    >>> ans = two_d_pulse_decay(mo, L, distance, D, time)
    >>> print(ans)
    >>> 0.0017046833530132385 kg / m³
    """
    
    initial_mass = initial_mass/L
    
    top = initial_mass * exp((-distance**2)/(4*D*time))
    bottom = (4*pi*D*time)
    
    C = top/bottom
    
    return C


def one_d_pulse_decay(initial_mass: Mass, area: Area, distance: Length, D: DiffusionCoefficient,
                        time: Time)-> Concentration:
    
    """Calculates the concentration at a given point after a pulse of concentration has been released after
    a certain period of time. This model is for one-dimensional scenarios where mass can diffuse 
    in one dimension.
    
    .. math:: C = \dfrac{m_o e^{\dfrac{-r^2}{4Dt}}}{(4 \pi Dt)&{1/2}}

    :param initial_mass: The initial mass released
    :type initial_mass: Mass
    :param area: The area of the release
    :type area: Area
    :param distance: Distance away to measuring point
    :type distance: Length
    :param D: Diffusion coefficient of the released material in the medium
    :type D: DiffusionCoefficient
    :param time: Time after release
    :type time: Time
    :return: The concentration at point z after time t
    :rtype: MultiUnit
    
    :Example:
    
    >>> from cheme_calculations.mass_transfer import one_d_pulse_decay
    >>> mo = Mass(2000, "kg")
    >>> area = Area(1, "m^2")
    >>> distance = Length(50, "m")
    >>> D = DiffusionCoefficient(3E-3, "cm^2/s")
    >>> time = Time(30000, "s")
    >>> ans = one_d_pulse_decay(mo, area, distance, D, time)
    >>> print(ans)
    >>> 0.05732841132227383 kg / m³
    """
    
    initial_mass = initial_mass/area
    
    top = initial_mass * exp((-distance**2)/(4*D*time))
    bottom = (4*pi*D*time)**(1/2)
    
    C = top/bottom
    
    return C