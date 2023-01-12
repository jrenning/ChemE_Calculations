from collections import defaultdict
from email.mime import multipart
from fractions import Fraction
import math
from pprint import pprint
import re
from itertools import chain
from typing import List
import numpy as np


class InvalidParentheses(Exception):
    pass

class ImproperChemicalEquation:
    pass

__all__ = ["balance_equation"]


def _check_valid_parenthese(equation: str):
    char_list = ["()"]
    while any(x in equation for x in char_list):
        for char in char_list:
            equation = equation.replace(char, "")
    return not equation


def _get_chemical_dict(chemical_dict: dict, search_group: str, multiplier: int):
    elements = re.findall(r"[A-Z][a-z]?\d+|[A-Z][a-z]?", search_group)      
    # pair them up 
    for element in elements:
        if re.findall(r"\d", element):
            coefficient = re.findall(r"\d+", element)
            ele, _ = re.split("\d+", element)
            chemical_dict[ele] += int(coefficient[0])*multiplier
        else:
            chemical_dict[element] += 1*multiplier
    return chemical_dict



def _get_fraction_lcm(fraction_list: List[Fraction]):
    frac_tuples = [x.as_integer_ratio() for x in fraction_list]
    num = [x[0] for x in frac_tuples]
    den = [x[1] for x in frac_tuples]
    
    numerator = math.gcd(*num)
    denominator = math.lcm(*den)


    return Fraction(denominator/numerator).limit_denominator()


def _parse_equation_side(side: List[str]):
    
    molecule_list = []
    for molecule in side:
    
        paren_groups = re.findall(r"\(.+\)", molecule)

        if paren_groups:
            for paren_group in paren_groups:
                
                # add backslashes
                paren_group = re.sub("\(", "\\(", paren_group)
                paren_group = re.sub("\)", "\\)", paren_group)
                
                ## do workaround for now as regex is not working 
                # TODO make this better
                idx = molecule.index(")")
                
                # assume multiplier of less than 9
                multiplier = int(molecule[idx+1])
                
                molecule_dict = defaultdict(lambda: 0)

                molecule_dict = _get_chemical_dict(molecule_dict, paren_group, multiplier)
                
                molecule = re.sub(f"{paren_group}\d+", "", molecule)
                
                molecule_dict = _get_chemical_dict(molecule_dict, molecule, 1)
                
                molecule_list.append(molecule_dict)
                
            # go to next product 
            continue
                    
        # pair them up 
        molecule_dict = defaultdict(lambda: 0)
        molecule_dict = _get_chemical_dict(molecule_dict, molecule, 1)
        molecule_list.append(molecule_dict)
        
    return molecule_list
    

def balance_equation(equation:str)-> str:
    """Balances a string representing a chemical equation, returns the balanced 
    equation in the simplest form possible with integer coefficients
    
    NOTE: The function assumes that there are no preexisting coefficients on the molecules, they will
    be ignored in the balancing, so distribute them if necessary 
    NOTE: Currently the function does not allow subscripts outside parentheses greater than 9 (this will be fixed later)
    

    :param equation: The string representing the equation to balance 
    :type equation: str
    :raises InvalidParentheses: Raises an error if the parentheses dont match in the equation ie missing one
    :raises ImproperChemicalEquation: Raises an error if the equation is impossible to balance ie one side has an element the other doesn't
    :return: The new balanced chemical equation
    :rtype: str
    
    :Example:
    
    >>> from cheme_calculations.reactions import balance_equation
    >>> eq1 = "Al + O2 -> Al2O3"
    >>> eq2 = "KI + Pb(NO3)2 -> KNO3 + PbI2"
    >>> eq3 = "H3PO4 + (NH4)2MoO4 + HNO3 -> (NH4)3PO4Mo12O36 + NH4NO3 + H2O"
    >>> balanced1 = balance_equation(eq1)
    >>> balanced2 = balance_equation(eq2)
    >>> balanced3 = balance_equation(eq3)
    >>> print(balanced1)
    >>> 4.0 Al + 3.0 O2 -> 2.0 Al2O3
    >>> print(balanced2)
    >>> 2.0 KI + 1.0 Pb(NO3)2 -> 2.0 KNO3 + 1.0 PbI2
    >>> print(balanced3)
    >>> 1.0 H3PO4 + 12.0 (NH4)2MoO4 + 21.0 HNO3 -> 1.0 (NH4)3PO4Mo12O36 + 21.0 NH4NO3 + 12.0 H2O
    
    """
    # sample equation to parse 
    # C3H8 + O2 -> H2O + CO2
    # assume there are no existing coefficients
    
    # check for valid parentheses
    if not _check_valid_parenthese:
        raise InvalidParentheses(f"The parentheses in the equation {equation} are invalid")
    
    # split on the arrow 
    left_side, right_side = equation.split("->")
    
    # now we have C3H8 + O2 and H2O + CO2
    
    # split on the +
    reactants = left_side.split("+")
    products = right_side.split("+")
    
    # strip whitespace 
    reactants = [x.strip() for x in reactants]
    products = [x.strip() for x in products]
    
    # Cu2S + HNO3 -> Cu(NO3)2 + CuSO4 + NO2 + H2O
    
    reactant_list = _parse_equation_side(reactants)
    
    product_list = _parse_equation_side(products)
        
    # get unique products and reactants
    unique_reactants = list(set(chain.from_iterable(d.keys() for d in reactant_list)))
    unique_products = list(set(chain.from_iterable(d.keys() for d in product_list)))
    
    if set(unique_products) != set(unique_reactants):
        raise ImproperChemicalEquation("There are elements that are on one side but not the other")
    
    # make the matrix 
    cols = []
    for reactant in reactant_list:
        col = np.zeros(len(unique_reactants))
        for element, value in reactant.items():
            col[unique_reactants.index(element)] = value
        cols.append(col)
        
    for product in product_list:
        col = np.zeros(len(unique_reactants))
        for element, value in product.items():
            # negative for the product side
            col[unique_reactants.index(element)] = -value
        cols.append(col)
    
    chemical_matrix = np.column_stack(cols)
    
    x = np.linalg.lstsq(chemical_matrix[:, :-1], chemical_matrix[:, -1], rcond=None)[0]
    
    # flip sign
    x = -x
    
    # get fraction representation
    x = [Fraction(x).limit_denominator() for x in x]
    
    # get lcm of all the fractions
    lcm = _get_fraction_lcm(x)
    
    # multiple represents the free variable in the matrix solution
    # set the multiple to the lcm, this makes it so all the fractions are now integers (technically speaking
    # , they are floats but can easily be cast to integers ie 4.0 -> 4)
    multiple = lcm
    sol = [x*multiple for x in x]
    sol.append(multiple)
    sol = [int(x) for x in sol]
    gcd = math.gcd(*sol)
    
    # # divide by gcd to get the most simplified coefficients
    sol = [x/gcd for x in sol]
    
    react_coeff = sol[:len(reactants)]
    product_coeff = sol[len(reactants):]
    
    # return string
    reactant_string = " + ".join([f"{x} {y}" for x,y in zip(react_coeff, reactants)])
    product_string = " + ".join([f"{x} {y}" for x,y in zip(product_coeff, products)])
    
    return f"{reactant_string} -> {product_string}"
    
    
    

                    
                    
                
                
                    
    
    