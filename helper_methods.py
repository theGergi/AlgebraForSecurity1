def add_minus(x):
    if x != "0":
        return "-" + x
    else:
        return x

def is_zero(num):
    return all(digit == 0 for digit in num)
def is_one(num):
    return num[-1] == 1
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

def remove_leading_zeros(string):
    while len(string) > 1 and string[0] == '0':
        string = string[1:]
    return string

def remove_leading_zeros_array(x):
    for i in range(len(x)):
        if x[i] != 0:
            return x[i:]
            

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
