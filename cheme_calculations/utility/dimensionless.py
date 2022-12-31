from xmlrpc.client import MultiCall
from cheme_calculations.units.mass_transfer import DiffusionCoefficient
from cheme_calculations.units.property_units import Cp, Density, DynamicViscosity, Gravity, Velocity
from cheme_calculations.units.units import Length, Temperature, Unit
from cheme_calculations.units.heat_transfer import ThermalConductivity, HeatTransferCoefficient

__all__ = ["reynolds", "biot", "prandtl", "schmidt", "gretz", "grashof"]

def reynolds(rho: Density, v: Velocity, L: Length, mu: DynamicViscosity)-> float:
    """Calculates the reynolds number for a fluid

    :param rho: Density of the fluid
    :type rho: Density
    :param v: Velocity of the fluid
    :type v: Velocity
    :param L: Characteristic length of the flow (for pipe flow use diameter)
    :type L: Length
    :param mu: Viscosity of the fluid
    :type mu: DynamicViscosity
    :return: The Reynolds number
    :rtype: float
    """
    return (rho*v*L)/mu

def biot(h: HeatTransferCoefficient, L: Length, k: ThermalConductivity)-> float:
    """Calculates the Biot number for a given system. Useful for determining if 
    either conductive or convective resistance can be neglected.

    :param h: Heat transfer coefficient of the system
    :type h: HeatTransferCoefficient
    :param L: Characteristic length of the system (ie s(distance to no flux line) for planar systems)
    :type L: Length
    :param k: Thermal conductivity value for the thing being heated in the system
    :type k: ThermalConductivity
    :return: The Biot number
    :rtype: float
    """
    return (h*L)/k

def prandtl(mu: DynamicViscosity, cp: Cp, k: ThermalConductivity) -> float:
    """Calculates the dimensionless Prandtl number for a system. Useful in finding
    heat transfer coefficients

    :param mu: Viscosity of the fluid being heated
    :type mu: DynamicViscosity
    :param cp: Heat capacity of the fluid
    :type cp: Cp
    :param k: Thermal conductivity of the fluid
    :type k: ThermalConductivity
    :return: The Prandtl number
    :rtype: float
    """
    return (mu*cp)/k

def schmidt(mu: DynamicViscosity, rho: Density, D: DiffusionCoefficient)-> float:
    """Calculates the dimensionless Schmidt number. Useful for finding mass transfer
    coefficients.

    :param mu: Viscosity of the fluid
    :type mu: DynamicViscosity
    :param rho: Density of the fluid
    :type rho: Density
    :param D: Diffusion coefficient of the target substance in the fluid
    :type D: DiffusionCoefficient
    :return: The Schmidt number
    :rtype: float
    """
    return mu/(rho*D)


def gretz(diameter: Length, length: Length, cp: Cp, characteristic_length: Length, rho: Density, 
          characteristic_speed: Velocity, k: ThermalConductivity)-> float:
    """Calculates the Gretz number. Useful for characterization of laminar flow in heat and mass transfer.
    Only used in a pipe scenario.

    :param diameter: Diameter of the pipe 
    :type diameter: Length
    :param length: Length of the pipe
    :type length: Length
    :param cp: Heat capacity of the fluid in the pipe
    :type cp: Cp
    :param characteristic_length: Characteristic length of the pipe (ie diameter for regular pipes, 4*hydraulic radius for annulus)
    :type characteristic_length: Length
    :param rho: Density of the fluid in the pipe
    :type rho: Density
    :param characteristic_speed: Characteristic speed of the fluid
    :type characteristic_speed: Velocity
    :param k: Thermal conductivity of the fluid in the pipe
    :type k: ThermalConductivity
    :return: The Gretz number
    :rtype: float
    """
    
    return (cp*diameter*characteristic_length*rho*characteristic_speed)/(k*length)



def grashof(g: Gravity, beta: Temperature, T2: Temperature, T1: Temperature, L: Length, 
            rho: Density, mu: DynamicViscosity)-> float:
    """_summary_

    :param g: The gravity in the system
    :type g: Gravity
    :param beta: The beta value for the system, units of 1/temperature
    :type beta: Temperature
    :param T2: Hotter temperature
    :type T2: Temperature
    :param T1: Cooler temperature
    :type T1: Temperature
    :param L: Characteristic length of the system (ie diameter for pipe flow)
    :type L: Length
    :param rho: Density of the fluid in the system
    :type rho: Density
    :param mu: Viscosity of the fluid in the system
    :type mu: DynamicViscosity
    :return: The Grashof number
    :rtype: float
    
    :Example:
    
    >>> from cheme_calculations.utility import grashof
    >>> g = Gravity(9.81, "m/s^2")
    >>> beta = Temperature(.0015, "K", -1)
    >>> T2 = Temperature(300, "K")
    >>> T1 = Temperature(275, "K")
    >>> L = Length(1, "m")
    >>> rho = get_water_properties(275)._density
    >>> mu = get_water_properties(275)._viscosity.convert_to("kg/m*s")
    >>> gr = grashof(g, beta, T2, T1, L, rho, mu)
    >>> print(gr)
    >>> 130031273830.54044
    
    """
    
    return (L**3*rho**2*beta*(T2-T1)*g)/(mu**2)

def beta(rho_1: Density, rho_2: Density,
         T2: Temperature, T1: Temperature)-> Unit:
    """Calculates the beta variable for use in calculating the 
    Grashof number of a fluid
    
    .. math:: \beta = \dfrac{\rho_1- \rho_2}{\rho * (T_2 - T_1)}

    :param rho_1: Density at temperature 1
    :type rho_1: Density
    :param rho_2: Density at temperature 2
    :type rho_2: Density
    :param T2: Hotter temperature in the system
    :type T2: Temperature
    :param T1: Cooler temperature in the system
    :type T1: Temperature
    :return: The beta variable, units of temperature^-1
    :rtype: Unit
    """
    beta = (rho_1-rho_2)/(((rho_1+rho_2)/2)*(T2-T1))
    
    return beta