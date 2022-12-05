from units import MultiUnit, BaseLength, BaseUnit, LengthUnit, Unit, Velocity
from typing import Literal, List

class ThermalConductivity(MultiUnit):
        def __init__(self,value:float, energy_unit: Literal["J", "BTU"], time_unit: Literal["s", "hr"],
                     length_unit: LengthUnit, temperature_unit: Literal['K', 'C', 'F', 'R']):
            super().__init__(value, top_half=[BaseUnit(energy_unit)], bottom_half=[BaseUnit(time_unit), BaseUnit(length_unit), BaseUnit(temperature_unit)])


class HeatTransferCoefficient(MultiUnit):
    def __init__(self, value:float, top_half: List[BaseUnit], bottom_half: List[BaseUnit]):
        super().__init__(value, top_half, bottom_half)
        

def htc_open_field_laminar_local(Re: float, Pr: float, L: BaseLength,
                             k: MultiUnit):
    Nu_local: float = 0.332*Re**(1/2)*Pr**(1/3)
    h: MultiUnit = (Nu_local * k) / L
    return HeatTransferCoefficient(h._value, h._top_half, h._bottom_half)
    

def htc_open_field_laminar_avg(Re: float, Pr: float, L: BaseLength,
                             k: MultiUnit):
    
    Nu_local: float = 0.664*Re**(1/2)*Pr**(1/3)
    h: MultiUnit = (Nu_local * k) / L
    return HeatTransferCoefficient(h._value, h._top_half, h._bottom_half)


if __name__ == "__main__":
    d = BaseLength(1, 'm')
    rho = MultiUnit(1.5,"kg/m^3")
    v = MultiUnit(2, "m/s")
    mu = MultiUnit(3, "kg/m*s")
    l = rho*v*d
    print(l)
    r = (l)/mu
    assert(r == 1.0)
    