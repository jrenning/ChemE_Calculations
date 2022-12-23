from cheme_calculations.units import MultiUnit, Length, Unit
from .unit_types import HeatTransferCoefficient, ThermalConductivity


__all__ = ["htc_open_field_laminar_local", "htc_open_field_laminar_avg"]

def htc_open_field_laminar_local(Re: float, Pr: float, L: Length,
                             k: ThermalConductivity)-> HeatTransferCoefficient:
    """Calculates the heat transfer coefficient for open field flow with a laminar flow profile at a local point

    :param Re: The renoyld number of the fluid
    :type Re: float
    :param Pr: The prandlt number of the fluid
    :type Pr: float
    :param L: The length of the object flow is against
    :type L: class: Length
    :param k: Thermal conductivity of the fluid
    :type k: class: ThermalConductivity
    :return: A heat transfer coefficient
    :rtype: class: HeatTransferCoefficient
    """
    Nu_local: float = 0.332*Re**(1/2)*Pr**(1/3)
    h: MultiUnit = (Nu_local * k) / L
    return HeatTransferCoefficient(h._value, top_half=h._top_half, bottom_half=h._bottom_half)
    

def htc_open_field_laminar_avg(Re: float, Pr: float, L: Length,
                             k: ThermalConductivity):
    
    Nu_local: float = 0.664*Re**(1/2)*Pr**(1/3)
    h: MultiUnit = (Nu_local * k) / L
    return HeatTransferCoefficient(h._value, top_half=h._top_half, bottom_half=h._bottom_half)

    
    
    