from math import log
from cheme_calculations.units import Temperature

__all__ = ["deltat_logmean"]


def deltat_logmean(T0A: Temperature, T1A: Temperature,
                   T0B: Temperature, T1B: Temperature, cocurrent: bool = False)-> float:
    """Calculates the temperature delta log mean. For use when evaluating heat transfer in 
    a heat exchanger.

    :param T0A: The temperature of the target fluid when it enters
    :type T0A: Temperature
    :param T1A: The temperature of the target fluid when it exits
    :type T1A: Temperature
    :param T0B: The temperature of the other fluid when it enters
    :type T0B: Temperature
    :param T1B: The temperature of the other fluid when it exits
    :type T1B: Temperature
    :param cocurrent: Whether or not the heat exchanger is cocurrent (False = countercurrent), defaults to False
    :type cocurrent: bool, optional
    :return: The temperature delta log mean
    :rtype: float
    """
    
    if cocurrent:
        side_a_dif = T0A = T0B
        side_b_dif = T1A - T1B
        
    else:
        side_a_dif = T0A - T1B
        side_b_dif = T1A - T0B
    log_mean = (side_a_dif-side_b_dif)/log(side_a_dif/side_b_dif)
    
    return log_mean
        
        
    