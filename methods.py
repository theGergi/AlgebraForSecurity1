from helper_methods import *
from integer_arithmetic import *
from modular_arithmetic import *

def multiplication_karatsuba (x,y,radix:int):
    
    if len(x) > len(y):
        x, y = y, x 
    
    n1 = len(x)
    n2 = len(y) 
    
    x = [0]*(n2-n1) + x
    
    #padding zeros at the beginning of the smaller number in order for the numbers to have the same number of digits
    
    n1,n2 = max(n1,n2),max(n1,n2)
    
    #base case
    if (n1 == 1): 
        ans = multiplication_primary(x,y,radix)
        return ans
        
    #in case the number of digits is odd, pad with a zero
    #to make it even
    if (n1 % 2 == 1):
        n1 += 1
        n2 += 1
        x = [0] + x
        y = [0] + y

    xl = []
    xr = []
    yl = []
    yr = []
    
    #find the values of xl, xr, yl, yr 
    #which are needed fot karatsuba multiplication
    
    xl = x[:n1//2]
    xr = x[n1//2:]
    yl = y[:n2//2]
    yr = y[n2//2:]

    p = []
    p = multiplication_karatsuba(xl, yl, radix)

    q = []
    q = multiplication_karatsuba(xr, yr, radix)

    r = []

    # a lot of lists are added to make the code easier to follow
    # and also easier to debug 
    
    addition_of_xl_and_xr = addition(xl,xr,radix)
    t1 = addition_of_xl_and_xr 
    t1 = remove_leading_zeros(t1)

    addition_of_yl_and_yr = addition(yl,yr,radix)
    t2 = addition_of_yl_and_yr 
    t2 = remove_leading_zeros(t2)

    kar_of_sum = multiplication_karatsuba(t1,t2,radix)
    t3 = kar_of_sum

    addition_of_p_and_q = addition(p,q,radix)
    t4 = addition_of_p_and_q


    r = subtraction(t3 , t4 , radix)

    # Multiply p by 10^n
    p = p + [0]*n1

    # Multiply r by 10^(n/2)
    r = r + [0]*(n1//2)

    z = [] 
    #calculate final answer
    z = addition(p, addition(q, r,radix),radix)

    z = remove_leading_zeros(z)
    
    return custom_decimal_to_radix(z,radix) 

def mod(a, b, radix, a_negative, b_negative):
    nr=0
    while bigger_than(a, b):
        a, a_negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
    a_minus_b, negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
    if(is_zero(a_minus_b)):
        a, a_negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
    return a, a_negative

def div(a, b, radix, a_negative, b_negative):
    nr = [0]
    a_bigger = bigger_than(a, b)
    while bigger_than(a, b):
        a, a_negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
        nr = addition(nr, [1], radix)
    if(is_zero(subtraction_with_negative(a, b, radix, a_negative, b_negative)[0])):
        a, a_negative = subtraction_with_negative(a, b, radix, a_negative, b_negative)
        nr = addition(nr, [1], radix)
        # nr=nr+1
    # nr=str(nr)
    # nr=custom_radix_to_decimal(nr, radix)
    return nr, not a_bigger

def gcd(a, b, radix):
    while is_zero(b) == False:
        a, b = b, mod(a, b, radix)
    return a



def extended_gcd(a, b, radix, a_negative, b_negative):

    if is_zero(a):
        return b, [0], [1], True, b_negative
    mod_ab, mod_ab_negative = mod(b, a, radix, b_negative, a_negative)
    
    gcd, x1, y1, x1_negative, y1_negative = extended_gcd(mod_ab, a, radix, mod_ab_negative, a_negative)
    r, r_negative = div(b, a, radix, b_negative, a_negative)
    r_x1, r_x1_negative = multiplication_primary_with_negative(r, x1, radix, r_negative, x1_negative)
    x, x_negative = subtraction_with_negative(y1, r_x1, radix, y1_negative, r_x1_negative)
    y = x1

    return gcd, x, y, x_negative, x1_negative


def modular_inverse(a, m, radix, a_negative, m_negative):
    gcd, x, y, x_negative, y_negative = extended_gcd(a, m, radix, a_negative, m_negative)
    
    if is_zero(gcd):
        raise ValueError("Modular inverse does not exist.")
    
    inverse, i_negative = mod(x, m, radix, x_negative, m_negative)  # Calculate the modular inverse using your mod function
    return inverse, i_negative
