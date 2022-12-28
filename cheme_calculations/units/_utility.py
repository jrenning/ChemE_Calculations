from itertools import chain, combinations

__all__ = ["powerset", "to_sup", "remove_zero", "get_prefix"]

# found here https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1)))

def remove_zero(x: float)-> int | float:
    """Removes trailing zeros from numbers that could be integers ie 3.0 -> 3
    

    :param x: number to remove zero from
    :type x: float
    :return: Returns the integer if has a trailing zero, otherwise just returns the input
    :rtype: int | float
    """
    new_x = str(x)
    if ".0" in new_x:
        return int(x)
    else:
        return x


def get_prefix(unit: str)-> tuple:
    """Gets the prefix of a given unit
    
    things that don't have prefixes 
    1. units of only one letter ie m
    2. units that don't start with a prefix
    3. units that aren't covered in the first two and are exceptions
    
    - Returns "" for units without a prefix

    :param unit: The unit to look for a prefix in
    :type unit: str
    :return: tuple of the prefix and the unit with it removed (if there is a prefix)
    :rtype: tuple
    """
    # things that don't have prefixes 
    # 1. units of only one letter ie m
    # 2. units that don't start with a prefix
    # 3. units that aren't covered in the first two and are exceptions
    if len(unit) == 1 or unit[0] not in ["m", "c", "d", "k", "M"] or unit in ["min", "cP"]:
        return ("", unit)
    else:
        return (unit[0], unit[1:])
        

# found here https://stackoverflow.com/questions/13875507/convert-numeric-strings-to-superscript
def to_sup(s):
    sups = {u'0': u'\u2070',
            u'1': u'\xb9',
            u'2': u'\xb2',
            u'3': u'\xb3',
            u'4': u'\u2074',
            u'5': u'\u2075',
            u'6': u'\u2076',
            u'7': u'\u2077',
            u'8': u'\u2078',
            u'9': u'\u2079'}

    return ''.join(sups.get(char, char) for char in s) 




