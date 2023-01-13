from typing import Literal
from cheme_calculations.units import Pressure, Length

__all__ = ["max_vessel_pressure"]

def max_vessel_pressure(material_strength: Pressure, 
                        wall_thickness: Length,
                        inside_radius: Length,
                        vessel_shape: Literal["sphere", "cylinder"])-> Pressure:
    """Calculates the max pressure a vessel can withstand

    :param material_strength: Strength of the material, can be value to resist deformation or just contain explosion
    :type material_strength: Pressure
    :param wall_thickness: Thickness of the container's walls
    :type wall_thickness: Length
    :param inside_radius: Inner radius of the container
    :type inside_radius: Length
    :param vessel_shape: Shape of the containment vessel
    :type vessel_shape: Literal[&quot;sphere&quot;, &quot;cylinder&quot;]
    :raises TypeError: Raises an error if the shape given is invalid
    :return: The max pressure
    :rtype: Pressure
    """
    
    if vessel_shape == "cylinder":
        p_max = (material_strength*wall_thickness)/(inside_radius+(0.6*wall_thickness))
    elif vessel_shape == "sphere":
        p_max = (2*wall_thickness*material_strength)/(inside_radius + 0.2*wall_thickness)
    else:
        raise TypeError(f"{vessel_shape} is not a valid vessel shape")
        
    return p_max    


