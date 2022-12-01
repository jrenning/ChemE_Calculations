from units import Temperature, Pressure, getR_constant, Unit


class UnitSystem:
    pass
# testing something
class Volume:
    def __init__(self,volume):
        self.volume = volume
    def __repr__(self) -> str:
        return f"{self.volume} cm^3"

    
        


def rendlich_kwong(temperature: Temperature, pressure: Pressure,
                   Tcrit: Temperature, Pcrit: Pressure,
                   state: str, iterations: int):
        """
        Takes in the starting temperature and pressure
        along with the critical temperature and pressure
        to calculate the Z value for the RK EOS based on
        the given state.\n
        T = initial temperature of component\n
        P = initial pressure of component\n
        Tcrit = critical temperature of component\n
        Pcrit = critical pressure of component\n
        state = liquid or vapor 
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
                   state: str, iterations: int):
    """
    Takes in the starting temperature and pressure
    along with the critical temperature and pressure
    to calculate the Z value for the Van Der Waals EOS based on
    the given state.\n
    T = initial temperature of component\n
    P = initial pressure of component\n
    Tcrit = critical temperature of component\n
    Pcrit = critical pressure of component\n
    state = liquid or vapor 
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
                   state: str, omega_lower: float, iterations: int):
    """
    Takes in the starting temperature and pressure
    along with the critical temperature and pressure
    to calculate the Z value for the SR EOS based on
    the given state.\n
    T = initial temperature of component\n
    P = initial pressure of component\n
    Tcrit = critical temperature of component\n
    Pcrit = critical pressure of component\n
    state = liquid or vapor 
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
                state: str, omega_lower: float, iterations: int):
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


if __name__ == '__main__':
    T = Temperature(350, "K",3)
    P = Pressure(350, "kPa")
    Pcrit = Pressure(350, "kPa")
    Tcrit = Temperature(350,'K')
    l = T/P
    print(l * T)
    

    
    

