from math import ceil, floor
from cheme_calculations.units.heat_transfer import ThermalConductivity
from cheme_calculations.units.property_units import Cp, Cv, Density, DynamicViscosity, Enthalpy, Entropy, InternalEnergy, SpecificVolume
from .water_data import WATER_PROPERTIES

class OutOfRangeProperty(Exception):
    pass

__all__ = ["Water", "get_water_properties"]


class Water:
    def __init__(self, cp: float, cv: float, density: float, 
                 enthalpy: float, entropy: float, internal_energy: float,
                 phase: str, thermal_conductivity: float, viscosity: float, 
                 specific_volume: float):
        self._Cp = Cp(cp, "J/g*K")
        self._Cv = Cv(cv, "J/g*K")
        self._density = Density(density, "kg/m^3")
        self._enthalpy = Enthalpy(enthalpy, "kJ/kg")
        self._entropy = Entropy(entropy, "J/g*K")
        self._internal_energy = InternalEnergy(internal_energy, "kJ/kg")
        self._phase = phase
        self._thermal_conductivity = ThermalConductivity(thermal_conductivity, "W/m*K")
        self._viscosity = DynamicViscosity(viscosity, "uPa*s")
        self._specific_volume = SpecificVolume(specific_volume, "m^3/kg")


def _interpolate_property_data(data: dict, eval_point: float, property_keys: list,
                               lower_bound: float, upper_bound: float)-> float:
    
    new_property_values = []
    for property_key in property_keys:
        y1 = data[lower_bound][property_key]
        y2 = data[upper_bound][property_key]
        if property_key != "Phase":
            new_value = y1 + (eval_point - lower_bound) * ((y2-y1)/(upper_bound-lower_bound))
            new_property_values.append(new_value)
        else:
            # assume interpolated phase is the higher value
            new_property_values.append(y2)
    
    return new_property_values
    


def get_water_properties(temperature: float)-> Water:
    """Returns a Water object that contains the isobaric properties
    of water at a given temperature in Kelvin. Assumes a pressure
    of 101325 Pa or 1 atm.
    
    Properties include:
    
    - Cp
    - Cv
    - density
    - enthalpy
    - entropy
    - internal energy
    - phase
    - thermal conductivity
    - viscosity 
    - specific volume

    :param temperature: Temperature in Kelvin
    :type temperature: float
    
    :Example:
    
    >>> from cheme_calculations.utility import get_water_properties
    >>> w = get_water_properties(300)
    >>> print(w._density)
    >>> 996.4449999999999 kg / m³
    >>> print(w._thermal_conductivity)
    >>> 0.6092 W / m * K
    """
    # no interpolation needed
    if temperature in WATER_PROPERTIES.keys():
        Cp = WATER_PROPERTIES[temperature]['Cp (J/g*K)']
        Cv = WATER_PROPERTIES[temperature]['Cv (J/g*K)']
        density = WATER_PROPERTIES[temperature]['Density (kg/m3)']
        enthalpy = WATER_PROPERTIES[temperature]['Enthalpy (kJ/kg)']
        entropy = WATER_PROPERTIES[temperature]['Entropy (J/g*K)']
        internal_energy = WATER_PROPERTIES[temperature]['Internal Energy (kJ/kg)']
        phase = WATER_PROPERTIES[temperature]['Phase']
        thermal_conductivity = WATER_PROPERTIES[temperature]['Cp (J/g*K)']
        viscosity = WATER_PROPERTIES[temperature]['Viscosity (uPa*s)']
        specific_volume = WATER_PROPERTIES[temperature]['Volume (kg/m^3)']
        
        return Water(Cp, Cv, density, enthalpy, entropy, internal_energy, phase, thermal_conductivity
                     , viscosity, specific_volume)
    # interpolate the values
    elif temperature > 275 and temperature < 1345:
        starting_index = 275
        
        lower_bound = (floor((temperature-starting_index)/10)*10)+starting_index
        upper_bound = (ceil((temperature-starting_index)/10)*10)+starting_index
        
        
        property_keys = ['Cp (J/g*K)', 'Cv (J/g*K)', 'Density (kg/m3)','Enthalpy (kJ/kg)', 'Entropy (J/g*K)',
                         'Internal Energy (kJ/kg)', 'Phase', "Therm. Cond. (W/m*K)", 'Viscosity (uPa*s)',
                         'Volume (m3/kg)']
        new_data = _interpolate_property_data(WATER_PROPERTIES, temperature, property_keys, lower_bound, upper_bound)
        
        return Water(*new_data)
        
    else:
        raise OutOfRangeProperty("Please enter a temperature between 275 and 1345 K")
        
    
    
    