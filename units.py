from typing import Literal, TypeVar, Generic, Union, List
from utility import powerset
from copy import deepcopy
from functools import reduce

T = TypeVar('T')

# milli. centi, deci, kilo, mega
prefixes = ["m", "c", "d", "k", "M"]

TemperateUnits = ["K", "C", "R", "F"]
TemperatureDict = {k:"Temperature" for k in TemperateUnits}

LengthUnits = ["m"]
LengthUnits = [f"{x}{y}" for x in prefixes for y in LengthUnits]
LengthUnits.extend(["m", "ft"])
LengthDict = { k:"Length" for k in LengthUnits }

CurrentUnits = ["A"]
CurrentDict = {"A":"Current"}

TimeUnits = ["s", "min", "hr", "day"]
TimeDict = {k:"Time" for k in TimeUnits}

MassUnits = ["g"]
MassUnits = [f"{x}{y}" for x in prefixes for y in MassUnits]
MassUnits.extend(["g", "lb"])
MassDict = { k:"Mass" for k in MassUnits }

# registers units to type of unit it is 
UNIT_REGISTRY = {
    **TemperatureDict,
    **LengthDict,
    **MassDict,
    **CurrentDict,
    **TimeDict
}

LengthUnit = Literal["m", "ft"]

DECONSTRUCTABLE_UNITS = {
    "Pa": "kg/m*s^2",
    "J": "kg*m^2/s^2",
    "W": "J/s",
}
 
class Unit:
    """
    A class meant to represent a basic unit with a value and exponent
    
    Attributes
    ----------
    :param value: float
        the value of the unit
    :param unit: str
        the string representing the unit
    :param exponent: int = 1
        the number representing the exponent of the unit ie m^2
    
    
    """
    def __init__(self, value:float=0.0,unit: Generic[T]="unitless", exponent: int=1):
        """Constructor for the Unit class

        :param value: value of the unit, defaults to 0.0
        :type value: float, optional
        :param unit: unit string, defaults to "unitless"
        :type unit: Generic[T], optional
        :param exponent: exponent of the unit, defaults to 1
        :type exponent: int, optional
        """
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
                return self.__class__(self._value + other._value, self._unit, self._exponent)
        elif isinstance(other, Union[int, float]):
            return self.__class__( self._value + other,self._unit)
        else:
            raise TypeError(f"Adding class {self.__class__} and {other.__class__} is unsupported")
    def __sub__(self,other):
        if isinstance(other, self.__class__):
            if (self._unit == other._unit) and (self._exponent == other._exponent):
                return self.__class__( self._value - other._value, self._unit,  self._exponent)
        elif isinstance(other, Union[int, float]):
            return self.__class__(self._value - other, self._unit)
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
                    return self.__class__(self._value / other._value, self._unit, exponent_remainder)
            else:
                return MultiUnit( top_half=[BaseUnit(self._unit, self._exponent)], bottom_half=[BaseUnit(other._unit, other._exponent)], value=self._value / other._value)
        # if both units
        elif other.__class__.__bases__[0] == Unit:
            return MultiUnit( top_half=[BaseUnit(self._unit, self._exponent)], bottom_half=[BaseUnit(other._unit, other._exponent)], value=self._value / other._value)
        elif isinstance(other, Union[int, float]):
            return self.__class__(self._value / other, self._unit)
        else:
            raise TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
    def __mul__(self, other):
        # same class 
        if self.__class__ == other.__class__:
            if (self._unit == other._unit):
                    return self.__class__(self._value * other._value, self._unit, self._exponent + other._exponent)
        # if both units
        if other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
                return MultiUnit(top_half=[self, other], bottom_half=None, value=self._value * other._value)
        elif isinstance(other, Union[int, float]):
            return self.__class__(self._value * other, self._unit)
        else:
            raise TypeError(f"Multiplying class {self.__class__} and {other.__class__} is unsupported")
    
    def __rmul__(self, other):
        if isinstance(other, Union[int, float]):
            return self.__class__(self._value * other, self._unit)
        else:
            raise TypeError(f"Multiplying class {self.__class__} and {other.__class__} is unsupported")
            
    def __pow__(self, other):
        if isinstance(other, Union[int, float]):
            return self.__class__(self._value**other, self._unit, self._exponent*other)
        else:
            raise TypeError(f"Exponentiations with class {self.__class__} and {other.__class__} is unsupported")
    
    def __neg__(self):
        return self.__class__(-self._value, self._unit, self._exponent)
    def convert_to(self,unit: str, inplace: bool =False):
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
            try:
                standard_val = self.to_standard_conversions[self._unit](self._value)
            except KeyError as _:
                raise TypeError(f"{self._unit} can not be converted to {unit}")
                
            val = self.from_standard_conversions[unit](standard_val)
            if inplace:
                return self.__class__.__init__(self, val, unit, self._exponent)
            return self.__class__(val, unit, self._exponent)

# basic class of unit without a value attached, used for constructing multi units by hand 
class BaseUnit:
    """Class representing a unit without a value, usually just for internal use
    
    
    """
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
    def __init__(self, value: float, unit: str="", *,  top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        # if passed a unit construct the class from it 
        if unit:
            top_half, bottom_half = self.parse_units(unit)
        # else use provided keys
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
                unit, exponent = utop.split("^")
            else:
                exponent = 1
                unit = utop
            final_top_units.append(unit)
            final_top_exponents.append(int(exponent))
        for ubot in bottom_units:
            if "^" in ubot:
                unit, exponent = ubot.split("^")
            else:
                exponent = 1
                unit = ubot
            final_bottom_units.append(unit)
            final_bottom_exponents.append(int(exponent))
        
        top_half = [BaseUnit(x,y) for x,y in zip(final_top_units, final_top_exponents)]
        bottom_half = [BaseUnit(x,y) for x,y in zip(final_bottom_units, final_bottom_exponents)]
        return top_half, bottom_half
    
    def deconstruct_units(self, top_list: List[BaseUnit], bottom_list: List[BaseUnit]):
        new_top_list = []
        new_bottom_list = []
        
        for unit in top_list:
            if unit._unit in DECONSTRUCTABLE_UNITS.keys():
                new_string = DECONSTRUCTABLE_UNITS[unit._unit]
                top_half, bottom_half = self.parse_units(new_string)
                new_top_list.extend(top_half)
                new_bottom_list.extend(bottom_half)
            else:
                new_top_list.append(unit)
                
        for unit in bottom_list:
            if unit._unit in DECONSTRUCTABLE_UNITS.keys():
                new_string = DECONSTRUCTABLE_UNITS[unit._unit]

                extra_top_list, extra_bottom_list = self.parse_units(new_string)
                new_bottom_list.extend(extra_top_list)
                new_top_list.extend(extra_bottom_list)
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
                top_base_units, bottom_base_units = self.parse_units(combo)
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
    def get_unit_class(unit: str):
        try:
            unit_class = UNIT_REGISTRY[unit]
        except KeyError as _:
            raise KeyError(f"{unit} is not a valid unit in the registry")
        
        match unit_class:
            case "Length":
                return Length
            case "Mass":
                return Mass
            case "Time":
                return Time
            case "Temperature":
                return Temperature
            case "Current":
                return Current
            case _:
                raise KeyError(f"UNIT REGISTRY is improperly formatted")
            
    def convert_to(self, unit: str, inplace: bool =False):
        # if converting to the same unit return 
        if (self.__repr__() == unit):
            return self
        
        # TODO make it so it doesn't error flipped units
        convert_top, convert_bottom = self.parse_units(unit)
        # get top and bottom half of self 
        new_top_half = [self.get_unit_class(x._unit)(1, x._unit, x._exponent) for x in self._top_half]
        new_bottom_half = [self.get_unit_class(x._unit)(1,x._unit, x._exponent) for x in self._bottom_half]
        
        top_convert_units = [x._unit for x in convert_top]
        bottom_convert_units = [x._unit for x in convert_bottom]
        
        top_converted = [x.convert_to(y) for x in new_top_half for y in top_convert_units]
        bottom_converted = [x.convert_to(y) for x in new_bottom_half for y in bottom_convert_units]
        top_nums = [x._value for x in top_converted]
        bottom_nums = [x._value for x in bottom_converted]
        
        top_factor = reduce((lambda x, y: x * y), top_nums)
        bottom_factor = reduce((lambda x, y: x * y), bottom_nums)
        
        if inplace:
            return self.__class__.__init__(self,self._value*(top_factor/bottom_factor), unit)
        else:
            return self.__class__(self._value*(top_factor/bottom_factor), unit)
        
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
                new_top_half = deepcopy(self._top_half) + deepcopy(other._bottom_half)
                new_bottom_half = deepcopy(self._bottom_half) + deepcopy(other._top_half)
                
                final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
                
                final_top_half, final_bottom_half = self.simplify_units(final_top_half, final_bottom_half)
                # if all units cancel
                if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                    return self._value / other._value
                
                #if just left with one unit
                if len(final_top_half) == 1 and len(final_bottom_half) == 0:
                    return Unit(self._value / other._value, final_top_half[0]._unit, final_top_half[0]._exponent)
                
                return MultiUnit(self._value / other._value, top_half=final_top_half, bottom_half=final_bottom_half)
        elif other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
            new_top_half = deepcopy(self._top_half)
            new_bottom_half = deepcopy(self._bottom_half) + [BaseUnit(other._unit, other._exponent)]
            
            new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half)
            
            new_bottom_half = self.combine_units(new_bottom_half)
                        
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            
            final_top_half, final_bottom_half = self.simplify_units(final_top_half, final_bottom_half)
            
            # if all units cancel
            if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                return self._value / other._value
            
            #if just left with one unit
            if len(final_top_half) == 1 and len(final_bottom_half) == 0:
                return Unit(self._value / other._value, final_top_half[0]._unit, final_top_half[0]._exponent)
            
            return MultiUnit(self._value / other._value, top_half=final_top_half, bottom_half=final_bottom_half)
        
        elif isinstance(other, Union[int, float]):
            return MultiUnit(self._value / other, top_half=self._top_half, bottom_half=self._bottom_half)
        else:
            TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
        
    def __mul__(self,other):

        if self.__class__ == other.__class__:
            
            new_top_half = deepcopy(self._top_half) + deepcopy(other._top_half)
            new_bottom_half = deepcopy(self._bottom_half) + deepcopy(other._bottom_half)
            
            new_top_half = self.combine_units(new_top_half)
            new_bottom_half = self.combine_units(new_bottom_half)
            
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            return MultiUnit(self._value * other._value, top_half=final_top_half, bottom_half=final_bottom_half)
        elif other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
            new_top_half = deepcopy(self._top_half) + [BaseUnit(other._unit, other._exponent)]
            new_bottom_half = deepcopy(self._bottom_half)
            
            new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half)
            
            new_top_half = self.combine_units(new_top_half)
            new_bottom_half = self.combine_units(new_bottom_half)
                        
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            
            final_top_half, final_bottom_half = self.simplify_units(final_top_half, final_bottom_half)
            # if all units cancel
            if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                return other._value * self._value
            
            #if just left with one unit
            if len(final_top_half) == 1 and len(final_bottom_half) == 0:
                return Unit(other._value * self._value, final_top_half[0]._unit, final_top_half[0]._exponent)
                            
            return MultiUnit(other._value * self._value, top_half=final_top_half, bottom_half=final_bottom_half)
        elif isinstance(other, Union[int, float]):
            return MultiUnit(self._value * other, top_half=self._top_half, bottom_half=self._bottom_half)
        else:
            TypeError(f"Multiplying class {self.__class__} and {other.__class__} is unsupported")
                
    def __rtruediv__(self,other):
        if isinstance(other, Union[int, float]):
            return MultiUnit(other/self._value,top_half=self._bottom_half, bottom_half=self._top_half)
        elif other.__class__ == Unit or other.__class__.__bases__[0] == Unit:
            
            
            new_top_half = self._top_half.deepcopy()
            new_bottom_half = self._bottom_half.deepcopy()
            # append unit to the bottom half 
            new_bottom_half.append(BaseUnit(other._unit, other._exponent))
            # swap halfs 
            new_top_half, new_bottom_half = new_bottom_half, new_top_half
            

            
            new_top_half = self.combine_units(new_top_half)
                        
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            
            # if all units cancel
            if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                return other._value / self._value
            
            #if just left with one unit
            if len(final_top_half) == 1 and len(final_bottom_half) == 0:
                return Unit(self._value / other._value, final_top_half[0]._unit, final_top_half[0]._exponent)
                            
            return MultiUnit(self._value * other._value, top_half=final_top_half, bottom_half=final_bottom_half)
            
        
        else:
            raise TypeError(f"Dividing class {other.__class__} and {self.__class__} is unsupported")
    def __rmul__(self, other):
        if isinstance(other, Union[int, float]):
            return MultiUnit(other * self._value,top_half=self._top_half, bottom_half=self._bottom_half)
        else:
            raise TypeError(f"Multiplying class {other.__class__} and {self.__class__} is unsupported")
    def __pow__(self, other):
        if isinstance(other, Union[int, float]):
            for u1 in self._top_half:
                u1._exponent *= other
            for u2 in self._bottom_half:
                u2._exponent *= other
            return MultiUnit(self._value**other,top_half=self._top_half, bottom_half=self._bottom_half)
        raise TypeError(f"Exponentiating class {other.__class__} and {self.__class__} is unsupported")
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
    
class Length(Unit):
    standard: str = "m"
    # from target unit to standard unit 
    to_standard_conversions = {
        "ft": lambda x: x*0.3048,
        "mm": lambda x: x/1000,
        "cm": lambda x: x/100,
        "dm": lambda x: x/10,
        "km": lambda x: x*1000
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "ft": lambda x: x*3.28084,
        "mm": lambda x: x*1000,
        "cm": lambda x: x*100,
        "dm": lambda x: x*10,
        "km": lambda x: x/1000
        
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

class Mass(Unit):
    standard: str = "kg"
    # from target unit to standard unit 
    to_standard_conversions = {
        "lb": lambda x: x*0.453592
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "lb": lambda x: x*2.20462
    }
    def __init__(self,value:float, unit: Literal["kg", "lb"],
                exponent: int = 1):
        super().__init__(value, unit, exponent)
          
          
class Current(Unit):
    standard: str = "A"
    def __init__(self,value:float, unit: Literal["A"],
                exponent: int = 1):
        super().__init__(value, unit, exponent)
class Velocity(MultiUnit):
    def __init__(self,value:float, unit: str, *, length_unit: Literal["m", "ft"]="m", time_unit: Literal["s", "min", "hr", "day"]="s"):
        super().__init__(value, unit)


class DynamicViscosity(MultiUnit):
    standard: str = "cP"
    # from target unit to standard unit 
    to_standard_conversions = {
        "kg/m*s": lambda x: x,
        "kg/cm*s": lambda x: x*100
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "kg/m*s": lambda x: x,
        "kg/cm*s": lambda x: x/100
    }
    def __init__(self, value, unit=Literal["cP", "kg/m*s", "cm/m*s"]):
        if unit == "cP":
            unit_string = "kg/m*s"
            super().__init__(value/1000,unit_string)
        else:
            super().__init__(value, unit)
    


        
def getR_constant(temperature_units: Literal["K", "C", "F", "R"],
                  volume_units: Literal["cm^3", "m^3", "L"],
                  pressure_units: Literal["Pa", "kPa", "bar", "atm", "mmHg", "torr"],
                  generic=False):
    if generic:
        return MultiUnit(8.314, "J/mol*K")
    if volume_units == "m^3" and pressure_units == "Pa" and temperature_units == "K":
        return MultiUnit(8.314, "m^3*Pa/mol*K")
    if volume_units == "L" and pressure_units == "atm" and temperature_units == "K":
        return MultiUnit(0.08205, "L*atm/mol*K")
    if volume_units == "m^3" and pressure_units == "atm" and temperature_units == "K":
        return MultiUnit(8.205746E-5, "m^3*atm/mol*K")
    
    raise ValueError("The units supplied to R are not defined in a known constant")
    
        
        