from units import MultiUnit
from typing import Literal

class Density(MultiUnit):
    def __init__(self,value:float, unit: str, *, length_unit: Literal["m", "ft"]="m", mass_unit: Literal["g", "lb"]="g"):
        super().__init__(value, unit)