from typing import Literal, TypeVar, Generic, Union



T = TypeVar('T')


# TODO implement unit conversions
class Unit:
    def __init__(self, value:float, unit: Generic[T], exponent: int=1):
        self._value = value
        self._unit = unit
        self._exponent = exponent
        
    def __repr__(self) -> str:
        if self._exponent == 1:
            return f"{self._value} {self._unit}"
        else:
            return f"{self._value} {self._unit}^{self._exponent}"
        
    def __add__(self, other):
        if isinstance(other, self.__class__):
            if (self._unit == other._unit) and (self._exponent == other._exponent):
                return Unit(self._value + other._value, self._unit, self._exponent)
        elif isinstance(other, Union[int, float]):
            return Unit(self._value + other, self._unit)
        else:
            raise TypeError(f"Adding class {self.__class__} and {other.__class__} is unsupported")
    def __sub__(self,other):
        if isinstance(other, self.__class__):
            if (self._unit == other._unit) and (self._exponent == other._exponent):
                return Unit(self._value - other._value, self._unit, self._exponent)
        elif isinstance(other, Union[int, float]):
            return Unit(self._value - other, self._unit)
        else:
            raise TypeError(f"Subtracting class {self.__class__} and {other.__class__} is unsupported")
    def __truediv__(self, other):
        # same class 
        if isinstance(other, self.__class__):
            if (self._unit == other._unit):
                exponent_remainder = self._exponent - other._exponent
                if exponent_remainder == 0:
                    return self._value / other._value
                else:
                    return Unit(self._value / other._value, self._unit, exponent_remainder)
        # if both units
        elif other.__class__.__bases__[0] == Unit:
            return Unit(self._value / other._value, f"{self._unit}/{other._unit}")
        elif isinstance(other, Union[int, float]):
            return Unit(self._value / other, self._unit)
        else:
            raise TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
    def __mul__(self, other):
                # same class 
        if isinstance(other, self.__class__):
            if (self._unit == other._unit):
                    return Unit(self._value * other._value, self._unit, self._exponent + other._exponent)
        # if both units
        if other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
            if ("/" in self._unit):
                split = self._unit.split("/")
                top_half = split[0]
                bottom_half = split[1]
                print(bottom_half)
                if "/" in other._unit:
                    pass
                else:
                    return Unit(self._value * other._value, f"{top_half} * {other._unit} /{bottom_half}")
                
            return Unit(self._value * other._value, f"{self._unit} * {other._unit}")
        elif isinstance(other, Union[int, float]):
            return Unit(self._value / other, self._unit)
        else:
            raise TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
        
    def __pow__(self, other):
        if isinstance(other, Union[int, float]):
            return Unit(self._value**other, self._unit, self._exponent*other)
        else:
            raise TypeError(f"Exponentiations with class {self.__class__} and {other.__class__} is unsupported")
        


class Temperature(Unit):
    def __init__(self, value:float, unit: Literal["K", "C", "F", "R"], exponent: int =1):
        super().__init__(value, unit, exponent)

class Pressure(Unit):
    def __init__(self, value:float, unit: Literal["Pa", "kPa", "bar", "atm", "mmHg", "torr"],
                 exponent: int = 1):
        super().__init__(value, unit, exponent)
    
class BaseLength(Unit):
    def __init__(self,value:float, unit: Literal["m", "ft"],
                 exponent: int = 1):
        super().__init__(value, unit, exponent)
        
def getR_constant(temperature_units: Literal["K", "C", "F", "R"],
                  volume_units: Literal["cm^3", "m^3", "L"],
                  pressure_units: Literal["Pa", "kPa", "bar", "atm", "mmHg", "torr"],
                  generic=False):
    if generic:
        return 8.314
    if volume_units == "m^3" and pressure_units == "Pa" and temperature_units == "K":
        return 8.314
    if volume_units == "L" and pressure_units == "atm" and temperature_units == "K":
        return 0.08205
    if volume_units == "m^3" and pressure_units == "atm" and temperature_units == "K":
        return 8.205746E-5
    
    raise ValueError("The units supplied to R are not defined in a known constant")
    
        
        