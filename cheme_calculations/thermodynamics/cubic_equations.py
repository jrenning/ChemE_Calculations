
from typing import Literal
from cheme_calculations.units import Temperature, Pressure


    
__all__ = ["rendlich_kwong", "van_der_waals", "soave_rendlich_kwong", 
           "peng_robinson"]  


def rendlich_kwong(temperature: Temperature, pressure: Pressure,
                   Tcrit: Temperature, Pcrit: Pressure,
                   state: Literal["vapor", "liquid"], iterations: int)-> float:
        """Calculates the Z correction factor based on the Rendlich-Kwong equation of state

        :param temperature: The temperature of the material
        :type temperature: class: Temperature
        :param pressure: The pressure of the material
        :type pressure: class: Pressure
        :param Tcrit: The critical temperature of the given material
        :type Tcrit: class: Temperature
        :param Pcrit: The critical pressure of the given material
        :type Pcrit: class: Pressure
        :param state: state of the material
        :type state: Literal["vapor", "liquid"]
        :param iterations: Number of iterations used to find the solution
        :type iterations: int
        :return: The correction factor Z
        :rtype: float
        
        :Example:
        
        >>> T = Temperature(350, "K)
        >>> Tcrit = Temperature(350, "K")
        >>> P = Pressure(350, "kPa")
        >>> Pcrit = Pressure(350, "kPa")
        >>> z = rendlich_kwong(T, P, Tcrit, Pcrit,"vapor", 6)
        >>> 0.47750
        
        """
        
        p_reduced = pressure/Pcrit
        t_reduced = temperature/Tcrit

        omega = .08664
        psi = .42748        
        alpha = t_reduced**(-1/2)
        beta = omega*(p_reduced/t_reduced)
        q = (psi*alpha)/(omega*t_reduced)
        
        if state == 'vapor':
            z_in = 1
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            for i in range(iterations):
                z_in = z_iter 
                z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
                
                
        if state == 'liquid':
            z_in = beta 
            z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            for i in range(iterations):
                z_in = z_iter
                z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
        
        return z_iter
        
        

def van_der_waals(temperature: Temperature, pressure: Pressure,
                   Tcrit: Temperature, Pcrit: Pressure,
                   state: Literal["vapor", "liquid"], iterations: int)-> float:
    """
    Takes in the starting temperature and pressure
    along with the critical temperature and pressure
    to calculate the Z value for the Van Der Waals EOS based on
    the given state.
    
    :param temperature: The temperature of the material
    :type temperature: class: Temperature
    :param pressure: The pressure of the material
    :type pressure: class: Pressure
    :param Tcrit: The critical temperature of the given material
    :type Tcrit: class: Temperature
    :param Pcrit: The critical pressure of the given material
    :type Pcrit: class: Pressure
    :param state: state of the material
    :type state: Literal["vapor", "liquid"]
    :param iterations: Number of iterations used to find the solution
    :type iterations: int
    :return: The correction factor Z
    :rtype: float
    
    :Example:
    
    >>> T = Temperature(350, "K)
    >>> Tcrit = Temperature(350, "K")
    >>> P = Pressure(350, "kPa")
    >>> Pcrit = Pressure(350, "kPa")
    >>> z = van_der_waals(T, P, Tcrit, Pcrit,"vapor", 6)
    >>> 0.70816
    
    """
    
    p_reduced = pressure/Pcrit
    t_reduced = temperature/Tcrit
    
    omega = 1/8
    psi = 27/64      
    alpha = 1
    beta = omega*(p_reduced/t_reduced)
    q = (psi*alpha)/(omega*t_reduced)
    
    if state == 'vapor':
        z_in = 1
        z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
        for i in range(iterations):
            z_in = z_iter 
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            
    if state == 'liquid':
        z_in = beta 
        z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
        for i in range(iterations):
            z_in = z_iter
            z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            
    return z_iter


def soave_rendlich_kwong(temperature: Temperature, pressure: Pressure,
                   Tcrit: Temperature, Pcrit: Pressure,
                   state: Literal["vapor", "liquid"], omega_lower: float, iterations: int)-> float:
    """
    Takes in the starting temperature and pressure
    along with the critical temperature and pressure
    to calculate the Z value for the SR EOS based on
    the given state.
    
    :param temperature: The temperature of the material
    :type temperature: class: Temperature
    :param pressure: The pressure of the material
    :type pressure: class: Pressure
    :param Tcrit: The critical temperature of the given material
    :type Tcrit: class: Temperature
    :param Pcrit: The critical pressure of the given material
    :type Pcrit: class: Pressure
    :param state: state of the material
    :type state: Literal["vapor", "liquid"]
    :param omega_lower: The accentric factor for the material
    :type omega_lower: float
    :param iterations: Number of iterations used to find the solution
    :type iterations: int
    :return: The correction factor Z
    :rtype: float
    
    :Example:
    
    >>> T = Temperature(350, "K)
    >>> Tcrit = Temperature(350, "K")
    >>> P = Pressure(350, "kPa")
    >>> Pcrit = Pressure(350, "kPa")
    >>> z = soave_rendlich_kwong(T, P, Tcrit, Pcrit,"vapor",0.224,  6)
    >>> 0.4775
    """
    p_reduced = pressure/Pcrit
    t_reduced = temperature/Tcrit
    
    omega = .08664
    psi = .42748
    alpha = (1 + (.480 + 1.574*omega_lower-0.176*omega_lower**2)*(1-t_reduced**(1/2)))**2
    beta = omega*(p_reduced/t_reduced)
    q = (psi*alpha)/(omega*t_reduced)
    
    if state == 'vapor':
        z_in = 1
        z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
        for i in range(iterations):
            z_in = z_iter 
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            
    if state == 'liquid':
        z_in = beta 
        z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
        for i in range(iterations):
            z_in = z_iter
            z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            
    return z_iter
            
            
    
def peng_robinson(temperature: Temperature, pressure: Pressure,
                Tcrit: Temperature, Pcrit: Pressure,
                state: Literal["vapor", "liquid"], omega_lower: float, iterations: int):
    """Calculates a Z correction factor using the peng robinson equation of state

    :param temperature: The temperature of the given material
    :type temperature: class: Temperature
    :param pressure: The pressure of the given material
    :type pressure: class: Pressure
    :param Tcrit: The critical temperature of the given material
    :type Tcrit: class: Temperature
    :param Pcrit: The critical pressure of the given material
    :type Pcrit: class: Pressure
    :param state: The state of the material
    :type state: Literal["vapor", "Liquid"]
    :param omega_lower: The accentric factor of the given material
    :type omega_lower: float
    :param iterations: The number of iterations used for the calculation
    :type iterations: int
    :return: The Z correction factor
    :rtype: float
    
     :Example:
    
    >>> T = Temperature(350, "K)
    >>> Tcrit = Temperature(350, "K")
    >>> P = Pressure(350, "kPa")
    >>> Pcrit = Pressure(350, "kPa")
    >>> z = peng_robinson(T, P, Tcrit, Pcrit,"vapor",0.224, 6)
    >>> 0.2351
    """
    p_reduced = pressure/Pcrit
    t_reduced = temperature/Tcrit
    
    sigma = 1 + 2**(1/2)
    epsilon = 1 - 2**(1/2)
    omega = .07780
    psi = .45724
    alpha = (1 + (.37464 + 1.54226*omega_lower-0.26992*omega_lower**2)*(1-t_reduced**(1/2)))**2
    beta = omega*(p_reduced/t_reduced)
    q = (psi*alpha)/(omega*t_reduced)
    
    if state == 'vapor':
        z_in = 1
        z_iter = beta + (z_in+epsilon*beta)*(z_in + sigma*beta)*((1+beta-z_in)/(q*beta))
        for i in range(iterations):
            z_in = z_iter 
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            
    if state == 'liquid':
        z_in = beta 
        z_iter = beta + (z_in+epsilon*beta)*(z_in + sigma*beta)*((1+beta-z_in)/(q*beta))
        for i in range(iterations):
            z_in = z_iter
            z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            
    return z_iter


    

    
    

