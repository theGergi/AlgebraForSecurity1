from helper_methods import *
from integer_arithmetic import *

def modular_reduction(x, modulo, radix):
    # modulo = [0] * (len(x) - len(modulo)) + modulo
    while(bigger_than(x, modulo) or x == modulo):
        
        y = modulo + [0] * (len(x) - len(modulo))
        
        if bigger_than(y, x):
            y = modulo + [0] * (len(x) - len(modulo) - 1)
        x = remove_leading_zeros_array(subtraction(x, y, radix))
    return x
    
def modular_addition(x, y, modulo, radix, x_negative, y_negative):
    x_modular_representation = modular_reduction(x, modulo, radix)
    y_modular_representation = modular_reduction(y, modulo, radix)
    z, z_negative = addition_with_negative(x_modular_representation, y_modular_representation, radix, x_negative, y_negative)
    if z_negative:
        z = subtraction(modulo, z, radix)
    if bigger_than(z, modulo) or z == modulo:
        z = subtraction(z, modulo, radix)
    return z

def modular_subtraction(x, y, modulo, radix, x_negative, y_negative):
    x_modular_representation = modular_reduction(x, modulo, radix)
    y_modular_representation = modular_reduction(y, modulo, radix)
    z, z_negative = subtraction_with_negative(x_modular_representation, y_modular_representation, radix, x_negative, y_negative)
    if z_negative:
        z = subtraction(modulo, z, radix)
    if bigger_than([0], z) or z == modulo:
        z = addition(z, modulo, radix)
    return z

def modular_multiplication(x,y,modulo,radix, x_negative, y_negative):
    x = modular_reduction(x, modulo, radix)
    y = modular_reduction(y, modulo, radix)
    product = multiplication_primary(x, y, radix)
    product = modular_reduction(product, modulo, radix)
    if x_negative != y_negative and not is_zero(product):
        product = subtraction(modulo, product, radix)
    return product
