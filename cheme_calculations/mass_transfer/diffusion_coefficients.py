from cheme_calculations.units import Temperature, MultiUnit
from cheme_calculations.units.property_units import DynamicViscosity

__all__ = ["wilke_chang"]
        

def wilke_chang(temperature: Temperature | float, theta_b: float, moleclar_weight_b: MultiUnit | float,
                viscosity_b: MultiUnit | float, molecular_volume_a: MultiUnit | float):
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
    
    return MultiUnit(answer, "cm^2/s")


    