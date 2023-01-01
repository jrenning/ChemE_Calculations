from cheme_calculations.units import Length
from cheme_calculations.units.heat_transfer import HeatTransferCoefficient, ThermalConductivity
from cheme_calculations.units.property_units import DynamicViscosity


__all__ = ["htc_open_field_laminar_local", "htc_open_field_laminar_avg", "wall_viscosity_correction_factor",
           "htc_open_field_turbulent_avg", "htc_open_field_turbulent_local", 
           "htc_pipe_laminar", "htc_pipe_turbulent", "htc_cross_cylinder",
           "htc_cross_sphere", "htc_short_pipe_correction"]

def wall_viscosity_correction_factor(mu: DynamicViscosity, mu_wall: DynamicViscosity)-> float:
    """Calculates a correction factor used in heat transfer coefficient calculations to
    account for the wall fluid's viscosity being different due to temperature, which
    affects hwo much heat is transferred there.

    :param mu: Viscosity of the bulk fluid
    :type mu: DynamicViscosity
    :param mu_wall: Viscosity of the fluid at the wall
    :type mu_wall: DynamicViscosity
    :return: The correction factor
    :rtype: float
    """
    return (mu/mu_wall)**(0.14)

def htc_open_field_laminar_local(Re: float, Pr: float, L: Length,
                             k: ThermalConductivity, psi_v: float=1)-> HeatTransferCoefficient:
    """Calculates the heat transfer coefficient for open field flow with a laminar flow profile at a local point
    
    .. math:: Nu = 0.332Re^{1/2}Pr^{1/3}*\psi_v
    .. math:: h = (Nu*k)/L

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandlt number of the fluid
    :type Pr: float
    :param L: The length of the object flow is against
    :type L: Length
    :param k: Thermal conductivity of the fluid
    :type k: ThermalConductivity
    :param psi_v: A correction factor for the change in viscosity between the bulk fluid and the wall fluid, defaults to 1
    :type psi_v: float, optional
    :return: A heat transfer coefficient
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_open_field_laminar_local
    >>> Re = 200000
    >>> Pr = 0.78
    >>> L = Length(50, "m")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> h = htc_open_field_laminar_local(Re, Pr, L, k)
    >>> print(h)
    >>> 1.6400831313611866 W / m² * K
    """
    Nu_local: float = 0.332*Re**(1/2)*Pr**(1/3)*psi_v
    h = (Nu_local * k) / L
    # TODO make this unneeded
    if "BTU" in k.__repr__():
        h.convert_to("BTU/hr*ft^2*F", True)
    else:
        h.convert_to("W/m^2*K", True)
    return HeatTransferCoefficient(h._value, top_half=h._top_half, bottom_half=h._bottom_half)
    

def htc_open_field_laminar_avg(Re: float, Pr: float, L: Length,
                             k: ThermalConductivity, psi_v: float=1):
    """Calculates the average heat transfer coefficient for open field flow with a laminar flow profile
    
    .. math:: Nu = 0.664Re^{1/2}Pr^{1/3}*\psi_v
    .. math:: h = (Nu*k)/L

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandlt number of the fluid
    :type Pr: float
    :param L: The length of the object flow is against
    :type L: Length
    :param k: Thermal conductivity of the fluid
    :type k: ThermalConductivity
    :param psi_v: A correction factor for the change in viscosity between the bulk fluid and the wall fluid, defaults to 1
    :type psi_v: float, optional
    :return: A heat transfer coefficient
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_open_field_laminar_avg
    >>> Re = 200000
    >>> Pr = 0.78
    >>> L = Length(50, "m")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> h = htc_open_field_laminar_local(Re, Pr, L, k)
    >>> print(h)
    >>> 3.280166262722373 W / m² * K
    """
    
    Nu_local: float = 0.664*Re**(1/2)*Pr**(1/3)*psi_v
    h = (Nu_local * k) / L
    if "BTU" in k.__repr__():
        h.convert_to("BTU/hr*ft^2*F", True)
    else:
        h.convert_to("W/m^2*K", True)
    return HeatTransferCoefficient(h._value, top_half=h._top_half, bottom_half=h._bottom_half)


def htc_open_field_turbulent_avg(Re: float, Pr: float, L: Length, 
                             k: ThermalConductivity, psi_v: float=1)-> HeatTransferCoefficient:
    """Calculates a heat transfer coefficient for turbulent open field flow using 
    an average value calculated across the whole length of the flow.
    
    .. math:: Nu = 0.037RE^{0.8}Pr^{1/3} \psi_v - 871Pr^{1/3} \psi_v
    .. math:: h = (Nu*k)/L

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandtl number of the fluid
    :type Pr: float
    :param L: The length the flow is occurring on 
    :type L: Length
    :param k: The thermal conductivity of the fluid
    :type k: ThermalConductivity
    :param psi_v: A correction factor for the change in viscosity between the bulk fluid and the wall fluid, defaults to 1
    :type psi_v: float, optional
    :return: The heat transfer coefficient for the system
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_open_field_turbulent_avg, wall_viscosity_correction_factor
    >>> from cheme_calculations.utility import reynolds, prandtl
    >>> rho = Density(800, "kg/m^3")
    >>> v = Velocity(5, "m/s")
    >>> L = Length(500, "m")
    >>> mu = DynamicViscosity(0.001, "kg/m*s")
    >>> mu_wall = DynamicViscosity(.0007, "kg/m*s")
    >>> cp = Cp(4.18, "kJ/kg*K")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> Re = reynolds(rho, v, L, mu)
    >>> Pr = prandtl(cp, mu, k)
    >>> psi_v = wall_viscosity_correction_factor(mu, mu_wall)
    >>> ans = htc_open_field_turbulent_avg(Re, Pr, L, k, psi_v)
    >>> print(ans)
    >>> 2457.7116974456826 W / m² * K
    """
    
    Nu = 0.037*Re**(0.8)*Pr**(1/3)*psi_v - 871*Pr**(1/3)*psi_v
    
    h = (Nu * k)/L
    
    return h

def htc_open_field_turbulent_local(Re: float, Pr: float, L: Length, 
                             k: ThermalConductivity, psi_v: float=1)-> HeatTransferCoefficient:
    """Calculates a heat transfer coefficient for turbulent open field flow using 
    an average value calculated across the whole length of the flow.
    
    .. math:: Nu = 0.037RE^{0.8}Pr^{1/3} \psi_v - 871Pr^{1/3} \psi_v
    .. math:: h = (Nu*k)/L

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandtl number of the fluid
    :type Pr: float
    :param L: The length the flow is occurring on 
    :type L: Length
    :param k: The thermal conductivity of the fluid
    :type k: ThermalConductivity
    :param psi_v: A correction factor for the change in viscosity between the bulk fluid and the wall fluid, defaults to 1
    :type psi_v: float, optional
    :return: The heat transfer coefficient for the system
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_open_field_turbulent_local, wall_viscosity_correction_factor
    >>> from cheme_calculations.utility import reynolds, prandtl
    >>> rho = Density(800, "kg/m^3")
    >>> v = Velocity(5, "m/s")
    >>> L = Length(500, "m")
    >>> mu = DynamicViscosity(0.001, "kg/m*s")
    >>> mu_wall = DynamicViscosity(.0007, "kg/m*s")
    >>> cp = Cp(4.18, "kJ/kg*K")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> Re = reynolds(rho, v, L, mu)
    >>> Pr = prandtl(cp, mu, k)
    >>> psi_v = wall_viscosity_correction_factor(mu, mu_wall)
    >>> ans = htc_open_field_turbulent_local(Re, Pr, L, k, psi_v)
    >>> print(ans)
    >>> 1967.8481001505118 W / m² * K
    """
    
    Nu = 0.0296*Re**(0.8)*Pr**(1/3)*psi_v
    
    h = (Nu * k)/L
    
    return h


def htc_pipe_laminar(Re: float, Pr: float, diameter: Length, L: Length, 
                     k: ThermalConductivity, psi_v: float=1)-> HeatTransferCoefficient:
    """Calculates a heat transfer coefficient for a laminar fluid flowing in a pipe.
    Laminar flow generally is when the reynolds number is below 2000 (for a pipe)
    
    .. math:: Nu = 1.85*(RePr*\dfrac{diameter}{length})^{1/3}*\psi_v
    .. math:: h = (Nu*k)/diameter

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandtl number of the fluid
    :type Pr: float
    :param diameter: The diameter of the pipe
    :type diameter: Length
    :param l: the length of the pipe
    :type l: Length
    :param k: The thermal conductivity of the fluid
    :type k: ThermalConductivity
    :param psi_v: A correction factor for the change in viscosity between the bulk fluid and the wall fluid, defaults to 1
    :type psi_v: float, optional
    :return: A heat transfer coefficient
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_pipe_laminar, wall_viscosity_correction_factor
    >>> from cheme_calculations.utility import reynolds, prandtl
    >>> rho = Density(800, "kg/m^3")
    >>> v = Velocity(.1, "m/s")
    >>> L = Length(1, "m")
    >>> diameter = Length(0.01, "m")
    >>> mu = DynamicViscosity(0.001, "kg/m*s")
    >>> mu_wall = DynamicViscosity(.0007, "kg/m*s")
    >>> cp = Cp(4.18, "kJ/kg*K")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> Re = reynolds(rho, v, diameter, mu)
    >>> Pr = prandtl(cp, mu, k)
    >>> psi_v = wall_viscosity_correction_factor(mu, mu_wall)
    >>> ans = htc_pipe_laminar(Re, Pr,diameter, L, k, psi_v)
    >>> print(ans)
    >>> 445.70508881121214 W / m² * K
    """

    Nu = 1.85*(Re*Pr*(diameter/L))**(1/3)*psi_v
    
    h = (Nu * k)/diameter
    
    return h

def htc_pipe_turbulent(Re: float, Pr: float, diameter: Length, 
                     k: ThermalConductivity, psi_v: float=1)-> HeatTransferCoefficient:
    """Calculates a heat transfer coefficient for a turbulent fluid flowing in a pipe.
    Laminar flow generally is when the reynolds number is below 2000 (for a pipe)
    
    .. math:: Nu = 0.023Re^{0.8}Pr^{1/3}* \psi_v
    .. math:: h = (Nu*k)/diameter

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandtl number of the fluid
    :type Pr: float
    :param diameter: The diameter of the pipe
    :type diameter: Length
    :param k: The thermal conductivity of the fluid
    :type k: ThermalConductivity
    :param psi_v: A correction factor for the change in viscosity between the bulk fluid and the wall fluid, defaults to 1
    :type psi_v: float, optional
    :return: A heat transfer coefficient
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_pipe_turbulent, wall_viscosity_correction_factor
    >>> from cheme_calculations.utility import reynolds, prandtl
    >>> rho = Density(800, "kg/m^3")
    >>> v = Velocity(5, "m/s")
    >>> diameter = Length(0.1, "m")
    >>> mu = DynamicViscosity(0.001, "kg/m*s")
    >>> mu_wall = DynamicViscosity(.0007, "kg/m*s")
    >>> cp = Cp(4.18, "kJ/kg*K")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> Re = reynolds(rho, v, diameter, mu)
    >>> Pr = prandtl(cp, mu, k)
    >>> psi_v = wall_viscosity_correction_factor(mu, mu_wall)
    >>> ans = htc_pipe_turbulent(Re, Pr,diameter, k, psi_v)
    >>> print(ans)
    >>> 8398.886215378532 W / m² * K
    """

    Nu = 0.023*Re**(0.8)*Pr**(1/3)*psi_v
    
    h = (Nu * k)/diameter
    
    return h


def htc_cross_cylinder(Re: float, Pr: float, diameter: Length, 
                     k: ThermalConductivity)-> HeatTransferCoefficient:
    """Calculates a heat transfer coefficient for flow of a fluid across 
    cylinders in an open field scenario.
    
    .. math:: Nu = 0.35Pr^{0.3} + 0.56Re^{0.52}Pr^{0.3}
    .. math:: h = (Nu*k)/diameter

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandtl number of the fluid
    :type Pr: float
    :param diameter: The diameter of the cylinder flow is going across
    :type diameter: Length
    :param k: The thermal conductivity of the fluid
    :type k: ThermalConductivity
    :return: A heat transfer coefficient
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_cross_cylinder
    >>> from cheme_calculations.utility import reynolds, prandtl
    >>> rho = Density(800, "kg/m^3")
    >>> v = Velocity(5, "m/s")
    >>> diameter = Length(0.1, "m")
    >>> mu = DynamicViscosity(0.001, "kg/m*s")
    >>> cp = Cp(4.18, "kJ/kg*K")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> Re = reynolds(rho, v, diameter, mu)
    >>> Pr = prandtl(cp, mu, k)
    >>> ans = htc_cross_cylinder(Re, Pr,diameter, k)
    >>> print(ans)
    >>> 4927.758769048417 W / m² * K
    """

    Nu = 0.35*Pr**(0.3)+0.56*(Re)**(0.52)*Pr**(0.3)
    
    h = (Nu * k)/diameter
    
    return h

def htc_cross_sphere(Re: float, Pr: float, diameter: Length, 
                     k: ThermalConductivity)-> HeatTransferCoefficient:
    """Calculates a heat transfer coefficient for flow of a fluid across 
    spheres in an open field scenario.
    
    .. math:: Nu = 2 + 0.60Re^{1/2}Pr^{1/3}
    .. math:: h = (Nu*k)/diameter

    :param Re: The Reynolds number of the fluid
    :type Re: float
    :param Pr: The Prandtl number of the fluid
    :type Pr: float
    :param diameter: The diameter of the sphere flow is going across
    :type diameter: Length
    :param k: The thermal conductivity of the fluid
    :type k: ThermalConductivity
    :return: A heat transfer coefficient
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_cross_sphere
    >>> from cheme_calculations.utility import reynolds, prandtl
    >>> rho = Density(800, "kg/m^3")
    >>> v = Velocity(5, "m/s")
    >>> diameter = Length(0.1, "m")
    >>> mu = DynamicViscosity(0.001, "kg/m*s")
    >>> cp = Cp(4.18, "kJ/kg*K")
    >>> k = ThermalConductivity(0.6, "W/m*K")
    >>> Re = reynolds(rho, v, diameter, mu)
    >>> Pr = prandtl(cp, mu, k)
    >>> ans = htc_cross_sphere(Re, Pr,diameter, k)
    >>> print(ans)
    >>> 4360.51367566926 W / m² * K
    """
    
    Nu = 2 + 0.60*Re**(1/2)*Pr**(1/3)
    
    h = (Nu * k)/diameter
    
    return h

def htc_short_pipe_correction(h: HeatTransferCoefficient, diameter: Length, L: Length)-> HeatTransferCoefficient:
    """Calculates a new heat transfer coefficient for a short
    pipe based on a coefficient that was calculated for a pipe in general.
    Used when the 
    
    .. math:: h = h_\infty * (1 + \dfrac({diameter}{length})^{0.7})

    :param h: A heat transfer coefficient calculated for the pipe independent of its length
    :type h: HeatTransferCoefficient
    :param diameter: Diameter of the pipe
    :type diameter: Length
    :param L: Length of the pipe
    :type L: Length
    :return: A new corrected heat transfer coefficient
    :rtype: HeatTransferCoefficient
    
    :Example:
    
    >>> from cheme_calculations.heat_transfer import htc_short_pipe_correction
    >>> h = HeatTransferCoefficient(400, "W/m^2*K")
    >>> diameter = Length(1, "m")
    >>> L = Length(1, "m")
    >>> ans = htc_short_pipe_correction(h, diameter, L)
    >>> print(ans)
    >>> 800.0 W / m² * K
    """
    
    h_new = h*(1+(diameter/L)**(0.7))
    
    return h_new