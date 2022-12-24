from typing import List
from .units import BaseUnit, MultiUnit

class DiffusionCoefficient(MultiUnit):
    def __init__(self,value:float, unit: str, *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit] = []):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)