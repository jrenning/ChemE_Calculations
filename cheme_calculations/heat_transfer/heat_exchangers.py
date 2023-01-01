from math import log, pi
from cheme_calculations.units import Temperature
from cheme_calculations.units.heat_transfer import ThermalConductivity
from cheme_calculations.units.property_units import Area, Cp, DynamicViscosity
from cheme_calculations.units.units import Length, MultiUnit
from cheme_calculations.utility import solvable_for
from cheme_calculations.utility.dimensionless import prandtl
from cheme_calculations.utility.equation_solving import UnsolvableEquation

__all__ = ["deltat_logmean", "solve_heat_exchanger_system",
           "equivalent_diameter"]

def equivalent_diameter(cross_sectional_area: Area, wetted_perimeter: Length)-> Length:
    """Calculates an effective diameter for an enclosed flow. Used in 
    calculations such as the Reynolds number as the characteristic length.
    Equation is also equivalent to 4 times the hydraulic radius.
    
    .. math:: equivalent diameter = 4*r_H = 4 * \dfrac{cross-sectional area}{wetted perimeter}

    :param cross_sectional_area: The cross sectional area of the enclosed flow
    :type cross_sectional_area: Area
    :param wetted_perimeter: The perimeter of the enclosed area that is touching fluid (ie only three sides for channel flow)
    :type wetted_perimeter: Length
    :return: The equivalent diameter
    :rtype: Length
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import equivalent_diameter
    >>> # 1m by 1m square pipe
    >>> csa = Area(1, "m^2")
    >>> perimeter = Length(4, "m")
    >>> ans = equivalent_diameter(csa, perimeter)
    >>> print(ans)
    >>> 1.0 m
    """
    
    eq_d = 4 * (cross_sectional_area/wetted_perimeter)
    
    return eq_d


def deltat_logmean(T0A: Temperature, T1A: Temperature,
                   T0B: Temperature, T1B: Temperature, cocurrent: bool = False)-> float:
    """Calculates the temperature delta log mean. For use when evaluating heat transfer in 
    a heat exchanger.

    :param T0A: The temperature of the target fluid when it enters
    :type T0A: Temperature
    :param T1A: The temperature of the target fluid when it exits
    :type T1A: Temperature
    :param T0B: The temperature of the other fluid when it enters
    :type T0B: Temperature
    :param T1B: The temperature of the other fluid when it exits
    :type T1B: Temperature
    :param cocurrent: Whether or not the heat exchanger is cocurrent (False = countercurrent), defaults to False
    :type cocurrent: bool, optional
    :return: The temperature delta log mean
    :rtype: float
    """
    
    if cocurrent:
        side_a_dif = T0A = T0B
        side_b_dif = T1A - T1B
        
    else:
        side_a_dif = T0A - T1B
        side_b_dif = T1A - T0B
    log_mean = (side_a_dif-side_b_dif)/log(side_a_dif/side_b_dif)
    
    return log_mean

def overall_heat_transfer_coefficient():
    pass


@solvable_for(["m1", "m2", "cp1", "cp2", "T0A", "T1A", "T0B", "T1B", "area", "U"], unknowns=2)
def solve_heat_exchanger_system(m1: MultiUnit | None, cp1: Cp | None,
                                m2: MultiUnit | None, cp2: Cp | None,
                                T0A: Temperature | None, T1A: Temperature | None,
                                T0B: Temperature | None, T1B: Temperature | None,
                                area: Area | None, U: MultiUnit | None,
                                cocurrent: bool = False, **kwargs):
    solving_for = kwargs["solving_for"]
    
    x = solving_for[0]
    y = solving_for[1]
    
    eq1 = ["m1", "cp1", "T1A", "T1B"]
    eq2 = ["m2", "cp2", "T0A", "T0B"]
    eq3 = ["U", "A", "T0A", "T0B", "T1A", "T1B"]
    
    if (x == "cp1" and y == "m1") or (x == "cp2" and y == "m2"):
        raise UnsolvableEquation
    
    
def shell_htc_full(fb: float, Ds: Length, Do:Length, 
                         Nb: float, P: Length, p: Length,
                         m_shell: MultiUnit,
                         mu_shell: DynamicViscosity,
                         Cp_shell: Cp, k_shell: ThermalConductivity):
    Sb = Sb_calc(fb, Ds, Nb, Do)
    Sc = Sc_calc(P, Ds, Do, p)
    Ge = Ge_calc(m_shell, Sb, Sc)
    Re = (Do*Ge)/mu_shell
    Pr = prandtl(mu_shell, Cp_shell, k_shell)
    h = htc_shell(Do, Ge, mu_shell, Pr, k_shell, 1)
    
    return h
    
    

    
    
def Ge_calc(m_shell: MultiUnit, Sb: Area, Sc: Area):
    Gb = m_shell/Sb
    Gc = m_shell/Sc
    Ge = (Gb*Gc)**(1/2)
    
    return Ge
    

def Sb_calc(fb: float, Ds: Length, Nb: float, Do: Length)-> Area:
    
    Sb = fb*((pi*Ds**2)/4) - Nb*((pi*Do**2)/4)
    
    return Sb

def Sc_calc(P:Length, Ds: Length, Do:Length, p:Length)-> Area:
    
    Sc = P*Ds*(1-(Do/p))
    
    return Sc

def htc_shell(Do: Length, Ge: MultiUnit, mu: DynamicViscosity, Pr: float, k: ThermalConductivity, psi_v: float=1):
    Nu = 0.2*((Do*Ge)/mu)**(0.6)*Pr**(0.33)*psi_v
    
    h = (Nu*k)/Do
    
    return h

def z_factor(Thot_in: Temperature, Thot_out: Temperature,
             Tcold_in: Temperature, Tcold_out: Temperature):
    """Calculates a z factor used in calculations for shell and tube 
    heat exchangers.

    :param Thot_in: _description_
    :type Thot_in: Temperature
    :param Thot_out: _description_
    :type Thot_out: Temperature
    :param Tcold_in: _description_
    :type Tcold_in: Temperature
    :param Tcold_out: _description_
    :type Tcold_out: Temperature
    :return: _description_
    :rtype: _type_
    """
    z = (Thot_in-Thot_out)/(Tcold_out-Tcold_in)
    
    return z


def nh_factor(Thot_in: Temperature,
             Tcold_in: Temperature, Tcold_out: Temperature)-> float:
    
    nh = (Tcold_out-Tcold_in)/(Thot_in-Tcold_in)
    
    return nh
        
        
    