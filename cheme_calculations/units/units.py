from math import floor
from pprint import pprint
from typing import Any, Callable, Literal, TypeVar, Generic, Union, List
from copy import deepcopy
from collections import defaultdict

from ._utility import remove_zero, to_sup, get_prefix




__all__ = ["Unit", "MultiUnit", "BaseUnit", "Temperature", "Pressure", 
           "Mass", "Current", "Energy", "Time", "Length","Volume","Area",  "UNIT_REGISTRY",
           "LengthUnits", "register_unit_from_existing"]

T = TypeVar('T')

class UnitConversionError(Exception):
    pass

class UnknownPrefix(Exception):
    pass

class IncorrectUnits(Exception):
    pass



    


# micro, milli, centi, deci, kilo, mega
prefixes = ["u", "m", "c", "d", "k", "M"]

# factors relative to no prefix 
prefix_factors = {
    "u": 1E-6,
    "m": .001,
    "c": .01,
    "d": .1,
    "k": 1000,
    "M": 1E6,
}

TemperateUnits = ["K", "C", "R", "F"]
TemperatureDict = {k:"Temperature" for k in TemperateUnits}

LengthUnits = ["m"]
LengthUnits = [f"{x}{y}" for x in prefixes for y in LengthUnits]
LengthUnits.extend(["m", "ft", "in", "yd", "mile"])
LengthDict = { k:"Length" for k in LengthUnits }

CurrentUnits = ["A"]
CurrentDict = {"A":"Current"}

TimeUnits = ["s", "min", "hr", "day"]
TimeDict = {k:"Time" for k in TimeUnits}

MassUnits = ["g"]
MassUnits = [f"{x}{y}" for x in prefixes for y in MassUnits]
MassUnits.extend(["g", "lb"])
MassDict = { k:"Mass" for k in MassUnits }

EnergyUnits = ["J"]
EnergyUnits = [f"{x}{y}" for x in prefixes for y in EnergyUnits]
EnergyUnits.extend(["J", "BTU"])
EnergyDict = {k: "Energy" for k in EnergyUnits}

PressureUnits = ["Pa"]
PressureUnits = [f"{x}{y}" for x in prefixes for y in PressureUnits]
PressureUnits.extend(["psi", "Pa", "atm", "bar", "mmHg"])
PressureDict = {k: "Pressure" for k in PressureUnits}

ForceUnits = ["N"]
ForceUnits = [f"{x}{y}" for x in prefixes for y in ForceUnits]
ForceUnits.extend(["N", "lbf"])
ForceDict = {k: "Force" for k in ForceUnits}

VolumeUnits = ["m^3", "L"]
VolumeUnits = [f"{x}{y}" for x in prefixes for y in VolumeUnits]
VolumeUnits.extend(["m^3", "ft^3", "L", "in^3"])
VolumeDict = {k: "Volume" for k in VolumeUnits}

AreaUnits = ["m^2"]
AreaUnits = [f"{x}{y}" for x in prefixes for y in AreaUnits]
AreaUnits.extend(["m^2", "ft^2", "acre", "in^2"])
AreaDict = {k: "Area" for k in AreaUnits}


AmountUnits = ["mol"]
AmountDict = {"mol": "Amount"}
# registers units to type of unit it is 
UNIT_REGISTRY = {
    **TemperatureDict,
    **LengthDict,
    **MassDict,
    **CurrentDict,
    **TimeDict,
    **EnergyDict,
    **PressureDict,
    **ForceDict,
    **VolumeDict,
    **AreaDict,
    **AmountDict,
}



DECONSTRUCTABLE_UNITS = {
    "Pa": "kg/m*s^2",
    "J": "kg*m^2/s^2",
    "W": "J/s",
    "psi": "lbf/in^2",
    "cP": "g/m*s",
    "C": "A*s",
    "V": "kg*m^2/s^3*A"
}

UNIT_SIMPLIFICATIONS = {
    "kg/s^3*K": "W/m^2*K",
    "kg/K*s^3": "W/m^2*K",
    "kg/s^3": "W/m^2",
}

UNIT_COMPOSITES = ["L", "acre"]

def register_unit_from_existing(new_unit:str, existing_unit:str, to_func: Callable, from_func: Callable):
    unit_class = MultiUnit.get_unit_class(existing_unit)
    
    if existing_unit != unit_class.standard:
        existing_to_standard = unit_class.to_standard_conversions[existing_unit]
        existing_from_standard = unit_class.from_standard_conversions[existing_unit]
        new_to_standard = lambda x: existing_to_standard(to_func(x))
        new_from_standard = lambda x: existing_from_standard(from_func(x))
    else:
        new_to_standard = to_func
        new_from_standard = from_func
    
    # update standards
    unit_class.to_standard_conversions[new_unit] = new_to_standard
    unit_class.from_standard_conversions[new_unit] = new_from_standard

 
class Unit:
    """ This is a class meant to represent a unit with a value and exponent.
    
    Should only consist of a singular unit ie Pa instead of kg/m*s^2
    
    :param value: The value for the given unit 
    :type value: float
    :param unit: A string representing the unit itself, defaults to ""
    :type unit: Generic[T]
    :param exponent: The exponent for the given unit, defaults to 1
    :type exponent: int
    :Example:
    
    >>> unit = Unit(5, "m", 2)
    >>> print(unit)
    >>> 5 m\u00b2
    """
    
    def __init__(self, value:float=0.0,unit: Generic[T]="", exponent: int=1):
        """Constructor for the Unit class 

        Args:
            value: _The value of the unit. Defaults to 0.0.
            unit: A string representing the unit. Defaults to "".
            exponent: The exponent of the given unit ie m^2 -> exponent = 2. Defaults to 1.
        """
        self._value = value
        self._unit = unit
        self._exponent = exponent
        
    def __repr__(self) -> str:
        if self._exponent == 1:
            return f"{self._value} {self._unit}"
        else:
            return f"{self._value} {self._unit}{to_sup(str(remove_zero(self._exponent)))}"
        
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
            else:
                raise TypeError(f"Adding unit {self._unit} and {other._unit} is unsupported")
        elif isinstance(other, Union[int, float]):
            return self.__class__( self._value + other,self._unit)
        else:
            raise TypeError(f"Adding class {self.__class__} and {other.__class__} is unsupported")
    def __sub__(self,other):
        if isinstance(other, self.__class__):
            if (self._unit == other._unit) and (self._exponent == other._exponent):
                return self.__class__( self._value - other._value, self._unit,  self._exponent)
            else:
               raise TypeError(f"Subtracting unit {self._unit} and {other._unit} is unsupported") 
        elif isinstance(other, Union[int, float]):
            return self.__class__(self._value - other, self._unit)
        else:
            raise TypeError(f"Subtracting class {self.__class__} and {other.__class__} is unsupported")
    def __truediv__(self, other):
        # same class or other is just a unit
        if other.__class__ == self.__class__ or other.__class__ == Unit or other.__class__.__bases__[0] == Unit:
            if (self._unit == other._unit):
                exponent_remainder = self._exponent - other._exponent
                if exponent_remainder == 0:
                    return self._value / other._value
                else:
                    return self.__class__(self._value / other._value, self._unit, exponent_remainder)
            else:
                return MultiUnit( top_half=[BaseUnit(self._unit, self._exponent)], bottom_half=[BaseUnit(other._unit, other._exponent)], value=self._value / other._value)
        elif isinstance(other, Union[int, float]):
            return self.__class__(self._value / other, self._unit, self._exponent)
        elif other.__class__ == MultiUnit or other.__class__.__bases__[0] == MultiUnit:
            return MultiUnit.__rtruediv__(other, self)
        else:
            raise TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
    def __mul__(self, other):
        # same class 
        if self.__class__ == other.__class__:
            if (self._unit == other._unit):
                    return self.__class__(self._value * other._value, self._unit, self._exponent + other._exponent)
        # if both units
        if other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
                return MultiUnit(top_half=[BaseUnit(self._unit), BaseUnit(other._unit)], bottom_half=[], value=self._value * other._value)
        elif other.__class__ == MultiUnit or other.__class__.__bases__[0] == MultiUnit:
            return MultiUnit.__mul__(other, self)
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
        """Converts a unit to another given unit 

        :param unit: The unit to convert to 
        :type unit: str
        :param inplace:  whether the conversion should create a new object or not, defaults to False
        :type inplace: bool, optional
        :raises UnitConversionError: Raises an error if a unit can't be converted
        :return: Returns a unit of the same class as self withe new value and unit
        :rtype: self.type
        """
        if "^" in unit and self._unit not in UNIT_COMPOSITES:
            unit, exponent = unit.split("^")
            exponent = float(exponent)
            return_unit = unit
        elif self._unit in UNIT_COMPOSITES:
            unit = unit
            return_unit, exponent = unit.split("^")
            exponent = float(exponent)
        else:
            unit = unit
            return_unit = unit
            exponent = 1

        if (self._unit == unit):
            return self
        if (unit == self.standard):     

            val = self.to_standard_conversions[self._unit](self._value)**exponent
            if inplace:
                return self.__class__.__init__(self, val, return_unit, exponent)
            return self.__class__(val, return_unit, exponent)
        elif (self._unit == self.standard):
            val = self.from_standard_conversions[unit](self._value)**exponent
            if inplace:
                return self.__class__.__init__(self, val, return_unit, exponent)
            return self.__class__(val, return_unit, exponent)
        else:
            try:
                standard_val = self.to_standard_conversions[self._unit](self._value)**exponent
            except KeyError as _:
                raise UnitConversionError(f"{self._unit} can not be converted to {unit}")
                

            val = self.from_standard_conversions[unit](standard_val)**exponent
            if inplace:
                return self.__class__.__init__(self, val, return_unit, exponent)
            return self.__class__(val, return_unit, exponent)

# basic class of unit without a value attached, used for constructing multi units by hand 
class BaseUnit:
    """Class representing a unit without a value, only used within MultiUnit
    
    :param unit: A string representing the unit itself
    :type unit: Generic[T]
    :param exponent: The exponent of the given unit, defaults to 1
    :type exponent: int
    
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
    
    
    def __pow__(self, other):
        if isinstance(other, Union[int, float]):
                     
            return BaseUnit(self._unit, self._exponent*other)
        else:
            raise TypeError(f"Taking a base unit to a power with {other} is not allowed")
        



# only used when an equation uses alot of units and/or simplifying requires a non obvious step
def do_common_simplifications(top_half: List[BaseUnit], bottom_half: List[BaseUnit]):
    for unit in UNIT_SIMPLIFICATIONS.keys():
        convert_top_half, convert_bottom_half = MultiUnit.parse_units(unit)
        
        if convert_top_half == top_half and convert_bottom_half == bottom_half:
            new_top_half, new_bottom_half = MultiUnit.parse_units(UNIT_SIMPLIFICATIONS[unit])
            return new_top_half, new_bottom_half
    
    return top_half, bottom_half
    
class MultiUnit:
    """ A class representing a unit that consists of multiple individual units
    
    :param value: The value for the unit
    :type value: float
    :param unit: A string representing the given unit, defaults to ""
    :type unit: str 
    :param top_half: A list of BaseUnits representing the top half of the unit, optional as this is created using the unit string
    :type top_half: List[class: BaseUnit]
    :param bottom_half: A list of BaseUnits representing the bottom half of the unit, optional as this is created using the unit string
    :type bottom_half: List[class: BaseUnit]
    
    :Example:
    
    >>> mu = MultiUnit(1, "kg*m/s^2)
    >>> 1 kg*m/s\u00b2
    """
    def __init__(self, value: float, unit: str="", *,  top_half: List[BaseUnit]=[], bottom_half: List[BaseUnit]=[]):
        # if passed a unit construct the class from it 
        if unit:
            top_half, bottom_half = self.parse_units(unit)
        # else use provided keys
        self._top_half = top_half
        self._bottom_half = bottom_half
        self._value = value
    
    
    @staticmethod
    def deconstruct_unit_prefixes(top_half: List[BaseUnit], bottom_half: List[BaseUnit])-> tuple:
        """Deconstructs a given top and bottom half of units to a representation without prefixes
        and returns a factor to account for it
        
        :param top_half: The top half of the MultiUnit
        :type top_half: List[BaseUnit]
        :param bottom_half: The bottom half of the MultiUnit
        :type bottom_half: List[BaseUnit]
        :raises UnknownPrefix: raises an error if a prefix is not within the known prefixes
        :return: list of base units for the top half passed in, list of base units for the bottom half passed in, factor to account for conversion
        :rtype: tuple(List[class: BaseUnit], List[class: BaseUnit], float)
        """
        # kg is special in that it is a prefixed unit that is the standard measurement
        top_prefixes = [get_prefix(x._unit)[0] if x._unit != "kg" else "" for x in top_half]
        top_base_units = [BaseUnit(get_prefix(x._unit)[1], x._exponent) if x._unit != "kg" else BaseUnit("kg", x._exponent) for x in top_half]
        bottom_prefixes = [get_prefix(x._unit)[0] if x._unit != "kg" else "" for x in bottom_half]
        bottom_base_units = [BaseUnit(get_prefix(x._unit)[1], x._exponent) if x._unit != "kg" else BaseUnit("kg", x._exponent) for x in bottom_half]
        
        factor = 1
        
        for i, prefix in enumerate(top_prefixes):
            # if not empty string
            if prefix:
                try:
                    factor *= prefix_factors[prefix]**top_base_units[i]._exponent
                except:
                    raise UnknownPrefix(f"The prefix of {prefix} is invalid")
        
        for i, prefix in enumerate(bottom_prefixes):
            # if not empty
            if prefix:
                try:
                    # inverse for bottom prefixes
                    factor *= (1/prefix_factors[prefix])**bottom_base_units[i]._exponent
                except:
                    raise UnknownPrefix(f"The prefix of {prefix} is invalid")
        
        return top_base_units, bottom_base_units, factor
                
    
    @staticmethod
    def reconstruct_unit_prefixes(top_half: List[BaseUnit], bottom_half: List[BaseUnit], factor:int):
        pass      

    
    @staticmethod   
    def cancel_units(top_half: List[BaseUnit], bottom_half: List[BaseUnit])-> tuple:
        """Cancels out the units for the given MultiUnit

        :param top_half: List of base units from the top half of the given MultiUnit
        :type top_half: List[class: BaseUnit]
        :param bottom_half: List of base units from the bottom half of the given MultiUnit
        :type bottom_half: List[BaseUnit]
        :return: new top half with canceled units, new bottom half with canceled units
        :rtype: tuple(List[class: BaseUnit], List[class: BaseUnit])
        
        :Example:
        
        >>> mu = MultiUnit(5, "kg*m/m^2")
        >>> top_half, bottom_half = mu.cancel_units(mu._top_half, mu._bottom_half)
        >>> print(top_half)
        >>> kg
        >>> print(bottom_half)
        >>> m
        """
        for u1 in top_half:
            for u2 in bottom_half:
                if u1._unit == u2._unit and u1._exponent != 0:
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
    def combine_units(unit_list: List[BaseUnit])-> List[BaseUnit]:
        """Combines units of the same name in the passed in list_

        :param unit_list: the unit list to be combined
        :type unit_list: List[BaseUnit]
        :return: The combined list of units
        :rtype: List[BaseUnit]
        
        :Example:
        
        >>> mu = MultiUnit(5, "m*m/s")
        >>> top_half = mu.combine_units(mu._top_half)
        >>> m\u00b2
        """
        for i, u1 in enumerate(unit_list):
            for j, u2 in enumerate(unit_list):
                if u1._unit == u2._unit and i != j:
                    u1._exponent += u2._exponent
                    u2._exponent = 0
        return unit_list
    
    @staticmethod
    def parse_units(unit_string: str)-> tuple:
        """Parses a given unit string to lists of top and bottom units

        :param unit_string: The unit to be parsed, use * for units multiplied and / to seperate the fraction
        :type unit_string: str
        :return: A tuple of the top half of base units then bottom half 
        :rtype: tuple(List[BaseUnit], List[BaseUnit])
        
        :Example:
        
        >>> top_half, bottom_half = MultiUnit.parse_units("m/s")
        >>> print(top_half)
        >>> m
        >>> print(bottom_half)
        >>> s
        
        """
        try:
            top_half, bottom_half = unit_string.split("/")
            bottom_units = bottom_half.strip().split("*")
            final_bottom_exponents = []
            final_bottom_units = []
            
            for ubot in bottom_units:
                if "^" in ubot:
                    unit, exponent = ubot.split("^")
                else:
                    exponent = 1
                    unit = ubot
                final_bottom_units.append(unit)
                final_bottom_exponents.append(float(exponent))
                
                        
            bottom_half = [BaseUnit(x,y) for x,y in zip(final_bottom_units, final_bottom_exponents)]
        # if no bottom half of units (really only a problem with W yeah)
        except ValueError:
            top_half = unit_string
            bottom_half = []
            
            
        top_units = top_half.strip().split("*")
        
        final_top_units = []
        final_top_exponents = []
        
        for utop in top_units:
            if "^" in utop:
                unit, exponent = utop.split("^")
            else:
                exponent = 1
                unit = utop
            final_top_units.append(unit)
            final_top_exponents.append(float(exponent))

        top_half = [BaseUnit(x,y) for x,y in zip(final_top_units, final_top_exponents)]
        return top_half, bottom_half
    
    
        
    
    def deconstruct_units(self, top_list: List[BaseUnit], bottom_list: List[BaseUnit], 
                          one_pass: bool = False)-> tuple:
        """A method to deconstruct composite units ie Pa to base units ie kg/m*s^2

        :param top_list: The top list of the given MultiUnit
        :type top_list: List[BaseUnit]
        :param bottom_list: The bottom list of the given MultiUnit
        :type bottom_list: List[BaseUnit]
        :param one_pass: if only one pass of deconstruct should happen ie W -> J/s instead of W -> kg*m^2/s^3, defaults to False
        :type one_pass: bool, optional
        :return: ne top half with units deconstructed, the bottom half with units deconstructed 
        :rtype: tuple(List[BaseUnit], List[BaseUnit])
        
        :Example:
        
        >>> mu = MultiUnit(1, "Pa/K")
        >>> top_half, bottom_half = mu.deconstruct_units(mu._top_half, mu._bottom_half)
        >>> print(top_half)
        >>> kg
        >>> print(bottom_half)
        >>> "K*m*s\u00b2"
        """
        
        top_list = deepcopy(top_list)
        bottom_list = deepcopy(bottom_list)
        
        # run a loop any time the last loop had a match 
        # catches units that decompose into units that decompose further 
        unit_match = True
        while unit_match:
            unit_match = False
            for i, unit in enumerate(top_list):
                if unit._unit in DECONSTRUCTABLE_UNITS.keys():
                    new_string = DECONSTRUCTABLE_UNITS[unit._unit]
                    top_half, bottom_half = self.parse_units(new_string)
                    # update exponents as well
                    top_half = [x**unit._exponent for x in top_half]
                    bottom_half = [x**unit._exponent for x in bottom_half]
                    # remove unit that got deconstructed 
                    del top_list[i]
                    # add new units
                    top_list.extend(top_half)
                    bottom_list.extend(bottom_half)
                    if not one_pass:
                        unit_match = True
                    
            for i, unit in enumerate(bottom_list):
                if unit._unit in DECONSTRUCTABLE_UNITS.keys():
                    new_string = DECONSTRUCTABLE_UNITS[unit._unit]

                    top_half, bottom_half = self.parse_units(new_string)
                    # update exponents as well
                    top_half = [x**unit._exponent for x in top_half]
                    bottom_half = [x**unit._exponent for x in bottom_half]
                    # delete old unit 
                    del bottom_list[i]
                    # add new units
                    bottom_list.extend(top_half)
                    top_list.extend(bottom_half)
                    if not one_pass:
                        unit_match = True
        
        return top_list, bottom_list
    
    def simplify_units(self, top_list: List[BaseUnit], bottom_list: List[BaseUnit])-> tuple:
        """MultiUnit class method to attempt to simplify units to a simpler form ie J/s to W
        
        Note: The current implementation will do simple simplifications right but will fail to
        recognize that a unit like kg/s^3 can be converted to W/m^2, which could technically
        be considered simpler 

        :param top_list: Top half of the MultiUnit
        :type top_list: List[BaseUnit]
        :param bottom_list: Bottom half of the MultiUnit
        :type bottom_list: List[BaseUnit]
        :return: (top list of simplified units, bottom list of simplified units)
        :rtype: tuple(List[BaseUnit], List[BaseUnit])
        
        :Example:
        
        >>> mu = MultiUnit("J/s")
        >>> top_half, bottom_half = mu.simplify_units(mu._top_half, mu._bottom_half)
        >>> print(top_half)
        >>> W
        >>> print(bottom_half)
        >>> ""
        """
        # TODO improve algorithm to also have preference for units with less exponents
        matches_dict = defaultdict(lambda: 0)
        
        unit_match = True
        while unit_match:
        
            for destructable_unit in DECONSTRUCTABLE_UNITS.values():

                top_base_units, bottom_base_units = self.parse_units(destructable_unit)
                # make a copy to standardize
                standard_base_top = deepcopy(top_base_units)
                standard_base_bottom = deepcopy(bottom_base_units)
                # standardize the unit (remove exponents)
                for u1 in standard_base_top:
                    u1._exponent = 1
                for u2 in standard_base_bottom:
                    u2._exponent = 1
                # standardize the top list passed in 
                standard_unit_top = deepcopy(top_list)
                standard_unit_bottom = deepcopy(bottom_list)
                for u1 in standard_unit_top:
                    u1._exponent = 1
                for u2 in standard_unit_bottom:
                    u2._exponent = 1
                
                # check if units in conversion unit are a subset of the unit list
                # if not moves on to next unit to check
                if not set(standard_base_top).issubset(set(standard_unit_top)) or not set(standard_base_bottom).issubset(set(standard_unit_bottom)):
                    continue
                
                
                # # check exponents (now that we know a match may exist)
                exp_match = True
                for u1 in top_base_units:
                    for u2 in top_list:
                        if u1._unit == u2._unit:
                            # units should be combined at this point so 
                            # each unit should exist only once in a top list / bottom list
                            if u2._exponent < u1._exponent:
                                exp_match = False
                    
                            # if no match try next unit
                if not exp_match:
                    continue
                
                exp_match = True
                for u1 in bottom_base_units:
                    for u2 in bottom_list:
                        if u1._unit == u2._unit:
                            # units should be combined at this point so 
                            # each unit should exist only once in a top list / bottom list
                            if u2._exponent < u1._exponent:
                                exp_match = False
                
                # if no match try next unit
                if not exp_match:
                    continue
                
                # know there is a match
                # find number of matches
                num_matches = 100
                for u1 in top_base_units:
                    for u2 in top_list:
                        if u1._unit == u2._unit:
                            matches = u2._exponent / u1._exponent
                            if matches < num_matches:
                                num_matches = matches
                for u1 in bottom_base_units:
                    for u2 in bottom_list:
                        if u1._unit == u2._unit:
                            matches = u2._exponent / u1._exponent
                            if matches < num_matches:
                                num_matches = matches
                                        # get key of the value
                value = [i for i in DECONSTRUCTABLE_UNITS if DECONSTRUCTABLE_UNITS[i]==destructable_unit]
                # add to matches dictionary
                matches_dict[value[0]] = num_matches   
                
                
            # no matches return original data 
            if matches_dict == {} or sum(matches_dict.values()) == 0:
                unit_match = False
                break
            
            
            # get max matches
            best_match_unit = max(matches_dict, key=matches_dict.get)
            
            best_match_to_replace = DECONSTRUCTABLE_UNITS[best_match_unit]
            best_match_val = matches_dict[best_match_unit]
            
            # get the best matches Base Unit lists
            top_base_units, bottom_base_units = self.parse_units(best_match_to_replace)
            
            # update exponent 
            for unit in top_base_units:
                unit._exponent *= best_match_val
            for unit in bottom_base_units:
                unit._exponent *= best_match_val  
            
            # add tp lists, then cancel units
            bottom_list.extend(top_base_units)
            top_list.extend(bottom_base_units)
            
            top_list, bottom_list = self.cancel_units(top_list, bottom_list)
        
            
            # add back simplified unit 
            top_list.append(BaseUnit(best_match_unit, best_match_val))
            
            # clear dict 
            matches_dict = {}
        
        # do final simplifications if possible
        top_list, bottom_list = do_common_simplifications(top_list, bottom_list)
        
        return top_list, bottom_list
        
    @staticmethod 
    def get_unit_class(unit: str):
        """Returns the class that a unit string corresponds to ie kg -> Mass

        :param unit: A string representing the unit, should be a singular unit ie m (not m*s)
        :type unit: str
        :raises KeyError: Raises a key error if the unit is not in the UNiT_REGISTRY
        :return: Returns the class of the given unit
        :rtype: Type[Length] | Type[Mass] | Type[Time] | Type[Temperature] | Type[Current] | Type[Energy] | Type[Pressure] | Type[Force] | Type[Volume]
        """
        try:
            unit_class = UNIT_REGISTRY[unit]
        except KeyError as _:
            raise KeyError(f"{unit} is not a valid unit in the registry")
        try:
            return UNIT_CLASSES[unit_class]
        except KeyError:
            raise KeyError(f"UNIT REGISTRY is improperly formatted")
        # match unit_class:
        #     case "Length":
        #         return Length
        #     case "Mass":
        #         return Mass
        #     case "Time":
        #         return Time
        #     case "Temperature":
        #         return Temperature
        #     case "Current":
        #         return Current
        #     case "Amount":
        #         return Amount
        #     case "Energy":
        #         return Energy
        #     case "Pressure":
        #         return Pressure
        #     case "Force":
        #         return Force
        #     case "Volume":
        #         return Volume
        #     case _:
        #         raise KeyError(f"UNIT REGISTRY is improperly formatted")
        
        
    def get_exponent_total(self)-> float:
        """Gets the exponent total of the given unit ie m^2/s^2 -> 4

        :return: The exponent total
        :rtype: float
        
        :Example:
        
        >>> mu = MultiUnit(5, "m^2/s^2")
        >>> total = mu.get_exponent_total()
        >>> 4
        """
        exponent_total = 0
        for u1 in self._top_half:
            exponent_total += u1._exponent
        for u2 in self._bottom_half:
            exponent_total += u2._exponent
            
        return exponent_total
    
    def base_to_unit(self, top_list: List[BaseUnit], bottom_list: List[BaseUnit]) -> List[Unit]:
        top_list = [self.get_unit_class(x._unit)(1, x._unit, x._exponent) for x in top_list]
        bottom_list = [self.get_unit_class(x._unit)(1, x._unit, x._exponent) for x in bottom_list]
        
        return top_list, bottom_list
        
    def convert_and_get_factor(self, unit: Unit):
        # temperature conversion works different in a multi unit
        if unit._unit in ["K", "C"]:
            unit._value *= (1*unit._exponent)
        elif unit._unit in ["R", "F"]:
            unit._value *= ((5/9)*unit._exponent)
        else:
            if unit._exponent == 1:
                unit.convert_to(unit.standard, True)
            else:
                unit.convert_to(f"{unit.standard}^{unit._exponent}", True)
        return unit
        
      
    def convert_to(self, unit: str, inplace: bool =False)-> Any | None:
        """Converts self from its unit to a new unit
        
        General algorithm for the conversion
        - (self / left side) English -> metric -> base units (SI)
        - This gives a conversion factor from self to base units
        - (unit / right side) English -> metric -> base units (SI)
        - This gives a conversion factor from unit to base units
        - Final value can then be found by using the (first factor / second factor) * og_value
        - Note: Improper conversions are found by comparing the base units 

        :param unit: String representing the unit to convert to
        :type unit: str
        :param inplace: Wether or not the function should return a new object(False), or modify the unit in place(True), defaults to False
        :type inplace: bool, optional
        :raises UnitConversionError: Raises an error if self can't be converted to the new unit 
        :return: A new MultiUnit with the new units | None
        :rtype: Self@MultiUnit | None
        """
        convert_top, convert_bottom = self.parse_units(unit)
        # deconstruct with one pass first to get rid of things like W
        convert_top, convert_bottom, prefix_factor_r = self.deconstruct_unit_prefixes(convert_top, convert_bottom)
        convert_top, convert_bottom = self.deconstruct_units(convert_top, convert_bottom, one_pass=True)
        convert_top, convert_bottom = self.base_to_unit(convert_top, convert_bottom)
        
        # get top and bottom half of self 
        # deconstruct with one pass first to get rid of things like W
        new_top_half, new_bottom_half, prefix_factor_l = self.deconstruct_unit_prefixes(deepcopy(self._top_half), deepcopy(self._bottom_half))
        new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half, one_pass=True)
        new_top_half, new_bottom_half = self.base_to_unit(new_top_half, new_bottom_half)
        
        

        # flow diagram for converting units
        # english -> SI -> base units -> SI -> english

        # first convert self unit to base units 
        left_factor = 1*prefix_factor_l
        for u1 in new_top_half:
            u1 = self.convert_and_get_factor(u1)
            left_factor *= u1._value
        for u1 in new_bottom_half:
            # temperature conversion works different in a multi unit
            u1 = self.convert_and_get_factor(u1)
            left_factor *= 1/u1._value
        
        # now deconstruct to base units 
        new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half)
        new_top_half, new_bottom_half = self.base_to_unit(new_top_half, new_bottom_half)
        
        # do the same steps to the right side 
        
        right_factor = 1*prefix_factor_r
        for u1 in convert_top:
            u1 = self.convert_and_get_factor(u1)
            right_factor *= u1._value
        for u1 in convert_bottom:
            u1 = self.convert_and_get_factor(u1)
            right_factor *= 1/(u1._value)
            
        convert_top, convert_bottom = self.deconstruct_units(convert_top, convert_bottom)
        convert_top, convert_bottom = self.base_to_unit(convert_top, convert_bottom)
        
        # now tally up and make sure the sides are the same 

        new_unit_dict = defaultdict(lambda: 0)
        self_unit_dict = defaultdict(lambda: 0)
        
        for u1 in convert_top:
            new_unit_dict[str(self.get_unit_class(u1._unit))] += 1*u1._exponent
        for u2 in convert_bottom:
            new_unit_dict[str(self.get_unit_class(u2._unit))] += -1*u2._exponent
        for u1 in new_top_half:
            self_unit_dict[str(self.get_unit_class(u1._unit))] += 1*u1._exponent
        for u2 in new_bottom_half:
            self_unit_dict[str(self.get_unit_class(u2._unit))] += -1*u2._exponent
            
        # remove any zeros 
        new_unit_dict = {k:v for k, v in new_unit_dict.items() if v != 0}
        self_unit_dict = {k:v for k, v in self_unit_dict.items() if v != 0}
            
        if new_unit_dict != self_unit_dict:
            raise UnitConversionError(f"The conversion from {self.__repr__()} to {unit} is not allowed")
        
        if inplace:
            return self.__class__.__init__(self,self._value*(left_factor/right_factor), unit)
        else:
            return self.__class__(self._value*(left_factor/right_factor), unit)
        
    def get_unit_string(self):
        try:
            top_string = " * ".join(f"{x._unit}{to_sup(str(remove_zero(x._exponent)))}" if x._exponent != 1 else f"{x._unit}" for x in self._top_half)
        except KeyError:
            top_string = " * ".join(f"{x._unit}^{x._exponent}" if x._exponent != 1 else f"{x._unit}" for x in self._top_half)
        if self._bottom_half:
            bottom_strings = []
            for x in self._bottom_half:
                # don't include exponent if its 1
                if x._exponent == 1:
                    bottom_strings.append(f"{x._unit}")
                # if bottom has negative units flip them to the top
                elif x._exponent < 0:
                    try:
                        # add * based on top string having anything in it 
                        if top_string == "":  
                            top_string += f"{x._unit}{to_sup(str(remove_zero(-x._exponent)))}"
                        else:
                            top_string += f" * {x._unit}{to_sup(str(remove_zero(-x._exponent)))}"
                    # error for to_sup
                    except KeyError:
                        top_string += f" * {x._unit}^{-x._exponent}"
                else:
                    try: 
                        bottom_strings.append(f"{x._unit}{to_sup(str(remove_zero(x._exponent)))}")
                    except KeyError:
                        bottom_strings.append(f"{x._unit}^{x._exponent}")
            bottom_string = " * ".join(bottom_strings)
            return f"{top_string} / {bottom_string}"
        else:
            return top_string
        
    def __repr__(self):
        unit_string = self.get_unit_string()
        return f"{self._value} {unit_string}"

    
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
               raise TypeError(f"Adding units {self.__repr__()} and {other.__repr__()} is unsupported") 
        else:
            raise TypeError(f"Adding class {self.__class__} and {other.__class__} is unsupported")
    def __sub__(self, other):
        if other.__class__ == MultiUnit or other.__class__.__bases__[0] == MultiUnit:
            if self._top_half == other._top_half and self._bottom_half == other._bottom_half:
                return MultiUnit(value= self._value - other._value, top_half=self._top_half, bottom_half=self._bottom_half)
            else:
                raise TypeError(f"Subtracting unit {self.__repr__()} and {other.__repr__()} is unsupported")
        else:
            raise TypeError(f"Subtracting class {self.__class__} and {other.__class__} is unsupported")
    def __truediv__(self,other):
        
        # same class or inherit from same class 
        if other.__class__.__bases__[0] == MultiUnit or other.__class__ == MultiUnit:
            # same units 
            if self._top_half == other._top_half and self._bottom_half == other._bottom_half:
                return self._value / other._value
            else:
                new_top_half = deepcopy(self._top_half) + deepcopy(other._bottom_half)
                new_bottom_half = deepcopy(self._bottom_half) + deepcopy(other._top_half)
                
                new_top_half, new_bottom_half, factor = self.deconstruct_unit_prefixes(new_top_half, new_bottom_half)
                
                new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half)
                
                new_bottom_half = self.combine_units(new_bottom_half)
                new_top_half = self.combine_units(new_top_half)
                
                final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
                
                final_top_half, final_bottom_half = self.simplify_units(final_top_half, final_bottom_half)
                
                # if all units cancel
                if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                    return (self._value / other._value)*factor
                
                #if just left with one unit
                if len(final_top_half) == 1 and len(final_bottom_half) == 0:
                    return Unit((self._value / other._value)*factor, final_top_half[0]._unit, final_top_half[0]._exponent)
                
                # one unit in the bottom
                if len(final_top_half) == 0 and len(final_bottom_half) == 1:
                    return Unit((self._value / other._value)*factor, final_bottom_half[0]._unit, -final_bottom_half[0]._exponent)
                
                return MultiUnit((self._value / other._value)*factor, top_half=final_top_half, bottom_half=final_bottom_half)
        elif other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
            new_top_half = deepcopy(self._top_half)
            new_bottom_half = deepcopy(self._bottom_half) + [BaseUnit(other._unit, other._exponent)]
            
            new_top_half, new_bottom_half, factor = self.deconstruct_unit_prefixes(new_top_half, new_bottom_half)
            
            new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half)
            
            new_bottom_half = self.combine_units(new_bottom_half)
                        
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            
            final_top_half, final_bottom_half = self.simplify_units(final_top_half, final_bottom_half)
            
            # if all units cancel
            if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                return (self._value / other._value)*factor
            
            #if just left with one unit
            if len(final_top_half) == 1 and len(final_bottom_half) == 0:
                return Unit((self._value / other._value)*factor, final_top_half[0]._unit, final_top_half[0]._exponent)
            
            # one unit in the bottom
            if len(final_top_half) == 0 and len(final_bottom_half) == 1:
                return Unit((self._value / other._value)*factor, final_bottom_half[0]._unit, -final_bottom_half[0]._exponent)
            
            return MultiUnit((self._value / other._value)*factor, top_half=final_top_half, bottom_half=final_bottom_half)
        
        elif isinstance(other, Union[int, float]):
            return MultiUnit(self._value / other, top_half=self._top_half, bottom_half=self._bottom_half)
        else:
            TypeError(f"Dividing class {self.__class__} and {other.__class__} is unsupported")
        
    def __mul__(self,other):

        if self.__class__ == other.__class__ or other.__class__.__bases__[0] == MultiUnit or other.__class__ == MultiUnit:
            
            new_top_half = deepcopy(self._top_half) + deepcopy(other._top_half)
            new_bottom_half = deepcopy(self._bottom_half) + deepcopy(other._bottom_half)
            
            new_top_half, new_bottom_half, factor = self.deconstruct_unit_prefixes(new_top_half, new_bottom_half)
            
            new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half)
            
            new_top_half = self.combine_units(new_top_half)
            new_bottom_half = self.combine_units(new_bottom_half)
            

        
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            
            final_top_half, final_bottom_half = self.simplify_units(final_top_half, final_bottom_half)
            
            return MultiUnit((self._value * other._value)*factor, top_half=final_top_half, bottom_half=final_bottom_half)
        elif other.__class__.__bases__[0] == Unit or other.__class__ == Unit:
            new_top_half = deepcopy(self._top_half) + [BaseUnit(other._unit, other._exponent)]
            new_bottom_half = deepcopy(self._bottom_half)
            
            new_top_half, new_bottom_half, factor = self.deconstruct_unit_prefixes(new_top_half, new_bottom_half)
            
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
            
            
            new_top_half = deepcopy(self._top_half)
            new_bottom_half = deepcopy(self._bottom_half)
            # append unit to the bottom half 
            new_bottom_half.append(BaseUnit(other._unit, other._exponent))
            # swap halfs 
            new_top_half, new_bottom_half = new_bottom_half, new_top_half
            
            new_top_half, new_bottom_half, factor = self.deconstruct_unit_prefixes(new_top_half, new_bottom_half)
            
            # deconstruct units
            new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half)
            
            new_top_half = self.combine_units(new_top_half)
                        
            final_top_half, final_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            
            final_top_half, final_bottom_half = self.simplify_units(final_top_half, final_bottom_half)
            
            # if all units cancel
            if len(final_top_half) == 0 and len(final_bottom_half) == 0:
                return other._value / self._value
            
            #if just left with one unit in top
            if len(final_top_half) == 1 and len(final_bottom_half) == 0:
                return Unit(other._value / self._value, final_top_half[0]._unit, final_top_half[0]._exponent)
            # one unit in the bottom
            if len(final_top_half) == 0 and len(final_bottom_half) == 1:
                return Unit(other._value / self._value, final_bottom_half[0]._unit, -final_bottom_half[0]._exponent)
                            
            return MultiUnit(other._value / self._value, top_half=final_top_half, bottom_half=final_bottom_half)
            
        
        else:
            raise TypeError(f"Dividing class {other.__class__} and {self.__class__} is unsupported")
    def __rmul__(self, other):
        if isinstance(other, Union[int, float]):
            return MultiUnit(other * self._value,top_half=self._top_half, bottom_half=self._bottom_half)
        elif other.__class__ == Unit or other.__class__.__bases__[0] == Unit:
            new_top_half = deepcopy(self._top_half) + [BaseUnit(other._unit, other._exponent)]
            new_bottom_half = deepcopy(self._bottom_half)
            
            new_top_half, new_bottom_half, factor = self.deconstruct_unit_prefixes(new_top_half, new_bottom_half)
            
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
        else:
            raise TypeError(f"Multiplying class {other.__class__} and {self.__class__} is unsupported")
    def __pow__(self, other):
        if isinstance(other, Union[int, float]):
            new_top_half = deepcopy(self._top_half)
            new_bottom_half = deepcopy(self._bottom_half)
            for u1 in new_top_half:
                u1._exponent *= other
            for u2 in new_bottom_half:
                u2._exponent *= other
                
            new_top_half, new_bottom_half = self.deconstruct_units(new_top_half, new_bottom_half)
            new_top_half = self.combine_units(new_top_half)
            new_bottom_half = self.combine_units(new_bottom_half)
            new_top_half, new_bottom_half = self.cancel_units(new_top_half, new_bottom_half)
            new_top_half, new_bottom_half = self.simplify_units(new_top_half, new_bottom_half)
            
            
            return MultiUnit(self._value**other,top_half=new_top_half, bottom_half=new_bottom_half)
        raise TypeError(f"Exponentiating class {other.__class__} and {self.__class__} is unsupported")
    
    def __neg__(self):
        return self.__class__(-self._value,top_half=self._top_half, bottom_half=self._bottom_half)


class Temperature(Unit):
    standard: str = "K"
    to_standard_conversions = {
        "F": lambda x: (5/9)*(x + 459.67),
        "C": lambda x: x + 273.15,
        "R": lambda x: x / (1.8)
    }
    from_standard_conversions = {
        "F": lambda x: 1.8*(x-273.15)+32,
        "C": lambda x: x - 273.15,
        "R": lambda x: x * 1.8,
    }
    def __init__(self, value:float, unit: TemperateUnits="K", exponent: int =1):
        # if unit not in TemperateUnits:
        #     raise TypeError(f"The unit of {unit} is not valid for temperature")
        super().__init__(value, unit, exponent)
        
class Pressure(Unit):
    standard: str = "Pa"
    # from target unit to standard unit 
    to_standard_conversions = {
        "uPa": lambda x: (x/1E6),
        "mPa": lambda x: (x/1000),
        "dPa": lambda x: (x/10),
        "kPa": lambda x: (x*1000),
        "MPa": lambda x: (x*10E6),
        "bar": lambda x: x*100000,
        "atm": lambda x: x*101325,
        "mmHg": lambda x: x*133.322,
        "psi": lambda x: x*6894.76,
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "uPa": lambda x: x*1E6,
        "mPa": lambda x: (x*1000),
        "dPa": lambda x: (x*10),
        "kPa": lambda x: (x/1000),
        "MPa": lambda x: (x/10E6),
        "bar": lambda x: x/100000,
        "atm": lambda x: x/101325,
        "mmHg": lambda x: x/133.322,
        "psi": lambda x: x/6894.76,
    }
    def __init__(self, value:float, unit: PressureUnits="atm",
                 exponent: int = 1):
        if unit not in PressureUnits:
            raise TypeError(f"The unit of {unit} is not valid for pressure")
        super().__init__(value, unit, exponent)
    
class Length(Unit):
    standard: str = "m"
    # from target unit to standard unit 
    to_standard_conversions = {
        "in": lambda x: (x/12)*0.3048,
        "ft": lambda x: x*0.3048,
        "yd": lambda x: x*0.9144,
        "mile": lambda x: x*1609.34,
        "um": lambda x: x/1E6,
        "mm": lambda x: x/1000,
        "cm": lambda x: x/100,
        "dm": lambda x: x/10,
        "km": lambda x: x*1000
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "in": lambda x: (x*12) * 3.28084,
        "ft": lambda x: x*3.28084,
        "yd": lambda x: x/0.9144,
        "mile": lambda x: x*1609.34,
        "um": lambda x: x*1E6,
        "mm": lambda x: x*1000,
        "cm": lambda x: x*100,
        "dm": lambda x: x*10,
        "km": lambda x: x/1000
        
    }
    def __init__(self,value:float, unit: str,
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
        "uJ": lambda x: x/1E6,
        "mJ": lambda x: x/1000,
        "cJ": lambda x: x/100,
        "dJ": lambda x: x/10,
        "kJ": lambda x: x*1000,
        "MJ": lambda x: x*1E6,
        "BTU": lambda x: x*1055.056
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "uJ": lambda x: x*1E6,
        "mJ": lambda x: x*1000,
        "cJ": lambda x: x*100,
        "dJ": lambda x: x*10,
        "kJ": lambda x: x/1000,
        "MJ": lambda x: x/1E6,
        "BTU": lambda x: x/1055.056
    }
    def __init__(self,value:float, unit: EnergyUnits,
                exponent: int = 1):
        super().__init__(value, unit, exponent)

class Mass(Unit):
    standard: str = "kg"
    # from target unit to standard unit 
    to_standard_conversions = {
        "ug": lambda x: x/1E9,
        "mg": lambda x: x/1E6,
        "dg": lambda x: x/10000,
        "g": lambda x: x/1000,
        "Mg": lambda x: x*1000,
        "lb": lambda x: x*0.453592
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        'ug': lambda x: x*1E9,
        "mg": lambda x: x*1E6,
        "dg": lambda x: x*10000,
        "g": lambda x: x*1000,
        "Mg": lambda x: x/1000,
        "lb": lambda x: x*2.20462
    }
    def __init__(self,value:float, unit: MassUnits,
                exponent: int = 1):
        super().__init__(value, unit, exponent)
          
        
class Current(Unit):
    standard: str = "A"
    def __init__(self,value:float, unit: Literal["A"],
                exponent: int = 1):
        if unit not in CurrentUnits:
            raise TypeError(f"The unit of {unit} is not valid for current")
        super().__init__(value, unit, exponent)
        
class Amount(Unit):
    standard: str = "mol"
    def __init__(self,value:float, unit: Literal["mol"],
                exponent: int = 1):
        if unit not in AmountUnits:
            raise TypeError(f"The unit of {unit} is not valid for an amount")
        super().__init__(value, unit, exponent)

    
class Force(Unit):
    standard: str = "N"
    # from target unit to standard unit 
    to_standard_conversions = {
        "uN": lambda x: x/1E6,
        "mN": lambda x: x/1000,
        "dN": lambda x: x/10,
        "kN": lambda x: x*1000,
        "MN": lambda x: x*1E6,
        "lbf": lambda x: x*4.44822,
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "uN": lambda x: x*1E6,
        "mN": lambda x: x*1000,
        "dN": lambda x: x*10,
        "kN": lambda x: x/1000,
        "MN": lambda x: x/1E6,
        "lbf": lambda x: x/4.44822
    }
    def __init__(self,value:float, unit: ForceUnits,
                exponent: int = 1):
        if unit not in ForceUnits:
            raise TypeError(f"The unit of {unit} is not valid for force")
        super().__init__(value, unit, exponent)

        
class Volume(Unit):
    standard: str = "m^3"
    # from target unit to standard unit 
    # cube applied to unit value in convert function
    # ie actual L conversion is by a factor of 10 * 10 * 10
    to_standard_conversions = {
        "uL": lambda x: x/1E-3,
        "mL": lambda x: x/100,
        "cL": lambda x: x/46.41588,
        "dL": lambda x: x/21.544346,
        "kL": lambda x: x,
        "L": lambda x: x/10,
        "um^3": lambda x: x/(1E6),
        "mm^3": lambda x: x/(1000),
        "cm^3": lambda x: x/(100),
        "dm^3": lambda x: x/(10),
        "km^3": lambda x: x*(1000),
        "ft^3": lambda x: x*0.3048,
        "gal": lambda x: x*0.00454609,
    }
    # form standard unit to the target unit 
    from_standard_conversions = {
        "uL": lambda x: x*1E-3,
        "mL": lambda x: x*100,
        "cL": lambda x: x*46.41588,
        "dL": lambda x: x*21.544346,
        "kL": lambda x: x,
        "L": lambda x: x*10,
        "um^3": lambda x: x*1E6,
        "mm^3": lambda x: x*(1000),
        "cm^3": lambda x: x*(100),
        "dm^3": lambda x: x*(10),
        "km^3": lambda x: x/(1000),
        "ft^3": lambda x: x/0.3048,
        "gal": lambda x: x/0.00454609,
    }
    def __init__(self, value: float, unit: str, exponent: int = 1):
        if "^" in unit:
            unit, exponent = unit.split("^")
            super().__init__(value, unit, float(exponent))
        else:
            super().__init__(value, unit, exponent)
class Area(Unit):
    standard = "m^2"
        
    to_standard_conversions = {
            "acre": lambda x: x*(4046.873)**(1/2),
            "in^2": lambda x: X*0.0254,
            "ft^2": lambda x: x*0.3048,
            "mile^2": lambda x: x*1609.344,
        }
        
    from_standard_conversions = {
            "acre": lambda x: x/(4046.873)**(1/2),
            "in^2": lambda x: x/0.0254,
            "ft^2": lambda x: x/0.3048,
            "mile^2": lambda x: x/1609.344,
        }
    def __init__(self, value: float, unit: str, exponent: int=1):

        if "^" in unit:
            unit, exponent = unit.split("^")
            super().__init__(value, unit, float(exponent))
        else:
            super().__init__(value, unit, exponent)   
        
UNIT_CLASSES = {
    "Temperature": Temperature,
    "Length": Length,
    "Mass": Mass,
    "Time": Time,
    "Current": Current,
    "Amount": Amount,
    "Energy": Energy,
    "Pressure": Pressure,
    "Force": Force,
    "Volume": Volume,
    "Area": Area,
}

def check_units(u: Unit | MultiUnit, unit_check: str, name: str)-> bool:
    # if not a unit class assume units are correct
    if u.__class__ not in [Unit, MultiUnit] and u.__class__.__bases__[0] not in [Unit, MultiUnit]:
        return
    
    if u.__class__ == Unit or u.__class__.__bases__[0] == Unit:
        if u._unit == unit_check:
            return 
        else:
           raise IncorrectUnits(f"Please supply the correct units of {unit_check} instead of {u._unit} for {name}") 
    else:
        top_check, bottom_check = u.parse_units(unit_check)
        
        if u._top_half == top_check and u._bottom_half == bottom_check:
            return 
        else:
            raise IncorrectUnits(f"Please supply the correct units of {unit_check} instead of {u._unit} for {name}") 
        
    