from cheme_calculations.units import Temperature, Length
from cheme_calculations.units.property_units import Density, DynamicViscosity, Gravity, Hvap
from cheme_calculations.units.units import MultiUnit
from cheme_calculations.units.heat_transfer import HeatFlux, HeatTransferCoefficient, ThermalConductivity

__all__ = ['condensation_transfer_coefficient', "flux_max_boiling"]

def condensation_transfer_coefficient(k: ThermalConductivity, 
                                      rho: Density, g: Gravity,
                                      hvap: Hvap, num_pipes: int, 
                                      T2: Temperature, T1: Temperature, 
                                      diameter: Length, mu: DynamicViscosity) -> HeatTransferCoefficient:
    """
    Calculates the heat transfer coefficient for a bundle of tubes stacked vertically
    
    NOTE: properties should be taken at a temperature value of 3/4 of the way to the pipe wall temperature
    NOTE: T2 must be higher than T1 or you will get imaginary answers
    
    :param k: Thermal conductivity taken at the correct temperature
    :type k: ThermalConductivity
    :param rho: Density of the vapor taken at the correct temperature
    :type rho: Density
    :param g: The gravity
    :type g: Gravity
    :param hvap: The heat of vaporization for the given material
    :type hvap: Hvap
    :param num_pipes: The number of pipes in the stack
    :type num_pipes: int
    :param T2: Temperature at the condensation point of the vapor ie 100 C for water at 1 atm (assumption made)
    :type T2: Temperature
    :param T1: Temperature at the pipe wall
    :type T1: Temperature
    :param diameter: the diameter of the tubes
    :type diameter: Length
    :param mu: the viscosity taken at the correct temperature
    :type mu: DynamicViscosity
    :return: The heat transfer coefficient 
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import condensation_transfer_coefficient
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> rho = Density(800, "kg/m^3")
    >>> g = Gravity(9.81 "m/s^2")
    >>> hv = Hvap(3000, "J/kg")
    >>> num_pipes = 4
    >>> T2 = Temperature(400, "K")
    >>> T1 = Temperature(300, "K")
    >>> d = Length(1, "m")
    >>> mu = DynamicViscosity(.001, "kg/m*s")
    >>> h = condensation_transfer_coefficient(
        k, rho, g, hv, num_pipes, T2, T1, d, mu
    )
    >>> print(h)
    >>> 231.50934556238877 W / m² * K
    """
    
    
    t = (k**3 * rho**2 * g * hvap)
    print(t)
    b = (num_pipes * (T2-T1) * diameter * mu)
    print(b)

    h = 0.729*((k**3 * rho**2 * g * hvap)/(num_pipes * (T2-T1) * diameter * mu))**(1/4)
    
    
    return h

def flux_max_boiling(hvap: Hvap, rho_v: Density, rho_l: Density, 
                     surface_tension: MultiUnit, g: Gravity)-> HeatFlux:
    """Max flux possible for a boiling scenario
    
    NOTE: This equation has complicated unit operations so the final answer is cast to 
    W/m^2 explicitly, to get other units in the answer use the convert_to method 

    :param hvap: Heat of vaporization for the substance
    :type hvap: Hvap
    :param rho_v: Density of the vapor
    :type rho_v: Density
    :param rho_l: Density of the liquid
    :type rho_l: Density
    :param surface_tension: Surface tension of the liquid
    :type surface_tension: MultiUnit
    :param g: The gravity
    :type g: Gravity
    :return: The max flux
    :rtype: HeatFlux
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import flux_max_boiling
    >>> Hvap = Hvap(3000, "J/kg")
    >>> rho_v = Density(0.776, "kg/m^3")
    >>> rho_l = Density(0.987, "kg/m^3")
    >>> surface_t = MultiUnit(52, "kg/s^2")
    >>> g = Gravity(9.81, "m/s^2")
    >>> qA = flux_max_boiling(Hvap, rho_v, rho_l, surface_t, g)
    >>> print(qA)
    >>> 1276.827053549569 W / m²
    """
    
    qa_max: MultiUnit = 0.15*hvap*rho_v**(1/2)*(surface_tension*g*(rho_l-rho_v))**(1/4)
        
    qa_max.convert_to("W/m^2")
    
    return qa_max