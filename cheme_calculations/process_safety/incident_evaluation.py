
__all__ = ["FAR"]

def FAR(number_of_fatalities: float, total_hours: float)-> float:
    """Calculates the FAR value for a specific workplace in a specific time period,
    Used as a measure of workplace safety.
    
    .. math:: FAR = \dfrac{# fatalities * 10^8}{Total hours worked by employees in period}

    :param number_of_fatalities: Number of workplace fatalities in the time period
    :type number_of_fatalities: float
    :param total_hours: Number of hours worked by all employees in the time period
    :type total_hours: float
    :return: The FAR value
    :rtype: float
    
    :Example:
    
    >>> from cheme_caluclations.process_safety import FAR
    >>> ans = FAR(2, 1E9)
    >>> print(ans)
    >>> 2.0
    """
    
    return (number_of_fatalities*10E8)/total_hours


def OSHA_incidence_rate(relevent_number: float, total_hours: float)-> float:
    """Calculates the OSHA incidence rate. Can be based on number of lost workdays
    or number of injuries and illnesses.
    
    .. math:: incidence_rate = \dfrac{relevant_number * 200000}{Total hours worked by employees in period}

    :param relevent_number: Number of injuries/illnesses or number of lost workdays
    :type relevent_number: float
    :param total_hours: Total hours worked by all employees in the time period
    :type total_hours: float
    :return: The OSHA incidence rate 
    :rtype: float
    """
    return (relevent_number*200000)/total_hours