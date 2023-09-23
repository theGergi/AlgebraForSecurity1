
def custom_radix_to_decimal(number_str, radix):
    
    if not 2 <= radix <= 16:
        raise ValueError("Radix must be between 2 and 16.")

    decimal_notation = []
    power = 0

    for digit in number_str:
        if '0' <= digit <= '9':
            digit_value = ord(digit) - ord('0')
        else:
            digit_value = ord(digit.upper()) - ord('A') + 10

        decimal_notation.append(digit_value)
        power += 1

    return decimal_notation


def custom_decimal_to_radix(number_arr, radix):
    if number_arr is None:
        return number_arr

    if not 2 <= radix <= 16:
        raise ValueError("Radix must be between 2 and 16.")

    radix_notation = ""
    power = 0

    for digit in number_arr:
        if 0 <= digit <= 9:
            digit_value = chr(digit + ord('0'))
        else:
            digit_value = chr(digit - 10 + ord('A'))

        radix_notation += digit_value
        power += 1

    return remove_leading_zeros(radix_notation)

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
    return z

def bigger_than(x, y):
    while(len(x) != len(y)):
        if len(x) > len(y):
            y = [0] + y
        else:
            x = [0] + x

    for i in range(len(x)):
        if y[i]>x[i]:
            return False
        if x[i]>y[i]:
            return True

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
        if x[i]>=y[i]:
            z[i] = x[i] - y[i] + c
            c = 0
        else:
            z[i] = x[i] - y[i] + c + radix
            c = -1
    print(z)
    print(custom_decimal_to_radix(z, radix))
    return z

def multiplication_primary(x, y, radix: int):
    while(len(x) != len(y)):
        if len(x) > len(y):
            y = [0] + y
        else:
            x = [0] + x
    c = 0
    x = [0] + x
    y = [0] + y
    z = [0] * (len(x) ** 2)
    # print(x)
    # print(y)
    a = 0
    for i in range(len(x) - 1, -1, -1):
        inv_i = len(x) - 1 - i
        mid_z = [0] * (len(x) ** 2)
        mid_c = 0
        for j in range(len(y) - 1, -1, -1):
            inv_j = len(y) - 1 - j
            a = [0] * (len(x) ** 2)
            a[len(a) - 1 - inv_j] = x[i] * y[j] + mid_c
            # print(x[i], y[j], a[len(a) - 1 - inv_j], mid_c)
            if a[len(a) - 1 - inv_j] >= radix:
                mid_c = a[len(a) - 1 - inv_j] // radix
                a[len(a) - 1 - inv_j] = a[len(a) - 1 - inv_j] % radix
            else:
                mid_c = 0
            # print("A ", a)
            mid_z = addition(mid_z, a, radix)
            # print("Mid z ", mid_z)
        # print("======================================")
        mid_z += [0] * inv_i
        # print(mid_z)
        z = addition(z, mid_z, radix)

    for i in range(len(z) - 1):
        if z[0] == 0:
            z = z[1:]
    print(z)
    print(custom_decimal_to_radix(z, radix))
    return z
    
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

def remove_leading_zeros(string):
    while len(string) > 1 and string[0] == '0':
        string = string[1:]
    return string

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


def is_zero(num):
    return all(digit == 0 for digit in num)

def mod(a, b):
    nr=0
    while bigger_than(a, b):
        a = subtraction(a, b, 10)
    if(is_zero(subtraction(a,b,10))):
        a = subtraction(a, b, 10)
    return a

def div(a, b):
    nr = 0
    while bigger_than(a, b):
        a = subtraction(a, b, 10)
        nr=nr+1
    if(is_zero(subtraction(a,b,10))):
        a = subtraction(a, b, 10)
        nr=nr+1
    nr=str(nr)
    nr=custom_radix_to_decimal(nr, 10)
    return nr

def gcd(a, b):
    while is_zero(b) == False:
        a, b = b, mod(a, b)
    return a



def extended_gcd(a, b):
    if is_zero(a):
        return b, [0], [1]

    gcd, x1, y1 = extended_gcd(mod(b, a), a)

    r = div(b, a)
    x = subtraction(y1, multiplication_primary(r, x1, 10), 10)
    y = x1

    return gcd, x, y


def modular_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    
    if is_zero(gcd):
        raise ValueError("Modular inverse does not exist.")
    
    inverse = mod(x, m)  # Calculate the modular inverse using your mod function
    return inverse

    
