from typing import Literal, TypeVar, Generic, Union

T = TypeVar('T')



# TODO implement unit conversions
class Unit:
    def __init__(self, value:float, unit: Generic[T]):
        self._value = value
        self._unit = unit
    def __repr__(self) -> str:
        return f"{self._value} {self._unit}"
    def __add__(self, other):
        if isinstance(other, self.__class__):
            if (self._unit == other._unit):
                return Unit(self._value + other._value, self._unit)
        elif isinstance(other, Union[int, float]):
            return Unit(self._value + other, self._unit)
        else:
            raise TypeError(f"Adding class {self.__class__} and {other.__class__} is unsupported")
    def __sub__(self,other):
        if isinstance(other, self.__class__):
            if (self._unit == other._unit):
                return Unit(self._value - other._value, self._unit)
        elif isinstance(other, Union[int, float]):
            return Unit(self._value - other, self._unit)
        else:
            raise TypeError(f"Subtracting class {self.__class__} and {other.__class__} is unsupported")
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            if (self._unit == other._unit):
                return Unit(self._value / other._value, self._unit)
        elif isinstance(other, Union[int, float]):
            return Unit(self._value / other, self._unit)
        else:
            raise TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
        
        


class Temperature(Unit):
    def __init__(self, value:float, unit: Literal["K", "C", "F", "R"]):
        super().__init__(value, unit)

class Pressure(Unit):
    def __init__(self, value:float, unit: Literal["Pa", "kPa", "bar", "atm", "mmHg", "torr"]):
        super().__init__(value, unit)
    
class BaseLength(Unit):
    def __init__(self,value:float, unit: Literal["m", "ft"]):
        super().__init__(value, unit)
        

        
        