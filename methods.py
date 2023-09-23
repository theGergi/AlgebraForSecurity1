from helper_methods import *
from integer_arithmetic import *
    
def find_sum(str1, str2,radix:int):
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    str1 = str1[::-1]
    str2 = str2[::-1]

    n1 = len(str1)
    n2 = len(str2)

    carry = 0
    result = []

    for i in range(n1):
        sum_digit = int(str1[i]) + int(str2[i]) + carry
        result.append(str(sum_digit % radix))
        carry = sum_digit // radix

    for i in range(n1, n2):
        sum_digit = int(str2[i]) + carry
        result.append(str(sum_digit % radix))
        carry = sum_digit // radix

    if carry:
        result.append(str(carry))

    result.reverse()
    return ''.join(result)

def find_diff(str1, str2,radix:int):
    str1 = str1[::-1]
    str2 = str2[::-1]

    n1 = len(str1)
    n2 = len(str2)

    carry = 0
    result = []

    for i in range(n2):
        sub = int(str1[i]) - int(str2[i]) - carry
        if sub < 0:
            sub += radix
            carry = 1
        else:
            carry = 0
        result.append(str(sub))

    for i in range(n2, n1):
        sub = int(str1[i]) - carry
        if sub < 0:
            sub += radix
            carry = 1
        else:
            carry = 0
        result.append(str(sub))

    result.reverse()
    return ''.join(result)

def karatsuba(A, B,radix:int):
    if len(A) > len(B):
        A, B = B, A

    n1 = len(A)
    n2 = len(B)

    while n2 > n1:
        A = '0' + A
        n1 += 1

    if n1 == 1:
        ans = int(A) * int(B)
        return str(ans)

    if n1 % 2 == 1:
        n1 += 1
        A = '0' + A
        B = '0' + B

    Al = A[:n1 // 2]
    Ar = A[n1 // 2:]
    Bl = B[:n1 // 2]
    Br = B[n1 // 2:]

    p = karatsuba(Al, Bl, radix)
    q = karatsuba(Ar, Br, radix)
    r = find_diff(karatsuba(find_sum(Al, Ar, radix), find_sum(Bl, Br, radix),radix), find_sum(p, q, radix), radix)

    for i in range(n1):
        p += '0'
    for i in range(n1 // 2):
        r += '0'

    ans = find_sum(p, find_sum(q, r,radix),radix)
    ans = remove_leading_zeros(ans)

    return ans

def modular_reduction_array(x, modulo, radix):
    modulo = [0] * (len(x) - len(modulo)) + modulo
    while(bigger_than(x, modulo)):
        # print("X: ", x)
        y = modulo + [0] * (len(x) - len(modulo))
        if bigger_than(y, x):
            y = modulo + [0] * (len(x) - len(modulo) - 1)
        # print("Subtractor:", y)
        x = subtraction(x, y, radix)
    print(custom_decimal_to_radix(x, radix))
    print(x)
    return x
    
def modular_addition(x, y, modulo, radix):
    x_modular_representation = modular_reduction_array(x, modulo, radix)
    y_modular_representation = modular_reduction_array(y, modulo, radix)
    z = addition(x_modular_representation, y_modular_representation, radix)
    modulo = [0] * (len(z) - len(modulo)) + modulo
    if bigger_than(z, modulo) or z == modulo:
        z = subtraction(z, modulo, radix)
    print(f"the result is {z} mod {modulo}")
    return z

def modular_reduction(x, modulo: int):
    w = modulo

    while x> w*w:
        w = w*w

    w = x - w 
    print(f"{x} equals {w} mod {modulo}")
    return w

def modular_subtraction(x, y, modulo, radix):
    x_modular_representation = modular_reduction_array(x, modulo, radix)
    y_modular_representation = modular_reduction_array(y, modulo, radix)
    z = subtraction(x_modular_representation, y_modular_representation, radix)
    
    if bigger_than([0], z) or z == modulo:
        z = addition(z, modulo, radix)
    print(f"the result is {z} mod {modulo}")
    return z


def mod(a, b, radix, a_negative, b_negative):
    nr=0
    while bigger_than(a, b):
        a, a_negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
    a_minus_b, negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
    if(is_zero(a_minus_b)):
        a, a_negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
    return a, a_negative

def div(a, b, radix, a_negative, b_negative):
    nr = 0
    a_bigger = bigger_than(a, b)
    while bigger_than(a, b):
        a, a_negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
        nr=nr+1
    if(is_zero(subtraction_with_negative(a, b, radix, a_negative, b_negative)[0])):
        a, a_negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
        nr=nr+1
    nr=str(nr)
    nr=custom_radix_to_decimal(nr, radix)
    return nr, not a_bigger

def gcd(a, b, radix):
    while is_zero(b) == False:
        a, b = b, mod(a, b, radix)
    return a



def extended_gcd(a, b, radix, a_negative, b_negative):
    print("A: ", a, a_negative)
    print("B: ", b, b_negative)
    if is_zero(a):
        return b, [0], [1], True, b_negative
    mod_ab, mod_ab_negative = mod(b, a, radix, b_negative, a_negative)
    gcd, x1, y1, x1_negative, y1_negative = extended_gcd(mod_ab, a, radix, mod_ab_negative, a_negative)
    print(b, a)
    r, r_negative = div(b, a, radix, b_negative, a_negative)
    r_x1, r_x1_negative = multiplication_primary_with_negative(r, x1, radix, r_negative, x1_negative)
    x, x_negative = subtraction_with_negative(y1, r_x1, radix, y1_negative, r_x1_negative)
    y = x1

    return gcd, x, y, x_negative, x1_negative


def modular_inverse(a, m, radix):
    gcd, x, y = extended_gcd(a, m, radix)
    
    if is_zero(gcd):
        raise ValueError("Modular inverse does not exist.")
    
    inverse = mod(x, m, radix)  # Calculate the modular inverse using your mod function
    return inverse
