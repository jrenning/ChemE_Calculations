from math import log, pi
from cheme_calculations.units import DiffusionCoefficient
from cheme_calculations.units.mass_transfer import Concentration
from cheme_calculations.units.property_units import Area
from cheme_calculations.units.units import Length, MultiUnit

__all__ = ["planar_mass_transfer_steady_state", "planar_mass_flux_steady_state",
           "pipe_mass_transfer_steady_state", "sphere_mass_transfer_steady_state"]

def planar_mass_transfer_steady_state(D: DiffusionCoefficient, A: Area, C2: Concentration,
                C1: Concentration, thickness: Length)-> MultiUnit:
    """Calculates a mass transfer rate for a planar system at steady state.
    
    .. math:: JA = -DA \dfrac{C_2-C_1}{thickness}

    :param D: Diffusion coefficient for the system
    :type D: DiffusionCoefficient
    :param A: Area of the planar system
    :type A: Area
    :param C2: Downstream concentration that the mass flows to
    :type C2: Concentration
    :param C1: Upstream concentration the mass flows from 
    :type C1: Concentration
    :param thickness: Thickness of the planar system
    :type thickness: Length
    :return: The mass transfer rate, in units of mass / time
    :rtype: MultiUnit
    """
    JA = -D * A * ((C2-C1)/thickness)
    
    return JA

def planar_mass_flux_steady_state(D: DiffusionCoefficient, C2: Concentration,
                C1: Concentration, thickness: Length)-> MultiUnit:
    """Calculates a mass transfer flux for a planar system at steady state.
    
    .. math:: J = -D \dfrac{C2-C1}{thickness}

    :param D: Diffusion coefficient for the system
    :type D: DiffusionCoefficient
    :param C2: Downstream concentration that the mass flows to
    :type C2: Concentration
    :param C1: Upstream concentration the mass flows from
    :type C1: Concentration
    :param thickness: Thickness of the planar system
    :type thickness: Length
    :return: The mass transfer rate, in units of mass / time
    :rtype: MultiUnit
    """
    J = -D * ((C2-C1)/thickness)
    
    return J

def pipe_mass_transfer_steady_state(D: DiffusionCoefficient, r2: Length, r1: Length, C2: Concentration,
                C1: Concentration, L: Length)-> MultiUnit:
    """Calculates the steady state mass transfer rate at steady state in a pipe.
    
    .. math:: JA = -2 \pi L D * \dfrac{C_2-C_1}{ln(\dfrac{r_2}{r_2})}

    :param D: Diffusion coefficient for the material
    :type D: DiffusionCoefficient
    :param r2: Outer radius of the pipe
    :type r2: Length
    :param r1: Inner radius of the pipe
    :type r1: Length
    :param C2: Downstream concentration mass transfer flows to it
    :type C2: Concentration
    :param C1: Upstream concentration mass transfer flows from it
    :type C1: Concentration
    :param L: Length of the pipe
    :type L: Length
    :return: The mass transfer rate, units of mass / time
    :rtype: MultiUnit
    
    :Example:
    
    >>> from cheme_calculations.mass_transfer import pipe_mass_transfer_steady_state
    >>> D = DiffusionCoefficient(1E-3, "m^2/s")
    >>> r2 = Length(.5, "m")
    >>> r1 = Length(.4, "m")
    >>> C2 = Concentration(0, "kg/m^3")
    >>> C1 = Concentration(0.015, "kg/m^3")
    >>> L = Length(5, "m")
    >>> ans = pipe_mass_transfer_steady_state(D, r2, r1, C2, C1, L)
    >>> print(ans)
    >>> 0.0021118194779239426 kg / s
    
    """
    
    
    JA = -2*pi*L*D*((C2-C1)/log(r2/r1))
    
    return JA
    
    
def sphere_mass_transfer_steady_state(D: DiffusionCoefficient, r2: Length, r1: Length, C2: Concentration,
                C1: Concentration)-> MultiUnit:
    """Calculates the steady state mass transfer in a sphere at steady state.
    
    .. math:: JA = -4 \pi r_1 r_2 D* \dfrac{C_2-C_1}{r_2-r_1}

    :param D: Diffusion coefficient for the material
    :type D: DiffusionCoefficient
    :param r2: Outer radius of the sphere
    :type r2: Length
    :param r1: Inner radius of the sphere
    :type r1: Length
    :param C2: Upstream concentration mass transfer flows from it
    :type C2: Concentration
    :param C1: Downstream concentration mass transfer flows to it
    :type C1: Concentration
    :return: The mass transfer rate, units of mass / time
    :rtype: MultiUnit
    
    :Example:
    
    >>> from cheme_calculations.mass_transfer import sphere_mass_transfer_steady_state
    >>> D = DiffusionCoefficient(1E-3, "m^2/s")
    >>> r2 = Length(.5, "m")
    >>> r1 = Length(.4, "m")
    >>> C2 = Concentration(0, "kg/m^3")
    >>> C1 = Concentration(0.015, "kg/m^3")
    >>> ans = sphere_mass_transfer_steady_state(D, r2, r1, C2, C1)
    >>> print(ans)
    >>> 0.00037699111843077525 kg / s
    """
    
    JA = -4*pi*r1*r2*D*((C2-C1)/(r2-r1))
    
    return JA