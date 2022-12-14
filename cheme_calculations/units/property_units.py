from .units import BaseUnit, MultiUnit, Unit
from typing import List, Literal

class Area(Unit):
    def __init__(self, value: float, unit: str):
        unit, _ = unit.split("^")
        super().__init__(value, unit, 2)
        
class Volume(Unit):
    def __init__(self, value: float, unit: str):
        unit, _ = unit.split("^")
        super().__init__(value, unit, 3)


class Velocity(MultiUnit):
    def __init__(self,value:float, unit: str, *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit] = []):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)


class Gravity(MultiUnit):
    def __init__(self,value:float, unit: Literal["m/s^2", "ft/s^2"], *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit] = []):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)

class DynamicViscosity(MultiUnit):
    def __init__(self, value, unit=Literal["cP", "kg/m*s", "cm/m*s"]):
        if unit == "cP":
            unit_string = "kg/m*s"
            super().__init__(value/1000,unit_string)
        else:
            super().__init__(value, unit)

    

class Density(MultiUnit):
    def __init__(self,value:float, unit: str, *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)
        
class Cp(MultiUnit):
    def __init__(self,value:float, unit: str="J/mol*K", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)
    
class Hvap(MultiUnit):
    def __init__(self,value:float, unit: str, *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)
    