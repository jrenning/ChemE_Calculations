from units import MultiUnit, BaseLength, Time, Pressure, ThermalConductivity


def htc_open_field_laminar_local(Re: float, Pr: float, L: BaseLength,
                             k: MultiUnit):
    Nu_local = 0.332*Re**(1/2)*Pr**(1/3)
    top = Nu_local * k
    h = (top) / L
    return h
    

if __name__ == "__main__":
    Re = 5000
    Pr = 10
    L = BaseLength(50, "m")
    k = ThermalConductivity(.5,"J","s", "m", "K")
    h = htc_open_field_laminar_local(Re,Pr,L,k)
    print(h)
    