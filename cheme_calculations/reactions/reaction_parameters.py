

from math import exp, log
from typing import List, Union
import numpy as np
from collections import namedtuple
from cheme_calculations.units.mass_transfer import Concentration

from cheme_calculations.utility import solvable_for

from cheme_calculations.units.reactions import ActivationEnergy, KineticConstant
from cheme_calculations.units.units import MultiUnit, Temperature, Time

IntegralResults = namedtuple(
    'IntegralResults', ["order", "r_squared"]
)

__all__ = ["integral_method", "arrhenius"]

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


def _get_arrhenius_units(order: float):
    if order == 0:
        return "mol/L*s"
    if order == 1:
        return "s^-1"
    else:
        c = Concentration(1, "mol/L")
        c = c**(1-order)
        c = c/Time(1, "s")
        return c.get_unit_string()
        


@solvable_for(["A", "Ea", "T", "k"], 1)
def arrhenius(order: float, A: float, Ea: ActivationEnergy, R: MultiUnit, T: Temperature, k:KineticConstant=None, **kwargs)-> Union[KineticConstant
                                                                                                                      ,ActivationEnergy,
                                                                                                                      Temperature,
                                                                                                                      float]:
    """Solve for a variable in the arrhenius equation, defaults to solving for k
    units for arrhenius constant and k are based off the order provided
    NOTE: assumes units for reaction is in mol/L, can convert after for alternative units
    
    .. math:: k = Ae^{\frac{-Ea}{RT}}

    :param A: The Arrhenius constant
    :type A: float
    :param Ea: The activation energy, typically kJ/mol
    :type Ea: ActivationEnergy
    :param R: The gas constant, units must match Ea
    :type R: MultiUnit
    :param T: The temperature of the system
    :type T: Temperature
    :param k: The kinetic constant, defaults to None
    :type k: KineticConstant, optional
    :return: The parameter not supplied to the function, k by default
    :rtype: _type_
    
    :Example:
    >>> from cheme_calculations.reactions import arrhenius
    >>> from cheme_calculations.utility import get_gas_constant
    >>> A = 1E19
    >>> Ea = ActivationEnergy(89000, "J/mol")
    >>> R = get_gas_constant(generic=True) # 8.314 J / mol*K
    >>> T = Temperature(350, "K")
    >>> k = arrhenius(1, A, Ea, R, T)
    >>> print(k)
    >>> 521191.74607982725 s-¹
    >>> Ea = arrhenius(1, A, None, R, T, k)
    >>> print(Ea)
    >>> 89000.0 J / mol
    """
    # set units of A
    A = MultiUnit(A, _get_arrhenius_units(order))
    
    solving_for = kwargs["solving_for"]
    if solving_for == "k":
        return A*exp(-Ea/(R*T))
    if solving_for == "Ea":
        return -log(k/A)*R*T
    if solving_for == "T":
        return 1/((log(k/A)*R)/-Ea)
    if solving_for == "A":
        return k/(exp(-Ea/R*T))
    
    

       
        
        
        
    