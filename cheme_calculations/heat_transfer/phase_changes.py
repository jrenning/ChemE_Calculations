from cheme_calculations.units import Temperature
from cheme_calculations.units.property_units import Density, DynamicViscosity, Gravity, Hvap
from cheme_calculations.units.units import Length
from .unit_types import HeatTransferCoefficient, ThermalConductivity



def condensation_transfer_coefficient(k: ThermalConductivity, 
                                      rho: Density, g: Gravity,
                                      hvap: Hvap, num_pipes: int, 
                                      T2: Temperature, T1: Temperature, 
                                      diameter: Length, mu: DynamicViscosity):
    
    top = k**3*rho**2*g*hvap
    bot = (T2-T1)*diameter*mu*num_pipes
    l = top/bot
    print(k**3*rho**2*g)
    print(bot)

    
    h = 0.729*((k**3 * rho**2 * g * hvap)/(num_pipes * (T2-T1) * diameter * mu))**(1/4)
    
    
    return h