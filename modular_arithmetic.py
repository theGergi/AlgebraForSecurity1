from helper_methods import *
from integer_arithmetic import *

def modular_reduction(x, modulo, radix):
    modulo = [0] * (len(x) - len(modulo)) + modulo
    while(bigger_than(x, modulo) or x == modulo):
        # print("X: ", x)
        y = modulo + [0] * (len(x) - len(modulo))
        if bigger_than(y, x):
            y = modulo + [0] * (len(x) - len(modulo) - 1)
        # print("Subtractor:", y)
        x = subtraction(x, y, radix)
    return x
    
def modular_addition(x, y, modulo, radix):
    x_modular_representation = modular_reduction(x, modulo, radix)
    y_modular_representation = modular_reduction(y, modulo, radix)
    z = addition(x_modular_representation, y_modular_representation, radix)
    modulo = [0] * (len(z) - len(modulo)) + modulo
    if bigger_than(z, modulo) or z == modulo:
        z = subtraction(z, modulo, radix)
    print(f"the result is {z} mod {modulo}")
    return z

def modular_subtraction(x, y, modulo, radix):
    x_modular_representation = modular_reduction(x, modulo, radix)
    y_modular_representation = modular_reduction(y, modulo, radix)
    z = subtraction(x_modular_representation, y_modular_representation, radix)
    
    if bigger_than([0], z) or z == modulo:
        z = addition(z, modulo, radix)
    print(f"the result is {z} mod {modulo}")
    return z

def modular_multiplication(x,y,modulo,radix):
    x = modular_reduction(x, modulo, radix)
    y = modular_reduction(y, modulo, radix)
    product = multiplication_primary(x, y, radix)
    return modular_reduction(product, modulo, radix)
