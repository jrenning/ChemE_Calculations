from typing import Literal, TypeVar, Generic, Union, List

T = TypeVar('T')





# TODO implement unit conversions
# base unit class only meant for units with fractions or multiplications 
class Unit:
    def __init__(self, value:float=0.0,unit: Generic[T]="unitless", exponent: int=1):
        self._value = value
        self._unit = unit
        self._exponent = exponent
        
    def __repr__(self) -> str:
        if self._exponent == 1:
            return f"{self._value} {self._unit}"
        else:
            return f"{self._value} {self._unit}^{self._exponent}"
        
    def __eq__(self, other)-> bool:
        if self.__class__ == other.__class__ or other.__class__ == Unit:
            if self._value == other._value:
                if self._unit == other._unit:
                    if self._exponent == other._exponent:
                        return True
        return False
    def __add__(self, other):
        if isinstance(other, self.__class__):
            if (self._unit == other._unit) and (self._exponent == other._exponent):
                return Unit(self._value + other._value, self._unit, self._exponent)
        elif isinstance(other, Union[int, float]):
            return Unit( self._value + other,self._unit)
        else:
            raise TypeError(f"Adding class {self.__class__} and {other.__class__} is unsupported")
    def __sub__(self,other):
        if isinstance(other, self.__class__):
            if (self._unit == other._unit) and (self._exponent == other._exponent):
                return Unit( self._value - other._value, self._unit,  self._exponent)
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

# basic class of unit without a value attached, used for constructing multi units by hand 
class BaseUnit:
    def __init__(self,unit: Generic[T], exponent: int = 1):
        self._unit = unit
        self._exponent = exponent
    def __repr__(self):
        return f"{self._unit}^{self._exponent}"
    def __eq__(self, other):
        if self._unit == other._unit and self._exponent == other._exponent:
            return True
        return False
    def __hash__(self):
        return hash(str(self))
class MultiUnit:
    def __init__(self, value: float, top_half: List[BaseUnit], bottom_half: List[BaseUnit]):
        self._top_half = top_half
        self._bottom_half = bottom_half
        self._value = value
    
    @staticmethod   
    def cancel_units(top_half: List[BaseUnit], bottom_half: List[BaseUnit]):
        for u1 in top_half:
            for u2 in bottom_half:
                if u1._unit == u2._unit:
                    u1._exponent -= u2._exponent
                    u2._exponent = 0
                    
        final_top_half = []   
        final_bottom_half = []          
        for unit in top_half:
            if unit._exponent == 0:
                pass
            elif unit._exponent < 0:
                final_bottom_half.append(BaseUnit(unit._unit,-unit._exponent))
            else:
                final_top_half.append(unit)
                

        # update units from the bottom half 
        for unit in bottom_half:
            if unit._exponent != 0:
                final_bottom_half.append(unit)
        return  final_top_half, final_bottom_half
    @staticmethod
    def combine_units(unit_list: List[BaseUnit]):
        for i, u1 in enumerate(unit_list):
            for j, u2 in enumerate(unit_list):
                if u1._unit == u2._unit and i != j:
                    u1._exponent += u2._exponent
                    u2._exponent = 0
        return unit_list
        
    def __repr__(self):
        top_string = " * ".join(f"{x._unit}^{x._exponent}" if x._exponent != 1 else f"{x._unit}" for x in self._top_half)
        if self._bottom_half:
            bottom_string = " * ".join(f"{x._unit}^{x._exponent}" if x._exponent != 1 else f"{x._unit}" for x in self._bottom_half)
            return f"{self._value} {top_string} / {bottom_string}"
        else:
            return f"{self._value} {top_string}"
    
    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self._value == other._value:
                if set(self._top_half) == set(other._top_half):
                    if set(self._bottom_half) == set(other._bottom_half):
                        return True
        return False
    def __add__(self, other):
        if self.__class__ == other.__class__:
            if self._top_half == other._top_half and self._bottom_half == other._bottom_half:
                return MultiUnit(value= self._value + other._value, top_half=self._top_half, bottom_half=self._bottom_half)
        else:
            raise TypeError(f"Adding class {self.__class__} and {other.__class__} is unsupported")
    def __sub__(self, other):
        if self.__class__ == other.__class__:
            if self._top_half == other._top_half and self._bottom_half == other._bottom_half:
                return MultiUnit(value= self._value - other._value, top_half=self._top_half, bottom_half=self._bottom_half)
        else:
            raise TypeError(f"Subtracting class {self.__class__} and {other.__class__} is unsupported")
    def __truediv__(self,other):
        
        # same class 
        if self.__class__ == other.__class__:
            # same units 
            if self._top_half == other._top_half and self._bottom_half == other._bottom_half:
                return self._value / other._value
            else:
                new_top_half = self._top_half + other._bottom_half
                new_bottom_half = self._bottom_half + other._top_half
                
                final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
                
            
                # if all units cancel
                if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                    return self._value / other._value
                
                return MultiUnit(self._value / other._value, final_top_half, final_bottom_half)
        elif other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
            new_top_half = self._top_half 
            new_bottom_half = self._bottom_half + [BaseUnit(other._unit, other._exponent)]
            
            new_bottom_half = self.combine_units(new_bottom_half)
                        
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
                    
            
            return MultiUnit(self._value / other._value, final_top_half, final_bottom_half)
        
        elif isinstance(other, Union[int, float]):
            return MultiUnit(self._value / other, self._top_half, self._bottom_half)
        else:
            TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
        
    def __mul__(self,other):

        if self.__class__ == other.__class__:
            new_top_half = self._top_half + other._top_half
            new_bottom_half = self._bottom_half + other._bottom_half
            
            new_top_half = self.combine_units(new_top_half)
            new_bottom_half = self.combine_units(new_bottom_half)
            
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            return MultiUnit(self._value * other._value, final_top_half, final_bottom_half)
        elif other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
            new_top_half = self._top_half + [BaseUnit(other._unit, other._exponent)]
            new_bottom_half = self._bottom_half
            
            new_top_half = self.combine_units(new_top_half)
                        
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
                            
            return MultiUnit(self._value * other._value, final_top_half, final_bottom_half)
        elif isinstance(other, Union[int, float]):
            return MultiUnit(self._value * other, self._top_half, self._bottom_half)
        else:
            TypeError(f"Multiplying class {self.__class__} and {other.__class__} is unsupported")
                
    def __rtruediv__(self,other):
        if isinstance(other, Union[int, float]):
            return MultiUnit(other/self._value,self._bottom_half, self._top_half)
        else:
            raise TypeError(f"Dividing class {other.__class__} and {self.__class__} is unsupported")
    def __rmul__(self, other):
        if isinstance(other, Union[int, float]):
            return MultiUnit(other * self._value,self._top_half, self._bottom_half)
        else:
            raise TypeError(f"Multiplying class {other.__class__} and {self.__class__} is unsupported")
            
            

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
    def __init__(self, value:float, unit: Literal["K", "C", "F", "R"]="K", exponent: int =1):
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
    def __init__(self, value:float, unit: Literal["Pa", "kPa", "bar", "atm", "mmHg", "torr"]="atm",
                 exponent: int = 1):
        super().__init__(value, unit, exponent)
    
class BaseLength(Unit):
    def __init__(self,value:float, unit: Literal["m", "ft"],
                 exponent: int = 1):
        super().__init__(value, unit, exponent)

class Time(Unit):
    def __init__(self,value:float, unit: Literal["s", "min", "hr", "day"],
                exponent: int = 1):
        super().__init__(value, unit, exponent)
    
        
class Velocity(MultiUnit):
    def __init__(self,value:float, length_unit: Literal["m", "ft"], time_unit: Literal["s", "min", "hr", "day"],
                 exponent: int = 1):
        super().__init__(value, top_half=[BaseUnit(length_unit._unit)], bottom_half=[BaseUnit(time_unit._unit)])




        
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
    
        
        