from cheme_calculations.units.units import BaseUnit, MultiUnit


unit_simplifications = {
    "kg/s^3*K": "W/m^2*K"
}

# only used when an equation uses alot of units and simplifying requires a non obvious step
def do_weird_simplifications(unit_string: MultiUnit):
    for unit in unit_simplifications.keys():
        top_half, bottom_half = MultiUnit.parse_units(unit)
        
        if top_half == unit_string._top_half and bottom_half == unit_string._bottom_half:
            top_half, bottom_half = MultiUnit.parse_units(unit_simplifications[unit])
            return MultiUnit(unit_string._value, top_half=top_half, bottom_half=bottom_half)
    
    return unit_string
        