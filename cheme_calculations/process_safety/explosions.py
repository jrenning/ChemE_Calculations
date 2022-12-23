from typing import Literal
from cheme_calculations.units import Pressure, Length

__all__ = ["max_vessel_pressure"]

def max_vessel_pressure(material_strength: Pressure, 
                        wall_thickness: Length,
                        inside_radius: Length,
                        vessel_shape: Literal["sphere", "cylinder"]):
    
    if vessel_shape == "cylinder":
        p_max = (material_strength*wall_thickness)/(inside_radius+(0.6*wall_thickness))
    elif vessel_shape == "sphere":
        p_max = (2*wall_thickness*material_strength)/(inside_radius + 0.2*wall_thickness)
    else:
        raise TypeError(f"{vessel_shape} is not a valid vessel shape")
        
    return p_max    
    