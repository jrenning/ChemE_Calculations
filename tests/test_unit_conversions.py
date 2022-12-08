from units import Velocity, MultiUnit

def test_multi_unit_conversion():
    v = Velocity(1, "m/s")
    v2 = v.convert_to("cm/s")
    assert(v2 == Velocity(3.28084,"ft/s"))