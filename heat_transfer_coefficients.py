from units import MultiUnit, Length, BaseUnit, LengthUnit, Unit, Velocity, Energy
from typing import Literal, List

class ThermalConductivity(MultiUnit):
    def __init__(self,value:float, unit: str="", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super().__init__(value, top_half=top_half, bottom_half=bottom_half)
        else:
            super().__init__(value, unit)


class HeatTransferCoefficient(MultiUnit):
    def __init__(self,value:float, unit: str="", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super().__init__(value, top_half=top_half, bottom_half=bottom_half)
        else:
            super().__init__(value, unit)
        

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


if __name__ == "__main__":
    J = Unit(50, "J")
    v = MultiUnit(50, "m/s")
    print(v/J)
    
    
    