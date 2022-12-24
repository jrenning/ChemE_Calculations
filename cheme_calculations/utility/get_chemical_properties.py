from cheme_calculations.units.heat_transfer import ThermalConductivity
from cheme_calculations.units.property_units import Cp, Density, DynamicViscosity, Enthalpy, Entropy, InternalEnergy, SpecificVolume
from .water_data import WATER_PROPERTIES


class Water:
    def __init__(self, cp: float, Cv: float, density: float, 
                 enthalpy: float, entropy: float, internal_energy: float,
                 phase: str, thermal_conductivity: float, viscosity: float, 
                 specific_volume: float):
        self._Cp = Cp(cp, "J/g*K")
        self._Cv = Cv
        self._density = Density(density, "kg/m^3")
        self._enthalpy = Enthalpy(enthalpy, "kJ/kg")
        self._entropy = Entropy(entropy, "J/g*K")
        self._internal_energy = InternalEnergy(internal_energy, "kJ/kg")
        self._phase = phase
        self._thermal_conductivity = ThermalConductivity(thermal_conductivity, "W/m*K")
        self.viscosity = DynamicViscosity(viscosity, "mPa*s")
        self._specific_volume = SpecificVolume(specific_volume, "m^3/kg")


def get_water_properties(temperature: float)-> Water:
    """

    :param temperature: Temperature in Kelvin
    :type temperature: float
    """
    
    if temperature in WATER_PROPERTIES.keys():
        Cp = WATER_PROPERTIES[temperature]['Cp (J/g*K)']
        Cv = WATER_PROPERTIES[temperature]['Cv (J/g*K)']
        density = WATER_PROPERTIES[temperature]['Density (kg/m3)']
        enthalpy = WATER_PROPERTIES[temperature]['Enthalpy (kJ/kg)']
        Cp = WATER_PROPERTIES[temperature]['Cp (J/g*K)']
        Cp = WATER_PROPERTIES[temperature]['Cp (J/g*K)']
        Cp = WATER_PROPERTIES[temperature]['Cp (J/g*K)']
        Cp = WATER_PROPERTIES[temperature]['Cp (J/g*K)']
        
        return Water(Cp, Cv, density, enthalpy, Cp, Cp, Cp, Cp, Cp, Cp)
        
    
    
    