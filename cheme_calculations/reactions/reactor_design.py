
from cheme_calculations.units.reactions import MolarFlowRate, ReactionRate
from cheme_calculations.units.units import Volume

__all__ = ["cstr_volume"]

def cstr_volume(Fa0: MolarFlowRate, Fa: MolarFlowRate, ra: ReactionRate)-> Volume:
    """Gets the volume for a CSTR reactor. Assumes steady state and perfect mixing 
    
    .. math:: V = \frac{F_{A0} - F_A}{-r_a}

    :param Fa0: Initial molar flow rate
    :type Fa0: MolarFlowRate
    :param Fa: Ending molar flow rate
    :type Fa: MolarFlowRate
    :param ra: The reaction rate
    :type ra: ReactionRate
    :return: The CSTR volume needed to go from Fa0 to Fa at reaction rate ra
    :rtype: Volume
    
    :Example:
    
    >>> 
    """
    return (Fa0 - Fa) / -ra