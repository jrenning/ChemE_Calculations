from typing import Literal, TypeVar, Generic, Union, List
from utility import powerset

T = TypeVar('T')

TemperateUnits = ["K", "C", "R", "F"]
LengthUnit = Literal["m", "ft"]

DECONSTRUCTABLE_UNITS = {
    "Pa": "kg/m*s^2",
    "W": "J/s",
    
    
}



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
    def convert_to(self,unit, inplace=False):
        if (self._unit == unit):
            return self
        if (unit == self.standard):
            val = self.to_standard_conversions[self._unit](self._value)
            if inplace:
                return self.__class__.__init__(self, val, unit, self._exponent)
            return self.__class__(val, unit, self._exponent)
        elif (self._unit == self.standard):
            val = self.from_standard_conversions[unit](self._value)
            if inplace:
                return self.__class__.__init__(self, val, unit, self._exponent)
            return self.__class__(val, unit, self._exponent)
        else:
            standard_val = self.to_standard_conversions[self._unit](self._value)
            val = self.from_standard_conversions[unit](standard_val)
            if inplace:
                return self.__class__.__init__(self, val, unit, self._exponent)
            return self.__class__(val, unit, self._exponent)

# basic class of unit without a value attached, used for constructing multi units by hand 
class BaseUnit:
    def __init__(self,unit: Generic[T], exponent: int = 1):
        self._unit = unit
        self._exponent = exponent
    def __repr__(self):
        if self._exponent != 1:
            return f"{self._unit}^{self._exponent}"
        else:
            return f"{self._unit}"
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
    
    def deconstruct_units(self, top_list: List[BaseUnit], bottom_list: List[BaseUnit]):
        new_top_list = []
        new_bottom_list = []
        
        for unit in top_list:
            if unit._unit in DECONSTRUCTABLE_UNITS.keys():
                new_string = DECONSTRUCTABLE_UNITS[unit._unit]
                (final_top_units, final_top_exponents,
                 final_bottom_units, final_bottom_exponents) = self.parse_units(new_string)
                for unit, exponent in zip(final_top_units, final_top_exponents):
                    new_top_list.append(BaseUnit(unit, exponent))
                for unit, exponent in zip(final_bottom_units, final_bottom_exponents):
                    new_bottom_list.append(BaseUnit(unit, exponent))
            else:
                new_top_list.append(unit)
                
        for unit in bottom_list:
            if unit._unit in DECONSTRUCTABLE_UNITS.keys():
                new_string = DECONSTRUCTABLE_UNITS[unit._unit]

                (final_top_units, final_top_exponents,
                 final_bottom_units, final_bottom_exponents) = self.parse_units(new_string)
                for unit, exponent in zip(final_top_units, final_top_exponents):
                    new_bottom_list.append(BaseUnit(unit, exponent))
                for unit, exponent in zip(final_bottom_units, final_bottom_exponents):
                    new_top_list.append(BaseUnit(unit, exponent))
            else:
                new_bottom_list.append(unit)

        
        return new_top_list, new_bottom_list
    
    def simplify_units(self, top_list: List[BaseUnit], bottom_list: List[BaseUnit]):
        top_unit_list = [x.__repr__() for x in top_list]
        bottom_unit_list = [x.__repr__() for x in bottom_list]
        # get possible combos
        possible_tops = powerset(top_unit_list)
        possible_bottoms = powerset(bottom_unit_list)
        
        
        tops = ["*".join(x) for x in possible_tops]
        bottoms = ["*".join(x) for x in possible_bottoms]
        
        # add flipped versions of everything
        topy_copy = tops.copy()
        for top in topy_copy:
            if "*" in top:
                split = top.split("*")
                if len(split) == 2:
                    bottoms.append(f"{split[1]}*{split[0]}")
        bot_copy = bottoms.copy()   
        for bot in bot_copy:
            if "*" in bot:
                split = bot.split("*")
                # no composite unit has a length of units greater than 2
                if len(split) == 2:
                    bottoms.append(f"{split[1]}*{split[0]}")
                
                
        combos = [f"{x}/{y}" for x in tops for y in bottoms]
        final_top = []
        final_bottom = []
        for combo in combos:
            if combo in DECONSTRUCTABLE_UNITS.values():
                # get key of the value
                value = [i for i in DECONSTRUCTABLE_UNITS if DECONSTRUCTABLE_UNITS[i]==combo]
                (final_top_units, final_top_exponents,
                 final_bottom_units, final_bottom_exponents) = self.parse_units(combo)
                top_base_units = [BaseUnit(x,y) for x in final_top_units for y in final_top_exponents]
                bottom_base_units = [BaseUnit(x,y) for x in final_bottom_units for y in final_bottom_exponents]
                for u1 in top_list:
                    if u1 not in top_base_units:
                        final_top.append(u1)
                for u2 in bottom_list:
                    if u2 not in bottom_base_units:
                        final_bottom.append(u2)
                # append new simplified unit
                final_top.append(BaseUnit(value[0]))
                break
        # if no matches
        else:
            final_top = top_list
            final_bottom = bottom_list
            
        return final_top, final_bottom
        
        
                
            
            
        
    @staticmethod
    def parse_units(unit_string: str):
        top_half, bottom_half = unit_string.split("/")
        top_units = top_half.strip().split("*")
        bottom_units = bottom_half.strip().split("*")
        final_top_units = []
        final_top_exponents = []
        final_bottom_units = []
        final_bottom_exponents = []
        for utop in top_units:
            if "^" in utop:
                exponent, unit = utop.split("^")
            else:
                exponent = 1
                unit = utop
            final_top_units.append(unit)
            final_top_exponents.append(exponent)
        for ubot in bottom_units:
            if "^" in ubot:
                unit, exponent = ubot.split("^")
            else:
                exponent = 1
                unit = ubot
            final_bottom_units.append(unit)
            final_bottom_exponents.append(int(exponent))
        
        return final_top_units, final_top_exponents, final_bottom_units, final_bottom_exponents
        
    
        
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
                
                final_top_half, final_bottom_half = self.simplify_units(final_top_half, final_bottom_half)
                # if all units cancel
                if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                    return self._value / other._value
                
                return MultiUnit(self._value / other._value, final_top_half, final_bottom_half)
        elif other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
            new_top_half = self._top_half 
            new_bottom_half = self._bottom_half + [BaseUnit(other._unit, other._exponent)]
            
            new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half)
            
            new_bottom_half = self.combine_units(new_bottom_half)
                        
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            
            final_top_half, final_bottom_half = self.simplify_units(final_top_half, final_bottom_half)
            
            # if all units cancel
            if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                return self._value / other._value
            
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
        if unit not in TemperateUnits:
            raise TypeError(f"The unit of {unit} is not valid for temperature")
        super().__init__(value, unit, exponent)

        
            
        

class Pressure(Unit):
    standard: str = "atm"
    # from target unit to standard unit 
    to_standard_conversions = {
        "Pa": lambda x: x / 101325,
        "bar": lambda x: x*0.986923,
        "mmHg": lambda x: x/760,
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "Pa": lambda x: x*101325,
        "bar": lambda x: x*1.01325,
        "mmHg": lambda x: x * 760,
    }
    def __init__(self, value:float, unit: Literal["Pa", "kPa", "bar", "atm", "mmHg"]="atm",
                 exponent: int = 1):
        super().__init__(value, unit, exponent)
    
class BaseLength(Unit):
    standard: str = "m"
    # from target unit to standard unit 
    to_standard_conversions = {
        "ft": lambda x: x*0.3048
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "ft": lambda x: x*3.28084
    }
    def __init__(self,value:float, unit: Literal["m", "ft"],
                 exponent: int = 1):
        super().__init__(value, unit, exponent)

class Time(Unit):
    standard: str = "s"
    # from target unit to standard unit 
    to_standard_conversions = {
        "min": lambda x: x*60,
        "hr": lambda x: x*3600,
        "day": lambda x: x*(3600*24)
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "min": lambda x: x/60,
        "hr": lambda x: x/3600,
        "day": lambda x: x/(3600*24)
    }
    def __init__(self,value:float, unit: Literal["s", "min", "hr", "day"],
                exponent: int = 1):
        super().__init__(value, unit, exponent)
        
class Energy(Unit):
    standard: str = "J"
    # from target unit to standard unit 
    to_standard_conversions = {
        "BTU": lambda x: x*1055.056
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "BTU": lambda x: x/1055.056
    }
    def __init__(self,value:float, unit: Literal["J", "BTU"],
                exponent: int = 1):
        super().__init__(value, unit, exponent)
    
        
class Velocity(MultiUnit):
    def __init__(self,value:float, length_unit: Literal["m", "ft"], time_unit: Literal["s", "min", "hr", "day"]):
        super().__init__(value, top_half=[BaseUnit(length_unit)], bottom_half=[BaseUnit(time_unit)])


class ThermalConductivity(MultiUnit):
        def __init__(self,value:float, energy_unit: Literal["J", "BTU"], time_unit: Literal["s", "hr"],
                     length_unit: LengthUnit, temperature_unit: Literal['K', 'C', 'F', 'R']):
            super().__init__(value, top_half=[BaseUnit(energy_unit)], bottom_half=[BaseUnit(time_unit), BaseUnit(length_unit), BaseUnit(temperature_unit)])
    


        
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
    
        
        