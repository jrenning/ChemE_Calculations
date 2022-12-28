from cheme_calculations.units import Length
from cheme_calculations.units.heat_transfer import HeatTransferCoefficient, ThermalConductivity


__all__ = ["htc_open_field_laminar_local", "htc_open_field_laminar_avg"]

def htc_open_field_laminar_local(Re: float, Pr: float, L: Length,
                             k: ThermalConductivity)-> HeatTransferCoefficient:
    """Calculates the heat transfer coefficient for open field flow with a laminar flow profile at a local point

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandlt number of the fluid
    :type Pr: float
    :param L: The length of the object flow is against
    :type L: Length
    :param k: Thermal conductivity of the fluid
    :type k: ThermalConductivity
    :return: A heat transfer coefficient
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_open_field_laminar_local
    >>> Re = 200000
    >>> Pr = 0.78
    >>> L = Length(50, "m")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> h = htc_open_field_laminar_local(Re, Pr, L, k)
    >>> print(h)
    >>> 1.6400831313611866 W / m² * K
    """
    Nu_local: float = 0.332*Re**(1/2)*Pr**(1/3)
    h = (Nu_local * k) / L
    # TODO make this unneeded
    if "BTU" in k.__repr__():
        h.convert_to("BTU/hr*ft^2*F", True)
    else:
        h.convert_to("W/m^2*K", True)
    return HeatTransferCoefficient(h._value, top_half=h._top_half, bottom_half=h._bottom_half)
    

def htc_open_field_laminar_avg(Re: float, Pr: float, L: Length,
                             k: ThermalConductivity):
    """Calculates the average heat transfer coefficient for open field flow with a laminar flow profile

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandlt number of the fluid
    :type Pr: float
    :param L: The length of the object flow is against
    :type L: Length
    :param k: Thermal conductivity of the fluid
    :type k: ThermalConductivity
    :return: A heat transfer coefficient
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_open_field_laminar_avg
    >>> Re = 200000
    >>> Pr = 0.78
    >>> L = Length(50, "m")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> h = htc_open_field_laminar_local(Re, Pr, L, k)
    >>> print(h)
    >>> 3.280166262722373 W / m² * K
    """
    
    Nu_local: float = 0.664*Re**(1/2)*Pr**(1/3)
    h = (Nu_local * k) / L
    if "BTU" in k.__repr__():
        h.convert_to("BTU/hr*ft^2*F", True)
    else:
        h.convert_to("W/m^2*K", True)
    return HeatTransferCoefficient(h._value, top_half=h._top_half, bottom_half=h._bottom_half)

    
    
    