from helper_methods import *
from integer_arithmetic import *

def modular_reduction(x:list[int], modulo:list[int], radix: int):
    """
        Performs modular reduction on a number x with modulo
    """
    while(bigger_than(x, modulo) or x == modulo):
        # Multiplies the modulo by the radix until the we get a number that is just smaller than x
        y = modulo + [0] * (len(x) - len(modulo))
        if bigger_than(y, x):
            y = modulo + [0] * (len(x) - len(modulo) - 1)
        # Remove unnecessary leading zeros
        x = remove_leading_zeros_array(subtraction(x, y, radix))
    return x
    
def modular_addition(x, y, modulo, radix, x_negative, y_negative):
    """
    Returns the modulo sum of 2 integers x and y.
    """
    # Reduce x and y
    x_modular_representation = modular_reduction(x, modulo, radix)
    y_modular_representation = modular_reduction(y, modulo, radix)

    z, z_negative = addition_with_negative(x_modular_representation, y_modular_representation, radix, x_negative, y_negative)
    
    # If the product is negative than we add the modulo once
    # If the product is bigger than the modulo than we subtract the modulo once
    if z_negative:
        z = subtraction(modulo, z, radix)
    if bigger_than(z, modulo) or z == modulo:
        z = subtraction(z, modulo, radix)
    return z

def modular_subtraction(x, y, modulo, radix, x_negative, y_negative):
    """
    Returns the modulo difference of 2 integers x and y.
    """
    # Reduce x and y
    x_modular_representation = modular_reduction(x, modulo, radix)
    y_modular_representation = modular_reduction(y, modulo, radix)
    
    z, z_negative = subtraction_with_negative(x_modular_representation, y_modular_representation, radix, x_negative, y_negative)
    
    # If the product is negative than we add the modulo once
    # If the product is smaller than 0 or equal to the modulo than we subtract the modulo once
    if z_negative:
        z = subtraction(modulo, z, radix)
    if bigger_than([0], z) or z == modulo:
        z = addition(z, modulo, radix)
    return z

def modular_multiplication(x,y,modulo,radix, x_negative, y_negative):
    """
    Returns the modulo product of 2 integers x and y.
    """
    # Reduce x and y
    x = modular_reduction(x, modulo, radix)
    y = modular_reduction(y, modulo, radix)

    product = multiplication_primary(x, y, radix)

    # Reduce product
    product = modular_reduction(product, modulo, radix)

    # If the product is negative then add the modulo once
    if x_negative != y_negative and not is_zero(product):
        product = subtraction(modulo, product, radix)
    return product

def modular_inverse(a, modulo, radix, a_negative, m_negative):
    """
    Returns the modular inverse of an integer x with modulo.
    """
    # Find the gcd of a and modulo
    gcd, x, y, x_negative, y_negative = extended_gcd(a, modulo, radix, a_negative, m_negative)
    
    if not is_one(gcd):
        return None, None
    
    # Do a modular reduction on x
    inverse = modular_reduction(x, modulo, radix)

    # If x is negative then add the modulo to make x positive
    if x_negative:
        inverse = subtraction(modulo, inverse, radix)
    return inverse, False
