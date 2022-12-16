from cheme_calculations.units import Temperature, Length
from cheme_calculations.units.property_units import Density, DynamicViscosity, Gravity, Hvap
from cheme_calculations.units.simplifications import do_weird_simplifications, unit_simplifications
from cheme_calculations.units.units import MultiUnit
from .unit_types import HeatTransferCoefficient, ThermalConductivity



def condensation_transfer_coefficient(k: ThermalConductivity, 
                                      rho: Density, g: Gravity,
                                      hvap: Hvap, num_pipes: int, 
                                      T2: Temperature, T1: Temperature, 
                                      diameter: Length, mu: DynamicViscosity):
    

    h = 0.729*((k**3 * rho**2 * g * hvap)/(num_pipes * (T2-T1) * diameter * mu))**(1/4)
    
    # units here get messed up so need to manually make them nice (units do check out though)
    h = do_weird_simplifications(h)
    
    
    return h

def flux_max_boiling(hvap: Hvap, rho_v: Density, rho_l: Density, 
                     surface_tension: MultiUnit, g: Gravity):
    
    qa_max = 0.15*hvap*rho_v**(1/2)*(surface_tension*g*(rho_l-rho_v))**(1/4)
    
    return qa_max