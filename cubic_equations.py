def cubic_eos_RK(T,P,Tcrit,Pcrit,state):
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
    p_reduced = P/Pcrit
    t_reduced = T/Tcrit

    omega = .08664
    psi = .42748        
    alpha = t_reduced**(-1/2)
    beta = omega*(p_reduced/t_reduced)
    q = (psi*alpha)/(omega*t_reduced)
    
    if state == 'vapor':
        z_in = 1
        z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
        for i in range(6):
            print(f'Z{i} = {z_iter}')
            z_in = z_iter 
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            
            
    if state == 'liquid':
        z_in = beta 
        z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
        for i in range(6):
            print(f'Z{i} = {z_iter}')
            z_in = z_iter
            z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
    
    return z_iter



def cubic_eos_vdW(T,P,Tcrit,Pcrit,state):
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
    
    p_reduced = P/Pcrit
    t_reduced = T/Tcrit
    
    omega = 1/8
    psi = 27/64      
    alpha = 1
    beta = omega*(p_reduced/t_reduced)
    q = (psi*alpha)/(omega*t_reduced)
    
    if state == 'vapor':
        z_in = 1
        z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
        for i in range(6):
            print(f'Z{i} = {z_iter}')
            z_in = z_iter 
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            
    if state == 'liquid':
        z_in = beta 
        z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
        for i in range(6):
            print(f'Z{i} = {z_iter}')
            z_in = z_iter
            z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            
    return z_iter
            
            
            
    
def cubic_eos_SR(T,P,Tcrit,Pcrit,state,omega_lower):
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
    p_reduced = P/Pcrit
    t_reduced = T/Tcrit
    
    omega = .08664
    psi = .42748
    alpha = (1 + (.480 + 1.574*omega_lower-0.176*omega_lower**2)*(1-t_reduced**(1/2)))**2
    beta = omega*(p_reduced/t_reduced)
    q = (psi*alpha)/(omega*t_reduced)
    
    if state == 'vapor':
        z_in = 1
        z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
        for i in range(6):
            print(f'Z{i} = {z_iter}')
            z_in = z_iter 
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            
    if state == 'liquid':
        z_in = beta 
        z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
        for i in range(6):
            print(f'Z{i} = {z_iter}')
            z_in = z_iter
            z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            
    return z_iter
    

def cubic_eos_PR(T,P,Tcrit,Pcrit,state,omega_lower):
    
    p_reduced = P/Pcrit
    t_reduced = T/Tcrit
    
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
        for i in range(6):
            print(f'Z{i} = {z_iter}')
            z_in = z_iter 
            z_iter = 1 + beta - q*beta*((z_in-beta)/(z_in*(z_in+beta)))
            
    if state == 'liquid':
        z_in = beta 
        z_iter = beta + (z_in+epsilon*beta)*(z_in + sigma*beta)*((1+beta-z_in)/(q*beta))
        for i in range(6):
            print(f'Z{i} = {z_iter}')
            z_in = z_iter
            z_iter = z_iter = beta + z_in*(z_in + beta)*((1+beta-z_in)/(q*beta))
            
    return z_iter
    
    
def calculate_volume(z_final,T,P,R):
    """
    calculates the volume of a compound using the non-ideal gas law
    """
    volume = (z_final*R*T)/P
    
    return volume 

def input_eos(eos: str):
    """
    Returns T, Tcrit, P, Pcrit, z_final, and volume for use in other functions
    """
    T = float(input('Input the starting temperature: '))
    Tcrit = float(input('Input the critical temperature: '))
    P = float(input('Input the starting pressure: '))
    Pcrit = float(input('Input the critical pressure: '))
    R = float(input('Input the appropriate R value: '))


    state = input('Input the state in question: ')
    
    if eos == 'RK':
        z_final = cubic_eos_RK(T=T,P=P,Tcrit=Tcrit,Pcrit=Pcrit,state=state)
    if eos == 'vdW':
        z_final = cubic_eos_vdW(T=T,P=P,Tcrit=Tcrit,Pcrit=Pcrit,state=state)
    if eos == 'SR':
        omega_lower = float(input('Input omega value: '))
        z_final = cubic_eos_SR(T=T,P=P,Tcrit=Tcrit,Pcrit=Pcrit,state=state,omega_lower=omega_lower)
    if eos == 'PR':
        omega_lower = float(input('Input omega value: '))
        z_final = cubic_eos_PR(T=T,P=P,Tcrit=Tcrit,Pcrit=Pcrit,state=state,omega_lower=omega_lower)
    
    volume = calculate_volume(z_final,T=T,P=P,R=R)
    print(f'The z-value found is {z_final:4f}')
    print(f'The volume is {volume}')
    
    return T, Tcrit, P, Pcrit, z_final, volume
    
        


if __name__ == '__main__':
    
    eos = input('Input the equation of state (vdW,RK,SR,PR): ')
    input_eos(eos)
    

