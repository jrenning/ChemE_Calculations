from cheme_calculations.units import Temperature, MultiUnit
from cheme_calculations.units.property_units import DynamicViscosity

__all__ = ["wilke_chang"]
        

def wilke_chang(temperature: Temperature, theta_b: float, moleclar_weight_b: MultiUnit,
                viscosity_b: MultiUnit, molecular_volume_a: MultiUnit):
    
    answer = (7.4E-8*(theta_b*moleclar_weight_b)**(1/2)*temperature)/(viscosity_b*molecular_volume_a**0.6)
    
    return MultiUnit(answer, "cm^2/s")


    