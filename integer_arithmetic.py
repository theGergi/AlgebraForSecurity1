from helper_methods import *

def addition(x, y, radix: int):
    """
    Returns the sum of 2 positive integers x and y.
    """
    c = 0
    #pad the smaller number with 0s to match the larger number in length
    while(len(x) != len(y)):
        if len(x) > len(y):
            y = [0] + y
        else:
            x = [0] + x
    x = [0] + x
    y = [0] + y
    z = [0] * len(x)

    # Add the 2 numbers
    for i in range(len(x) - 1, -1, -1):
        z[i] = x[i] + y[i] + c
        if z[i] >= radix:
            z[i] = z[i] - radix
            c = 1
        else:
            c = 0
    # Remove any leading zeros and return
    return remove_leading_zeros_array(z)

def addition_with_negative(x:list[int], y:list[int], radix:int, x_negative = False, y_negative = False):
    """Returns the sum of 2 positive integers x and y.

    Args:
        x_negative (bool): Is integer x a negative number
        y_negative (bool): Is integer y a negative number

    """
    # If x and y are the same sign then return the sum of their absolute values and the correct sign
    # Else return their difference with the correct sign
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
    """
    Returns the difference of 2 positive integers x and y.
    """
    c = 0

    #pad the smaller number with 0s to match the larger number in length
    while(len(x) != len(y)):
        if len(x) > len(y):
            y = [0] + y
        else:
            x = [0] + x
    z = [0] * len(x)

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
    # Remove any leading zeros and return
    return remove_leading_zeros_array(z)

def subtraction_with_negative(x:list[int], y:list[int], radix:int, x_negative = False, y_negative = False):
    """Returns the difference of 2 positive integers x and y.

    Args:
        x_negative (bool): Is integer x a negative number
        y_negative (bool): Is integer y a negative number

    """
    # If x and y have the opposite sign then return the sum of their absolute values and the correct sign
    # Else return their difference with the correct sign
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
    """
    Multiplies 2 positive numbers using the primary school method
    """

    # remove leading zeros
    x = remove_leading_zeros_array(x)
    y = remove_leading_zeros_array(y)

    # if x*y = 0 then return 0
    if is_zero(x) or is_zero(y):
        return [0]
    
    c = 0 # A carry for x * y[0:j]
    # Make z big enough to be able to store the output
    z = [0] * (max(len(x),len(y)) * 2 + 1)
    for i in range(len(x) - 1, -1, -1):
        inv_i = len(x) - 1 - i # An index which tracks x the opposite direction of i
        mid_c = 0 # A carry for x * y[j]
        for j in range(len(y) - 1, -1, -1):
            # This part keeps track of the number resulting by x * y[j]
            inv_j = len(y) - 1 - j# An index which tracks y the opposite direction of j
            mid_z = x[i] * y[j] + mid_c
            if mid_z >= radix:
                mid_c = mid_z // radix
                mid_z = mid_z % radix
            else:
                mid_c = 0

            # This part keeps track of the number resulting by x * y[0:j]
            # We use this instead of adding y[0] + y[1] +... y[len(y)] to improve calculation speed
            z[len(z) - 1 - inv_j - inv_i] = mid_z + z[len(z) - 1 - inv_j - inv_i] + c
            if z[len(z) - 1 - inv_j - inv_i] >= radix:
                c = z[len(z) - 1 - inv_j - inv_i] // radix
                z[len(z) - 1 - inv_j - inv_i] = z[len(z) - 1 - inv_j - inv_i] % radix
            else:
                c = 0
            if j == 0:
                z[len(z) - 2 - inv_j - inv_i] += mid_c + c
                c = 0
    # Remove leading zeros and return
    z = remove_leading_zeros_array(z)
    return z

def multiplication_primary_with_negative(x, y, radix, x_negative, y_negative):
    """
    Multiplies 2 numbers using the primary school method
    """
    z = multiplication_primary(x, y, radix)

    if x_negative != y_negative:
        return z, True
    else:
        return z, False
    

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
    return z



def division_with_remainder(a, b, radix):
    """
        Divides number a by number b and returns the quotient and remainder
    """
    a = remove_leading_zeros_array(a)
    b = remove_leading_zeros_array(b)
    a_bigger = bigger_than(a, b) # Finds if a is bigger, then the output qoutient is positive
    num = [0] * len(a)

    # Keep track of the current and old power of the radix that we are subtracting from a
    mult = 0
    old_mult = None

    # Keeps track of the number of times we subtracted the same power of radix times b from a
    nr = 0

    # While a is bigger than b keep subtracting
    while(bigger_than(a, b) or a == b):
        mult = len(a) - len(b)
        # Multiplies b by the radix until the we get a number that is just smaller than a
        y = b + [0] * (mult)
        if bigger_than(y, a):
            y = b + [0] * (mult - 1)
            mult -= 1
        a = remove_leading_zeros_array(subtraction(a, y, radix)) # Remainder

        # If the power of the radix we are subtracting changes then add a digit to the quotient equal to nr
        # Else increase nr
        if mult == old_mult or old_mult is None:
            nr += 1
        else:
            num[len(num) - 1 - old_mult] = nr
            nr = 1
        old_mult = mult
    
    # Add the last digit of the quotient
    num[len(num) - 1 - mult] = nr
    return num, a, not a_bigger

def extended_gcd(a, b, radix, a_negative, b_negative):
    """
        A recursive algorithm which returns the GCD of a and b
        and the coefficients x and y such that a*x + b*y = GCD(a,b) 
    """
    if is_zero(a):
        return b, [0], [1], True, b_negative
    
    # Finds the quotient and remainder of b and a
    q, rem, q_negative = division_with_remainder(b, a, radix)

    # Makes a recursive call with
    gcd, x1, y1, x1_negative, y1_negative = extended_gcd(rem, a, radix, False, a_negative)

    # Get the new x and y by subtracting the product of x and the x from the previous iteration
    # And y becomes the x from the previous iteration
    q_x1, q_x1_negative = multiplication_primary_with_negative(q, x1, radix, q_negative, x1_negative)
    x, x_negative = subtraction_with_negative(y1, q_x1, radix, y1_negative, q_x1_negative)
    y = x1

    return gcd, x, y, x_negative, x1_negative