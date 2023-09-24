from helper_methods import *
from integer_arithmetic import *
from modular_arithmetic import *

def multiplication_karatsuba (x,y,radix:int):
    # Check if the length of x is greater than y, if so, swap them
    if len(x) > len(y):
        x, y = y, x 
    
    n1 = len(x)
    n2 = len(y) 
    
    # Pad x with zeros to match the length of y
    
    x = [0]*(n2-n1) + x
    
    # Make n1 and n2 equal to the maximum of their original values
    
    n1,n2 = max(n1,n2),max(n1,n2)
    
    # If n1 is 1, perform primary multiplication and return the result
    if (n1 == 1): 
        ans = multiplication_primary(x,y,radix)
        return ans
        
    # If n1 is odd, adjust the lengths and pad with zeros
    if (n1 % 2 == 1):
        n1 += 1
        n2 += 1
        x = [0] + x
        y = [0] + y

    xl = []
    xr = []
    yl = []
    yr = []
    
    # Split x and y into left and right halves
    
    xl = x[:n1//2]
    xr = x[n1//2:]
    yl = y[:n2//2]
    yr = y[n2//2:]

    # Perform Karatsuba multiplication recursively
    p = []
    p = multiplication_karatsuba(xl, yl, radix)

    q = []
    q = multiplication_karatsuba(xr, yr, radix)

    r = []

    # Calculate the addition of the left and right halves of x and store it in t1
    addition_of_xl_and_xr = addition(xl,xr,radix)
    t1 = addition_of_xl_and_xr 
    t1 = remove_leading_zeros(t1)
    
    # Calculate the addition of the left and right halves of y and store it in t2
    addition_of_yl_and_yr = addition(yl,yr,radix)
    t2 = addition_of_yl_and_yr 
    t2 = remove_leading_zeros(t2)

    # Perform Karatsuba multiplication recursively on t1 and t2 and store the result in t3
    kar_of_sum = multiplication_karatsuba(t1,t2,radix)
    t3 = kar_of_sum

    # Calculate the addition of the partial results p and q and store it in t4
    addition_of_p_and_q = addition(p,q,radix)
    t4 = addition_of_p_and_q

    # Perform subtraction of t4 from t3 to calculate the final result and store it in r
    r = subtraction(t3 , t4 , radix)

    # Pad the lists p and r with zeros to match the expected result length
    p = p + [0]*n1
    r = r + [0]*(n1//2)

    z = [] 
    # Calculate the final result by adding p, q, and r
    z = addition(p, addition(q, r,radix),radix)

    z = remove_leading_zeros(z)
    
    # Convert the result to the desired radix
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
    
    if not is_one(gcd):
        raise ValueError("Modular inverse does not exist.")
    inverse, i_negative = mod(x, m, radix, x_negative, m_negative)  # Calculate the modular inverse using your mod function
    if x_negative:
        inverse = addition_with_negative(inverse, m, radix,i_negative,m_negative)  # Add m to make x positive
    return inverse, i_negative
