from units import Temperature, MultiUnit, LengthUnit, DynamicViscosity

class DiffusionCoefficient(MultiUnit):
    def __init__(value: float, length_unit: LengthUnit, time_unit):
        pass
        

def wilke_chnag(temperature: Temperature, theta_b: float, moleclar_weight_b: MultiUnit,
                viscosity_b: MultiUnit, molecular_volume_a: MultiUnit):
    
    answer = (7.4E-8*(theta_b*moleclar_weight_b)**(1/2)*temperature)/(viscosity_b*molecular_volume_a**0.6)
    
    return MultiUnit(answer, "cm^2/s")


if __name__ == "__main__":

    v = DynamicViscosity(50, "cP")
    v.convert_to("kg/s*m", True)
    print(v)
    