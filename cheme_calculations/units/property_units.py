from .units import BaseUnit, MultiUnit, Unit
from typing import List, Literal

class Area(Unit):
    def __init__(self, value: float, unit: str):
        unit, _ = unit.split("^")
        super().__init__(value, unit, 2)
        
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
        super().__init__(value, unit)

    

class Density(MultiUnit):
    def __init__(self,value:float, unit: str, *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)
        
        
class Enthalpy(MultiUnit):
    def __init__(self,value:float, unit: str="kJ/kg", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)
        
class Entropy(MultiUnit):
    def __init__(self,value:float, unit: str="J/g*K", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)
        
class InternalEnergy(MultiUnit):
    def __init__(self,value:float, unit: str="kJ/kg", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)
        
class Cp(MultiUnit):
    def __init__(self,value:float, unit: str="J/mol*K", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)


class Cv(MultiUnit):
    def __init__(self,value:float, unit: str="J/mol*K", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)

class Hvap(MultiUnit):
    def __init__(self,value:float, unit: str, *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)

class SpecificVolume(MultiUnit):
    def __init__(self,value:float, unit: str="m^3/kg", *, top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        if top_half and bottom_half:
            super.__init__(value, top_half=top_half, bottom_half=bottom_half)
        super().__init__(value, unit)