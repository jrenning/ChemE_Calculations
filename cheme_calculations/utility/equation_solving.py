from typing import Callable, List
from inspect import getfullargspec
from functools import wraps

__all__ = ["solvable_for"]

class UnsolvableEquation(Exception):
    pass

class SolutionNotSupported(Exception):
    pass

class OverSpecifiedProblem(Exception):
    pass

def solvable_for(solvable: List[str]):
    """Decorator function that helps determine what an equation should be solved for 
    and if that is a valid thing to solve for 

    :param solvable: List of parameters in the function that can be solved for 
    :type solvable: List[str]
    """
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
            
            # check for over specification
            if (args.count(None) + default_given) == 1:
                raise OverSpecifiedProblem("There are too many parameters supplied to this function")
            
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