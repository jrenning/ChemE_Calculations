from cheme_calculations.units import MultiUnit, Length, Unit
from .unit_types import HeatTransferCoefficient, ThermalConductivity




def htc_open_field_laminar_local(Re: float, Pr: float, L: Length,
                             k: ThermalConductivity):
    Nu_local: float = 0.332*Re**(1/2)*Pr**(1/3)
    h: MultiUnit = (Nu_local * k) / L
    return HeatTransferCoefficient(h._value, top_half=h._top_half, bottom_half=h._bottom_half)
    

def htc_open_field_laminar_avg(Re: float, Pr: float, L: Length,
                             k: ThermalConductivity):
    
    Nu_local: float = 0.664*Re**(1/2)*Pr**(1/3)
    h: MultiUnit = (Nu_local * k) / L
    return HeatTransferCoefficient(h._value, top_half=h._top_half, bottom_half=h._bottom_half)

    
    
    