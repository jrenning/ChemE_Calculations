from property_units import Density
from units import MultiUnit, Temperature, Length
from heat_transfer_coefficients import ThermalConductivity

def pseudo_steady_time(density: MultiUnit, heat_of_vaporization: MultiUnit, k: ThermalConductivity,
                       T_surface: Temperature, T_melt: Temperature, initial_length: Length,
                       final_length: Length):
    term1 = (density*heat_of_vaporization)/(k*(T_surface-T_melt))
    term2 = (final_length**2-initial_length**2)/2
    time = term1*term2
    return time


if __name__ == "__main__":
    ans = pseudo_steady_time(MultiUnit(800, "kg/m^3"),MultiUnit(8000,"J/kg"),
                       ThermalConductivity(0.6,"J","s","m","K"),
                       Temperature(293.15, "K"), Temperature(273.15, "K"),
                       Length(2, "m"), Length(0.5, "m"))
    
    print(ans)
    