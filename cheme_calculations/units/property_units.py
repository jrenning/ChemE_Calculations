from .units import BaseUnit, MultiUnit, Unit
from typing import List, Literal

class Area(Unit):
    def __init__(self, value: float, unit: str):
        unit, _ = unit.split("^")
        super().__init__(value, unit, 2)
    

class Density(MultiUnit):
    def __init__(self,value:float, unit: str, *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)