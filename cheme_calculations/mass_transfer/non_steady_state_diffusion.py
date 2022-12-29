from math import erf, erfc, sqrt
from cheme_calculations.units.mass_transfer import Concentration, DiffusionCoefficient
from cheme_calculations.units.units import Length, Time

__all__ = ["semi_infinite_slab_diffusion", "finite_slab_diffusion"]


def semi_infinite_slab_diffusion(Cs: Concentration, Co: Concentration,
                                 z: Length, D: DiffusionCoefficient, t: Time)-> Concentration:
    """Finds the concentration x distance into a slab after a certain period
    of time using a semi-infinite assumption (slab is infinitely deep).
    A valid assumption only at small time intervals.
    
    .. math:: C = C_s - (C_s - C_o) * erf(\dfrac{z}{\sqrt{4Dt}})

    :param Cs: Surface concentration mass is flowing from
    :type Cs: Concentration
    :param Co: Initial concentration of the slab
    :type Co: Concentration
    :param z: Depth into the slab from the surface
    :type z: Length
    :param D: The diffusion coefficient of the diffusing substance in the material
    :type D: DiffusionCoefficient
    :param t: Time after diffusion began
    :type t: Time
    :return: The concentration in the slab at depth z after time t
    :rtype: Concentration
    
    :Example:
    
    >>> from cheme_calculations.mass_transfer import semi_infinite_slab_diffusion
    >>> Cs = Concentration(1, "kg/m^3")
    >>> Co = Concentration(0, "kg/m^3")
    >>> z = Length(1, "m")
    >>> D = DiffusionCoefficient(.05, "m^2/s")
    >>> t = Time(30, "s")
    >>> ans = semi_infinite_slab_diffusion(Cs, Co, z, D, t)
    >>> print(ans)
    >>> 0.563702861650773 kg / m³
    """
    
    C = Cs - (Cs-Co) * erf(z/(4*D*t)**(1/2))
    
    return C

def finite_slab_diffusion(Cs: Concentration, Co: Concentration, a: Length, 
                          z: Length, D: DiffusionCoefficient, t: Time, iterations: int=10)-> Concentration:
    """Finds the concentration at a point z into a slab after time t. This 
    function uses a finite slab model.
    
    .. math:: C = C_s - (C_s - C_o)* \sum_{n=0}^\inf (-1)^n [erfc(\dfrac{(2n+1)a+z}{\sqrt{4Dt}})+ erfc(\dfrac{(2n+1)a-z}{\sqrt{4Dt}})]

    :param Cs: Surface concentration on the slab
    :type Cs: Concentration
    :param Co: Initial concentration of the slab
    :type Co: Concentration
    :param a: Distance to the no flux line
    :type a: Length
    :param z: Distance from the measuring point to the no flux line (ie if no flux and point are the same it is 0)
    :type z: Length
    :param D: The diffusion coefficient of the substance in question into the slab
    :type D: DiffusionCoefficient
    :param t: Time after diffusion began
    :type t: Time
    :param iterations: Number of iterations to use in summation, defaults to 10
    :type iterations: int, optional
    :return: The concentration at point z after time t
    :rtype: Concentration
    
    :Example:
    
    >>> from cheme_calculations.mass_transfer import finite_slab_diffusion
    >>> Cs = Concentration(1, "kg/m^3")
    >>> Co = Concentration(.2, "kg/m^3")
    >>> a = Length(1, "m")
    >>> z = Length(0, "m")
    >>> D = DiffusionCoefficient(.05, "m^2/s")
    >>> t = Time(30000, "s")
    >>> ans = finite_slab_diffusion(Cs, Co, a, z, D, t)
    >>> print(ans)
    >>> 0.7719641684120253 kg / m³
    """
    
    right_side = 0
    
    for n in range(iterations):
        right_side += (-1)**n * (erfc(((2*n+1)*a+z)/(4*D*t)**(1/2))+ erfc(((2*n+1)*a-z)/(4*D*t)**(1/2)))
        
    C = Cs - (Cs - Co)*right_side
    
    return C
    
    