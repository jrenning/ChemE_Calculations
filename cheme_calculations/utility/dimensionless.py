from cheme_calculations.units.mass_transfer import DiffusionCoefficient
from cheme_calculations.units.property_units import Cp, Density, DynamicViscosity, Velocity
from cheme_calculations.units.units import Length
from cheme_calculations.heat_transfer.unit_types import HeatTransferCoefficient, ThermalConductivity

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
    return (rho*v*d)/mu

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