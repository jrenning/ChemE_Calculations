from cheme_calculations.units import MolecularWeight
from cheme_calculations.units.fluids import VolumetricFlowrate
from cheme_calculations.units.mass_transfer import Concentration, MassFlowRate, MassTransferCoefficient
from cheme_calculations.units.units import Area, MultiUnit, Pressure, Temperature

__all__ = ['K_from_standard', "Qm_evaporation", "enclosure_concentration", 
           "ppm_to_other"]

def K_from_standard(M: MolecularWeight)-> MassTransferCoefficient:
    
    K = MassTransferCoefficient(0.83, "cm/s")*(MolecularWeight(18, "g/mol")/M)**(1/3)
    
    return K


def Qm_evaporation(M: MolecularWeight, K: MassTransferCoefficient, 
               A: Area, Psat: Pressure, R: MultiUnit, TL: Temperature)-> MassFlowRate:
    """Calculates the vaporization rate of material leaving a fluid spill or an open 
    container of liquid.
    
    .. math:: Q_m = \dfrac{MKAP^{sat}}{R_gT_L}

    :param M: The molecular weight of the substance
    :type M: MolecularWeight
    :param K: The mass transfer coefficient of the substance
    :type K: MassTransferCoefficient
    :param A: The area of the material that is exposed to the air
    :type A: Area
    :param Psat: Saturation pressure of the material at the given T and P
    :type Psat: Pressure
    :param R: The gas constant (units matching the other values)
    :type R: MultiUnit
    :param TL: Temperature of the liquid
    :type TL: Temperature
    :return: The vaporization rate
    :rtype: MassFlowRate
    
    :Example:
    
    >>> from cheme_calculations.process_safety import Qm_evaporation, K_from_standard
    >>> from cheme_calculations.utility import get_gas_constant
    >>> M = MolecularWeight(65, "g/mol")
    >>> K = K_from_standard(M)
    >>> A = Area(1, "m^2")
    >>> Psat = Pressure(5000, "Pa")
    >>> R = get_gas_constant("K", "m^3", "Pa")
    >>> TL = Temperature(300, "K")
    >>> ans = Qm_evaporation(M, K, A, Psat, R, TL)
    >>> print(ans)
    >>> 0.7049363323151078 g / s
    
    :Reference:
    
    Crowl, D., & Louvar, J. (2019). Chemical Process Safety: Fundamentals with Applications, 4th ed. Pearson.
    """
    
    
    Qm = (M*K*A*Psat)/(R*TL)
    
    return Qm


def enclosure_concentration(Qm: MassFlowRate, Rg: MultiUnit, T: Temperature,
                            k: float, Qv: VolumetricFlowrate, P: Pressure, 
                            M: MolecularWeight)-> float:
    """Calculates the average concentration in a vessel given a evaporation 
    rate of a volatile substance, the ventilation rate, and a mixing factor.
    
    NOTE: This equation assumes steady state
    
    .. math:: C_{ppm} = \dfrac{Q_mR_gT}{kQ_vPM} * 10^6

    :param Qm: The evaporation rate of the volatile substance
    :type Qm: MassFlowRate
    :param Rg: The gas constant
    :type Rg: MultiUnit
    :param T: Temperature in the enclosure
    :type T: Temperature
    :param k: Mixing factor, perfect = 1, usually .1 to .5
    :type k: float
    :param Qv: Ventilation rate 
    :type Qv: VolumetricFlowrate
    :param P: Pressure in the enclosure
    :type P: Pressure
    :param M: Molecular weight of the volatile substance
    :type M: MolecularWeight
    :return: The average concentration in ppm 
    :rtype: Concentration
    
    :Example:
    
    >>> from cheme_calculations.process_safety import enclosure_concentration, ppm_to_other
    >>> from cheme_calculations.utility import get_gas_constant
    >>> M = MolecularWeight(65, "g/mol")
    >>> Qm = MassFlowRate(.7, "g/s")
    >>> Rg = get_gas_constant("K", "m^3", "Pa")
    >>> T = Temperature(300, "K")
    >>> k = 0.35
    >>> Qv = VolumetricFlowrate(5, "m^3/s")
    >>> P = Pressure(1, "atm").convert_to("Pa")
    >>> cppm = enclosure_concentration(Qm, Rg, T, k, Qv, P, M)
    >>> print(cppm)
    >>> 1514.820930364972
    >>> # convert to another concentration
    >>> C = ppm_to_other(cppm, Rg, T, P, M)
    >>> print(C)
    >>> 0.4 g / m³
    
    
    :Reference:
    
    Crowl, D., & Louvar, J. (2019). Chemical Process Safety: Fundamentals with Applications, 4th ed. Pearson.
    """
    
    C_ppm = 10E6*(Qm*Rg*T)/(k*Qv*P*M)
    
    return C_ppm


def ppm_to_other(C_ppm: float, Rg: MultiUnit, T: Temperature, 
                 P: Pressure, M: MolecularWeight)-> Concentration:
    """Converts a concentration in ppm to one based on mass and volume 

    :param C_ppm: The ppm 
    :type C_ppm: float
    :param Rg: The gas constant
    :type Rg: MultiUnit
    :param T: The Temperature of the system 
    :type T: Temperature
    :param P: The pressure of the system 
    :type P: Pressure
    :param M: The molecular weight of the material
    :type M: MolecularWeight
    :return: The new concentration based on the units given 
    :rtype: Concentration
    
    :Example:
    
    >>> M = MolecularWeight(65, "g/mol")
    >>> P = Pressure(1, "atm").convert_to("Pa")
    >>> Rg = get_gas_constant("K", "m^3", "Pa")
    >>> T = Temperature(300, "K")
    >>> cppm = 1514.820930364972
    >>> # convert to another concentration
    >>> C = ppm_to_other(cppm, Rg, T, P, M)
    >>> print(C)
    >>> 0.4 g / m³
    
    """
    
    C = C_ppm/(10E6*(Rg*T)/(P*M))
    
    return C


def soemthing():
    pass