from helper_methods import *

def addition(x, y, radix: int):
    """
    Returns the sum of a and b.
    """
    c = 0

    while(len(x) != len(y)):
        if len(x) > len(y):
            y = [0] + y
        else:
            x = [0] + x
    x = [0] + x
    y = [0] + y
    z = [0] * len(x)
    # print(x)
    # print(y)
    for i in range(len(x) - 1, -1, -1):
        z[i] = x[i] + y[i] + c
        if z[i] >= radix:
            z[i] = z[i] - radix
            c = 1
        else:
            c = 0
    # print(z)
    # print(custom_decimal_to_radix(z, radix))
    return remove_leading_zeros_array(z)

def addition_with_negative(x, y, radix, x_negative = False, y_negative = False):
    # Solve integer arithmetic addition exercise
    if x_negative and y_negative:
        return addition(x, y, radix), True
    elif x_negative and not y_negative:
        if bigger_than(x, y):
            return subtraction(x, y, radix), True
        else:
            return subtraction(y, x, radix), False
    elif not x_negative and y_negative:
        if bigger_than(x, y):
            return subtraction(x, y, radix), False
        else:
            return subtraction(y, x, radix), True
    else:
        return addition(x, y, radix), False
    
def subtraction(x, y, radix: int):
    #Returns the dif of a and b.
    c = 0

    #pad the smaller number with 0s to match the larger number in length
    while(len(x) != len(y)):
        if len(x) > len(y):
            y = [0] + y
        else:
            x = [0] + x
    z = [0] * len(x)
    # print(x)
    # print(y)

    #check if y>x and switch the two numbers if that is the case
    if bigger_than(y, x):
        x, y = y, x

    #subtract the 2 numbers
    for i in range(len(x) - 1, -1, -1):
        z[i] = x[i] - y[i] + c
        if z[i] >= 0:
            c = 0
        else:
            z[i] += radix
            c = -1
    # print(z)
    # print(custom_decimal_to_radix(z, radix))
    return z

def subtraction_with_negative(x, y, radix, x_negative = False, y_negative = False):
    if not x_negative and y_negative:
        return addition(x, y, radix), False
    elif x_negative and not y_negative:
        return addition(x, y, radix), True
    elif x_negative and y_negative:
        if bigger_than(x, y):
            return subtraction(x, y, radix), True
        else:
            return subtraction(y, x, radix), False
    else:
        if bigger_than(x, y):
            return subtraction(x, y, radix), False
        else:
            return subtraction(y, x, radix), True

def multiplication_primary(x, y, radix: int):
    x = remove_leading_zeros_array(x)
    y = remove_leading_zeros_array(y)
    if is_zero(x) or is_zero(y):
        return [0]
    while(len(x) != len(y)):
        if len(x) > len(y):
            y = [0] + y
        else:
            x = [0] + x
    c = 0
    z = [0] * (len(x) * 2 + 1)
    for i in range(len(x) - 1, -1, -1):
        inv_i = len(x) - 1 - i
        mid_c = 0
        for j in range(len(y) - 1, -1, -1):
            inv_j = len(y) - 1 - j
            mid_z = x[i] * y[j] + mid_c
            if mid_z >= radix:
                mid_c = mid_z // radix
                mid_z = mid_z % radix
            else:
                mid_c = 0

            z[len(z) - 1 - inv_j - inv_i] = mid_z + z[len(z) - 1 - inv_j - inv_i] + c
            if z[len(z) - 1 - inv_j - inv_i] >= radix:
                c = z[len(z) - 1 - inv_j - inv_i] // radix
                z[len(z) - 1 - inv_j - inv_i] = z[len(z) - 1 - inv_j - inv_i] % radix
            else:
                c = 0
            if j == 0:
                z[len(z) - 2 - inv_j - inv_i] += mid_c + c
                c = 0
    z = remove_leading_zeros_array(z)
    return z

def multiplication_primary_with_negative(x, y, radix, x_negative, y_negative):
    z = multiplication_primary(x, y, radix)

    if x_negative != y_negative:
        return z, True
    else:
        return z, False
    
