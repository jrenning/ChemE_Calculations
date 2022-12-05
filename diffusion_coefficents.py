from units import Temperature, MultiUnit

def wilke_chnag(temperature: Temperature, theta_b: float, moleclar_weight_b: MultiUnit,
                viscosity_b: MultiUnit, molecular_volume_a: MultiUnit):
    
    answer = (7.4E-8*(theta_b*moleclar_weight_b)**(1/2)*temperature)/(viscosity_b*molecular_volume_a**0.6)
    
    return MultiUnit(answer, "cm^2/s")


if __name__ == "__main__":
    T = 293.15
    theta_b = 2.6
    molecular_weight = 18
    viscosity_b = 1
    molecular_vol = 29.9
    ans = wilke_chnag(T,theta_b,molecular_weight, viscosity_b,
                      molecular_vol)
    
    print(ans)