from units import MultiUnit, BaseLength, BaseUnit, Unit


def open_field_laminar_local(Re: float, Pr: float, L: BaseLength,
                             k: MultiUnit):
    Nu_local = 0.332*Re**(1/2)*Pr**(1/3)
    i1 = Nu_local * k
    h = (i1)/L
    return h
    

if __name__ == "__main__":
    Re = 500
    Pr = 4
    L = Unit(50, "m")
    k = MultiUnit(0.6, [BaseUnit("W")], [BaseUnit("m"), BaseUnit("K")])
    h = open_field_laminar_local(Re, Pr, L, k)
    print(h)