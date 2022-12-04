from units import MultiUnit, BaseLength, Time, Pressure


def htc_open_field_laminar_local(Re: float, Pr: float, L: BaseLength,
                             k: MultiUnit):
    Nu_local = 0.332*Re**(1/2)*Pr**(1/3)
    h = (Nu_local * k) / L
    return h
    

if __name__ == "__main__":
    P = Pressure(3000, "Pa")
    P.convert_to("atm")
    print(P)