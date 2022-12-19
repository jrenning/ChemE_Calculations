from itertools import chain, combinations
from threading import local
from typing import Callable, List, Literal
from inspect import getfullargspec
from functools import wraps
from pprint import pprint

# to get around circular import 
import cheme_calculations.units as u

class UnsolvableEquation(Exception):
    pass

class SolutionNotSupported(Exception):
    pass


__all__ = ["powerset", "getR_constant", "to_sup", "remove_zero", "solvable_for"]

# found here https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1)))


def solvable_for(solvable: List[str]):
    def inner(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            arg_names = getfullargspec(func).args
            
            arg_dict = {k:v for k,v in zip(arg_names, args)}
            
            # check if default solve was given a value
            default_given = 0
            if len(args) == len(arg_names):
                default_given = 1
            
            # check for improper None's
            for k, v in arg_dict.items():
                if k not in solvable and v == None:
                    raise SolutionNotSupported(f"Solving for {k} is not supported")
            
            # check for proper amount of None's 
            if (args.count(None) + 1 - default_given) > 1:
                raise UnsolvableEquation("Please supply more known parameters")
            
            # get thing were solving for 
            # initial set to default
            solving_for = arg_names[-1]
            for k, v in arg_dict.items():
                if v == None:
                    solving_for = k
                    
            
            a = func(*args, **kwargs, solving_for=solving_for)
            return a
        
        return wrapper
    
    return inner
    



def remove_zero(x: float):
    new_x = str(x)
    if ".0" in new_x:
        return int(x)
    else:
        return x


def get_prefix(unit: str):
    if len(unit) == 1:
        return ""
    else:
        return unit[0]
        

# found here https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript
def to_sup(s):
    sups = {u'0': u'\u2070',
            u'1': u'\xb9',
            u'2': u'\xb2',
            u'3': u'\xb3',
            u'4': u'\u2074',
            u'5': u'\u2075',
            u'6': u'\u2076',
            u'7': u'\u2077',
            u'8': u'\u2078',
            u'9': u'\u2079'}

    return ''.join(sups.get(char, char) for char in s) 




def getR_constant(temperature_units: Literal["K", "C", "F", "R"],
                  volume_units: Literal["cm^3", "m^3", "L"],
                  pressure_units: Literal["Pa", "kPa", "bar", "atm", "mmHg", "torr"],
                  generic=False):
    if generic:
        return u.MultiUnit(8.314, "J/mol*K")
    if volume_units == "m^3" and pressure_units == "Pa" and temperature_units == "K":
        return u.MultiUnit(8.314, "m^3*Pa/mol*K")
    if volume_units == "L" and pressure_units == "atm" and temperature_units == "K":
        return u.MultiUnit(0.08205, "L*atm/mol*K")
    if volume_units == "m^3" and pressure_units == "atm" and temperature_units == "K":
        return u.MultiUnit(8.205746E-5, "m^3*atm/mol*K")
    
    raise ValueError("The units supplied to R are not defined in a known constant")