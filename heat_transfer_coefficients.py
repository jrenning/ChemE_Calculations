from units import MultiUnit, BaseLength, BaseUnit, LengthUnit, Unit, Velocity, Energy
from typing import Literal, List

class ThermalConductivity(MultiUnit):
        def __init__(self,value:float, energy_unit: Literal["J", "BTU"], time_unit: Literal["s", "hr"],
                     length_unit: LengthUnit, temperature_unit: Literal['K', 'C', 'F', 'R']):
            super().__init__(value, top_half=[BaseUnit(energy_unit)], bottom_half=[BaseUnit(time_unit), BaseUnit(length_unit), BaseUnit(temperature_unit)])


class HeatTransferCoefficient(MultiUnit):
    def __init__(self, value:float, top_half: List[BaseUnit], bottom_half: List[BaseUnit]):
        super().__init__(value, top_half, bottom_half)
        

def htc_open_field_laminar_local(Re: float, Pr: float, L: BaseLength,
                             k: ThermalConductivity):
    Nu_local: float = 0.332*Re**(1/2)*Pr**(1/3)
    h: MultiUnit = (Nu_local * k) / L
    return HeatTransferCoefficient(h._value, h._top_half, h._bottom_half)
    

def htc_open_field_laminar_avg(Re: float, Pr: float, L: BaseLength,
                             k: ThermalConductivity):
    
    Nu_local: float = 0.664*Re**(1/2)*Pr**(1/3)
    h: MultiUnit = (Nu_local * k) / L
    return HeatTransferCoefficient(h._value, h._top_half, h._bottom_half)


if __name__ == "__main__":
    J = Unit(50, "J")
    v = MultiUnit(50, "m/s")
    print(v/J)
    
    
    