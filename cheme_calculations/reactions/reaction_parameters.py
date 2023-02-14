

from math import log
from typing import List
import numpy as np
from collections import namedtuple

IntegralResults = namedtuple(
    'IntegralResults', ["order", "r_squared"]
)

__all__ = ["integral_method"]

def integral_method(time_data: List, reaction_data: List, order_range: tuple)-> IntegralResults:
    """Uses the integral method to determine the reaction order for a particular reactant, 
    evaluates the bets result using r squared correlation.

    :param time_data: The time data for the reaction 
    :type time_data: List
    :param reaction_data: The concentration data for the reactant
    :type reaction_data: List
    :param order_range: The range of orders to test for the best fit, (start, stop, step)
    :type order_range: tuple(int, int, float)
    :return: The results of the fit (order: float, r_squared: float)
    :rtype: IntegralResults
    
    :Example: 
    
    >>> from cheme_calculations.reactions import integral_method
    >>> time_data = [0, 10, 20, 30, 40]
    >>> reaction_data = [0.624, 0.446, 0.318, 0.224, 0.164]
    >>> ans = integral_method(time_data, reaction_data, (0, 4, .5))
    >>> print(ans)
    >>> IntegralResults(order=1.0, r_squared=0.9997228295541076)
    """
    
    def get_r_squared(list1: List, list2: List):
        corr_matrix = np.corrcoef(list1, list2)
        corr = corr_matrix[0, 1]
        return corr**2
    
    best_r_squared = 0
    order = 0
    for i in np.arange(*order_range):
        if i == 1:
            reaction_data = [log(x) for x in reaction_data]
        elif i<1 and i>0:
            # based on power rule derivative 
            reaction_data = [x**(-i+1)/(-i+1) for x in reaction_data]
        elif i >= 1:
            reaction_data = [1/x**(i-1) for x in reaction_data]
        r = get_r_squared(time_data, reaction_data)
        if r > best_r_squared:
            best_r_squared = r
            order = i
    
    return IntegralResults(order, best_r_squared)


            
        
        
        
    