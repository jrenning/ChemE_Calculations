class UnitSystem:
    pass
# testing something
class Volume:
    def __init__(self,volume):
        self.volume = volume
    def __repr__(self) -> str:
        return f"{self.volume} cm^3"

class CubicEquationSolver: 
    def __init__(self, temperature: float, pressure: float,Tcrit: float, Pcrit: float, state: str, iterations: int):
        self._temperature = temperature
        self._pressure = pressure
        self._Tcrit = Tcrit
        self._Pcrit = Pcrit
        self._z_final = None
        
        if state not in ["vapor", "liquid"]:
            raise ValueError("state must be vapor or liquid")
        self._state = state
        if iterations > 100:
            raise ValueError("iterations must be below 100")
        self._iterations = iterations
        

    def solve_for_volume(self, z_final: float):
        """
        calculates the volume of a compound using the non-ideal gas law
        """
        R = 8.314
        volume = (z_final*R*self._temperature)/self._pressure
        
        return Volume(volume)
    
        


class RendlichKwongSolver(CubicEquationSolver):
    def __init__(self, temperature: float, pressure: float,Tcrit: float, Pcrit: float, state: str, 
                 iterations: int=6):
        super().__init__(temperature, pressure, Tcrit, Pcrit, state, iterations)
    def solve(self):
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
        p_reduced = self._pressure/self._Pcrit
        t_reduced = self._temperature/self._Tcrit

        omega = .08664
        psi = .42748        
        alpha = t_reduced**(-1/2)
        beta = omega*(p_reduced/t_reduced)
        q = (psi*alpha)/(omega*t_reduced)
        
        if self._state == 'vapor':
            z_in = 1
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            for i in range(self._iterations):
                z_in = z_iter 
                z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
                
                
        if self._state == 'liquid':
            z_in = beta 
            z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            for i in range(self._iterations):
                z_in = z_iter
                z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
        
        return z_iter
        
        

class VanDerWaalsSolver(CubicEquationSolver):
    def __init__(self, temperature: float, pressure: float,Tcrit: float, Pcrit: float, state: str,
                 iterations: int=6):
        super().__init__(temperature, pressure, Tcrit, Pcrit, state, iterations)
    def solve(self):
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
        
        p_reduced = self._pressure/self._Pcrit
        t_reduced = self._temperature/self._Tcrit
        
        omega = 1/8
        psi = 27/64      
        alpha = 1
        beta = omega*(p_reduced/t_reduced)
        q = (psi*alpha)/(omega*t_reduced)
        
        if self._state == 'vapor':
            z_in = 1
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            for i in range(self._iterations):
                z_in = z_iter 
                z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
                
        if self._state == 'liquid':
            z_in = beta 
            z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            for i in range(self._iterations):
                z_in = z_iter
                z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
                
        return z_iter


class SoaveRendlichKwongSolver(CubicEquationSolver):
    def __init__(self, temperature: float, pressure: float,Tcrit: float, Pcrit: float, state: str, 
                 omega_lower: float, iterations: int=6):
        super().__init__(temperature, pressure, Tcrit, Pcrit, state, iterations)
        self._omega_lower = omega_lower
    def solve(self):
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
        p_reduced = self._pressure/self._Pcrit
        t_reduced = self._temperature/self._Tcrit
        
        omega = .08664
        psi = .42748
        alpha = (1 + (.480 + 1.574*self._omega_lower-0.176*self._omega_lower**2)*(1-t_reduced**(1/2)))**2
        beta = omega*(p_reduced/t_reduced)
        q = (psi*alpha)/(omega*t_reduced)
        
        if self._state == 'vapor':
            z_in = 1
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            for i in range(self._iterations):
                z_in = z_iter 
                z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
                
        if self._state == 'liquid':
            z_in = beta 
            z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            for i in range(self._iterations):
                z_in = z_iter
                z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
                
        return z_iter
            
            
class PengRobinsonSolver(CubicEquationSolver):
    def __init__(self, temperature: float, pressure: float,Tcrit: float, Pcrit: float, state: str, 
                 omega_lower: float, iterations: int=6):
        super().__init__(temperature, pressure, Tcrit, Pcrit, state, iterations)
        self._omega_lower = omega_lower
    
    def solve(self):
        p_reduced = self._pressure/self._Pcrit
        t_reduced = self._temperature/self._Tcrit
        
        sigma = 1 + 2**(1/2)
        epsilon = 1 - 2**(1/2)
        omega = .07780
        psi = .45724
        alpha = (1 + (.37464 + 1.54226*self._omega_lower-0.26992*self._omega_lower**2)*(1-t_reduced**(1/2)))**2
        beta = omega*(p_reduced/t_reduced)
        q = (psi*alpha)/(omega*t_reduced)
        
        if self._state == 'vapor':
            z_in = 1
            z_iter = beta + (z_in+epsilon*beta)*(z_in + sigma*beta)*((1+beta-z_in)/(q*beta))
            for i in range(self._iterations):
                z_in = z_iter 
                z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
                
        if self._state == 'liquid':
            z_in = beta 
            z_iter = beta + (z_in+epsilon*beta)*(z_in + sigma*beta)*((1+beta-z_in)/(q*beta))
            for i in range(self._iterations):
                z_in = z_iter
                z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
                
        return z_iter


if __name__ == '__main__':
    
    solver = RendlichKwongSolver(350,350,350,350, "vapor")
    sol = solver.solve()
    vol = solver.solve_for_volume(sol)
    print(vol)
    

