from typing import Literal, TypeVar, Generic, Union, List



T = TypeVar('T')


# TODO implement unit conversions
# base unit class only meant for units with fractions or multiplications 
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
        if other.__class__ == self.__class__:
            if (self._unit == other._unit):
                exponent_remainder = self._exponent - other._exponent
                if exponent_remainder == 0:
                    return self._value / other._value
                else:
                    return Unit(self._value / other._value, self._unit, exponent_remainder)
        # if both units
        elif other.__class__.__bases__[0] == Unit:
            return MultiUnit( top_half=[self], bottom_half=[other], value=self._value / other._value)
        elif isinstance(other, Union[int, float]):
            return Unit(self._value / other, self._unit)
        else:
            raise TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
    def __mul__(self, other):
        # same class 
        if self.__class__ == other.__class__:
            if (self._unit == other._unit):
                    return Unit(self._value * other._value, self._unit, self._exponent + other._exponent)
        # if both units
        if other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
                return MultiUnit(top_half=[self, other], bottom_half=None, value=self._value * other._value)
        elif isinstance(other, Union[int, float]):
            return Unit(self._value * other, self._unit)
        else:
            raise TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
        
    def __pow__(self, other):
        if isinstance(other, Union[int, float]):
            return Unit(self._value**other, self._unit, self._exponent*other)
        else:
            raise TypeError(f"Exponentiations with class {self.__class__} and {other.__class__} is unsupported")
        
class MultiUnit:
    def __init__(self, top_half: List[Unit], bottom_half: List[Unit], value: float):
        self._top_half = top_half
        self._bottom_half = bottom_half
        self._value = value
    def __repr__(self):
        top_string = " * ".join(f"{x._unit}^{x._exponent}" if x._exponent != 1 else f"{x._unit}" for x in self._top_half)
        if self._bottom_half:
            bottom_string = " * ".join(f"{x._unit}^{x._exponent}" if x._exponent != 1 else f"{x._unit}" for x in self._bottom_half)
            return f"{self._value} {top_string} / {bottom_string}"
        else:
            return f"{self._value} {top_string}"
    def __add__(self, other):
        if self.__class__ == other.__class__:
            if self._top_half == other._top_half and self._bottom_half == other._bottom_half:
                return MultiUnit(top_half=self._top_half, bottom_half=self._bottom_half, value= self._value + other._value)
        else:
            raise TypeError(f"Adding class {self.__class__} and {other.__class__} is unsupported")
    def __sub__(self, other):
        if self.__class__ == other.__class__:
            if self._top_half == other._top_half and self._bottom_half == other._bottom_half:
                return MultiUnit(top_half=self._top_half, bottom_half=self._bottom_half, value= self._value - other._value)
        else:
            raise TypeError(f"Subtracting class {self.__class__} and {other.__class__} is unsupported")
    def __truediv__(self,other):
        pass
    
            

class Temperature(Unit):
    standard: str = "K"
    to_standard_conversions = {
        "F": lambda x: (5/9)*x + 459.67,
        "C": lambda x: x + 273.15,
        "R": lambda x: x / (1.8)
    }
    from_standard_conversions = {
        "F": lambda x: 1.8*(x-273.15)+32,
        "C": lambda x: x - 273.15,
        "R": lambda x: x * 1.8,
    }
    def __init__(self, value:float, unit: Literal["K", "C", "F", "R"], exponent: int =1):
        super().__init__(value, unit, exponent)
    def convert_to(self,unit):
        if (self._unit == unit):
            return self
        if (unit == self.standard):
            val = self.to_standard_conversions[self._unit](self._value)
            return Temperature(val, unit, self._exponent)
        elif (self._unit == self.standard):
            val = self.from_standard_conversions[unit](self._value)
            return Temperature(val, unit, self._exponent)
        else:
            standard_val = self.to_standard_conversions[self._unit](self._value)
            val = self.from_standard_conversions[unit](standard_val)
            return Temperature(val, unit, self._exponent)
        
            
        

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
    
        
        