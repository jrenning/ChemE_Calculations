from math import pi
from re import L
from cheme_calculations.units import Temperature, MultiUnit
from cheme_calculations.units.mass_transfer import DiffusionCoefficient
from cheme_calculations.units.property_units import DynamicViscosity
from cheme_calculations.units.units import Length
from cheme_calculations.utility.constants import BOLTZMANS_CONSTANT, FARADAYS_CONSTANT

__all__ = ["wilke_chang", "stokes_einstein", "ionic_diffusion_coefficient"]
        

def wilke_chang(temperature: Temperature | float, theta_b: float, moleclar_weight_b: MultiUnit | float,
                viscosity_b: MultiUnit | float, molecular_volume_a: MultiUnit | float)-> DiffusionCoefficient:
    """Calculates a liquid liquid diffusion coefficient based on the Wilke-Chnang equation
    
    NOTE: This is an empirical equation so units must be correct
    - Temperature = F
    - Viscosity = g/cm*s or cP
    
    - b: refers to a property of the liquid being diffused in
    - a: refers to a property of the liquid that is diffusing 

    :param temperature: Temperature in Fahrenheit
    :type temperature: Temperature | float
    :param theta_b: The theta constant of the liquid being diffused in
    :type theta_b: float
    :param moleclar_weight_b: Molecular weight of the liquid being diffused in (g/mol)
    :type moleclar_weight_b: MultiUnit | float
    :param viscosity_b: Viscosity of the liquid being diffused in (g/cm*s)
    :type viscosity_b: MultiUnit | float
    :param molecular_volume_a: Molecular volume of the liquid being diffused
    :type molecular_volume_a: MultiUnit | float
    :return: A diffusion coefficient in units of cm^2/s
    :rtype: MultiUnit
    
    :Example:
    
    >>> from cheme_calculations.mass_transfer import wilke_chang
    >>> T = 100 #F
    >>> theta_b = 1
    >>> molecular_weight_b = 18
    >>> viscosity_b = 0.78
    >>> molecular_volume_a = 65
    >>> diff = wilke_chang(T, theta_b, molecular_weight_b, viscosity_b, molecular_volume_a)
    >>> print(diff)
    >>> 3.288708309263814e-06 cm² / s
    """
    
    answer = (7.4E-8*(theta_b*moleclar_weight_b)**(1/2)*temperature)/(viscosity_b*molecular_volume_a**0.6)
    
    # if units were supplied just cast the final value to the right units 
    if answer.__class__ == MultiUnit:
        return DiffusionCoefficient(answer._value, "cm^2/s")
    else:
        return DiffusionCoefficient(answer, "cm^2/s")


def stokes_einstein(T: Temperature, mu_b: DynamicViscosity, R_a: Length)-> DiffusionCoefficient:
    """Finds a liquid-liquid diffusion coefficient using the stokes-einstein method.
    Should only be used when the radius of the solute particle is greater than 
    five times bigger than the solvent's radius.
    
    .. math:: D_{AB} = \dfrac{k_b*T}{6*\pi*\mu_b*R_A}
    

    :param T: Temperature of the system (K)
    :type T: Temperature
    :param mu_b: Viscosity of the solvent
    :type mu_b: DynamicViscosity
    :param R_a: Molecular radius of the solute
    :type R_a: Length
    :return: The diffusion coefficient of the solute in the solvent
    :rtype: DiffusionCoefficient
    
    :Example:
    
    >>> from cheme_calculations.mass_transfer import stokes_einstein
    >>> T = Temperature(300, "K")
    >>> mu_b = DynamicViscosity(.001, "kg/m*s")
    >>> R_a = Length(10E-7, "cm").convert_to("m")
    >>> ans = stokes_einstein(T, mu_b, R_a)
    >>> print(ans)
    >>> 6.17239081530568e-11 m² / s
    """
    
    D_ab = (BOLTZMANS_CONSTANT*T)/(6*pi*mu_b*R_a)
    
    return D_ab 

def ionic_diffusion_coefficient(R: MultiUnit, T: Temperature, n_plus: int, n_minus: int,
                                lambda_plus: MultiUnit, lambda_minus: MultiUnit)-> DiffusionCoefficient:
    """Calculates a diffusion coefficient for a dissociated ionic species in a solvent.
    
    .. math:: \dfrac{RT*[(1/n_+)+(1/n_-)]}{F^2*[(1/ \lambda_+)+(1/ \lambda_-)]}

    :param R: Gas constant
    :type R: MultiUnit
    :param T: Temperature of the system
    :type T: Temperature
    :param n_plus: The positive charge on the cation 
    :type n_plus: int
    :param n_minus: The negative charge on the anion
    :type n_minus: int
    :param lambda_plus: The limiting ionic conductance of the cation in the solvent
    :type lambda_plus: MultiUnit
    :param lambda_minus: the limiting ionic conductance of the anion in the solvent
    :type lambda_minus: MultiUnit
    :return: The diffusion coefficient of the ions in the solvent
    :rtype: DiffusionCoefficient
    
    :Example:
    
    >>> from cheme_calculations.mass_transfer import ionic_diffusion_coefficient
    >>> from cheme_calculations.utility.constants import get_gas_constant
    >>> R = get_gas_constant(generic=True)
    >>> T = Temperature(300, "K")
    >>> n_plus = 1
    >>> n_minus = 1
    >>> lambda_plus = MultiUnit(50.1, "A/cm^2*V*mol")
    >>> lambda_minus = MultiUnit(76.3, "A/cm^2*V*mol")
    >>> D = ionic_diffusion_coefficient(R, T, n_plus, n_minus, lambda_plus, lambda_minus)
    >>> print(D)
    >>> 1.6200254370943945e-09 m² / s
    
    """
    
    D = (R*T*((1/n_plus)+(1/n_minus)))/(FARADAYS_CONSTANT**2*((1/lambda_plus)+(1/lambda_minus)))
    
    return D