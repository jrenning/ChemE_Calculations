from math import ceil, floor
from typing import List
from cheme_calculations.units.heat_transfer import ThermalConductivity
from cheme_calculations.units.property_units import Cp, Cv, Density, DynamicViscosity, Enthalpy, Entropy, InternalEnergy, SpecificVolume
from cheme_calculations.units.units import Pressure, Temperature
from .water_data import WATER_PROPERTIES, WATER_PROPERTY_KEYS

class OutOfRangeProperty(Exception):
    pass

__all__ = ["Water", "get_water_properties"]


class Water:
    def __init__(self, pressure: float, temperature: float, cp: float, cv: float, density: float, 
                 enthalpy: float, entropy: float, internal_energy: float,
                 phase: str, thermal_conductivity: float, viscosity: float, 
                 specific_volume: float):
        
        self._temperature = Temperature(temperature, "K")
        self._pressure = Pressure(pressure, "MPa")
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
    
    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, temp: float):
        new_data = get_water_properties(temp, False)
        self.__init__(*new_data)
    
    
    
def _get_property_data(data: dict, eval_point: float, property_keys: list,
                               lower_bound: float, upper_bound: float)-> float:
    
    # first value returned is the index used 
    new_property_values = [eval_point]
    for property_key in property_keys:
        y1 = data[lower_bound][property_key]
        y2 = data[upper_bound][property_key]
        # if no interpolation needed
        if y1 == y2:
            new_property_values.append(y1)
        elif property_key != "Phase":
            new_value = y1 + (eval_point - lower_bound) * ((y2-y1)/(upper_bound-lower_bound))
            new_property_values.append(new_value)
        else:
            # assume interpolated phase is the higher value
            new_property_values.append(y2)
    
    return new_property_values
    


def get_water_properties(temperature: float, return_object: bool=True)-> List | Water:
    """Returns a Water object that contains the isobaric properties
    of water at a given temperature in Kelvin. Assumes a pressure
    of 101325 Pa or 1 atm.
    
    Properties include:
    
    - temperature (K)
    - pressure (MPa)
    - Cp (J/g*K)
    - Cv (J*g/K)
    - density (kg/m^3)
    - enthalpy (kJ/kg)
    - entropy (J/g*K)
    - internal energy (kJ/kg)
    - phase (liquid or vapor)
    - thermal conductivity (W/m*K)
    - viscosity (uPa*s)
    - specific volume (m^3/kg)

    :param temperature: Temperature in Kelvin
    :type temperature: float
    :param return_object: Whether or not the function should return a Water object (returns an array of the data if False), defaults to True
    :type return_object: bool
    
    :Example:
    
    >>> from cheme_calculations.utility import get_water_properties
    >>> w = get_water_properties(300)
    >>> print(w._density)
    >>> 996.4449999999999 kg / m³
    >>> print(w._thermal_conductivity)
    >>> 0.6092 W / m * K
    """
    
    if temperature >= 275 and temperature <= 1345:
        starting_index = 275
        
        # these will be the same if a key if an index value is chosen
        lower_bound = (floor((temperature-starting_index)/10)*10)+starting_index
        upper_bound = (ceil((temperature-starting_index)/10)*10)+starting_index
        
        new_data = _get_property_data(WATER_PROPERTIES, temperature, WATER_PROPERTY_KEYS, lower_bound, upper_bound)
        
        if return_object:
            return Water(*new_data)
        else:
            return new_data
        
    else:
        raise OutOfRangeProperty("Please enter a temperature between 275 and 1345 K")
        
    
    
    