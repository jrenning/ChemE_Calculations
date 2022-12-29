from typing import List
from .units import BaseUnit, LengthUnits, MultiUnit, TimeUnits, VolumeUnits, MassUnits

# mass per volume (length ^ 3)
ConcentrationUnits = [f"{x}/{y}" for x in MassUnits for y in VolumeUnits]
# add molar
ConcentrationUnits.append("M")

# length^2 / time
DiffusionCoefficientUnits = [f"{x}^2/{y}" for x in LengthUnits for y in TimeUnits]

class DiffusionCoefficient(MultiUnit):
    def __init__(self,value:float, unit: str, *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit] = []):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)
        
class Concentration(MultiUnit):
    def __init__(self,value:float, unit: ConcentrationUnits, *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit] = []):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)