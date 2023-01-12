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
    

def balance_equation(equation:str):
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
    
    # check if in parentheses
    
    #now we have C3H8, O2 and H2O, CO2
    
    reactant_list = []
    product_list = []
    
   
    product_dict = {}
    
    # Cu2S + HNO3 -> Cu(NO3)2 + CuSO4 + NO2 + H2O
    
  
    for reactant in reactants:
        
        paren_groups = re.findall(r"\(.+\)", reactant)

        if paren_groups:
            for paren_group in paren_groups:
                
                # add backslashes
                paren_group = re.sub("\(", "\\(", paren_group)
                paren_group = re.sub("\)", "\\)", paren_group)
                
                ## do workaround for now as regex is not working 
                # TODO make this better
                idx = reactant.index(")")
                
                # assume multiplier of less than 9
                multiplier = int(reactant[idx+1])
                
                reactant_dict = defaultdict(lambda: 0)

                reactant_dict = _get_chemical_dict(reactant_dict, paren_group, multiplier)
                
                reactant = re.sub(f"{paren_group}\d+", "", reactant)
                
                reactant_dict = _get_chemical_dict(reactant_dict, reactant, 1)
                
                reactant_list.append(reactant_dict)
                
            # go to next product 
            continue
                    
        # pair them up 
        reactant_dict = defaultdict(lambda: 0)
        reactant_dict = _get_chemical_dict(reactant_dict, reactant, 1)
        reactant_list.append(reactant_dict)


        
    for product in products:
        
        paren_groups = re.findall(r"\(.+\)", product)

        if paren_groups:
            for paren_group in paren_groups:
                
                # add backslashes
                paren_group = re.sub("\(", "\\(", paren_group)
                paren_group = re.sub("\)", "\\)", paren_group)
                
                ## do workaround for now as regex is not working 
                # TODO make this better
                idx = product.index(")")
                
                # assume multiplier of less than 9
                multiplier = int(product[idx+1])
                
                product_dict = defaultdict(lambda: 0)

                product_dict = _get_chemical_dict(product_dict, paren_group, multiplier)
                
                product = re.sub(f"{paren_group}\d+", "", product)
                
                product_dict = _get_chemical_dict(product_dict, product, 1)
                
                product_list.append(product_dict)
                
            # go to next product 
            continue
                    
        # pair them up 
        product_dict = defaultdict(lambda: 0)
        product_dict = _get_chemical_dict(product_dict, product, 1)
        product_list.append(product_dict)
        
    
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
    
    # pick high random int as the unsolved coefficient, higher reduces rounding error
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
    
    
    

                    
                    
                
                
                    
    
    