
from cheme_calculations.units import MultiUnit, BaseUnit
from typing import List, Literal

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
            
class HeatFlux(MultiUnit):
    def __init__(self,value:float, unit: str="", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super().__init__(value, top_half=top_half, bottom_half=bottom_half)
        else:
            super().__init__(value, unit)
            
class Power(MultiUnit):
    def __init__(self,value:float, unit: str=Literal["W", "BTU/hr", "BTU/s"], *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super().__init__(value, top_half=top_half, bottom_half=bottom_half)
        else:
            super().__init__(value, unit)