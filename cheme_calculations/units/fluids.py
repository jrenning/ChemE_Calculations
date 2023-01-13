from typing import List
from cheme_calculations.units.units import BaseUnit, MultiUnit


class VolumetricFlowrate(MultiUnit):
    def __init__(self,value:float, unit: str="", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit] = []):
        if top_half and bottom_half:
            super().__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)