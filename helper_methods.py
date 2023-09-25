def add_minus(x):
    """
        Add a minus in front of a string representation of a number
    """
    if x != "0":
        return "-" + x
    else:
        return x

def is_zero(num):
    """
        Return if the number is 0
    """
    return all(digit == 0 for digit in num)

def is_one(num):
    """
        Return if the number is 1
    """
    num = remove_leading_zeros_array(num)
    return len(num) == 1 and num[0] == 1

def bigger_than(x, y):
    """
        Returns True if x is bigger than y, else returns false
    """
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
    """
        Remove leading zeros from a string representation of a number
    """
    while len(string) > 1 and string[0] == '0':
        string = string[1:]
    return string

def remove_leading_zeros_array(x):
    """
        Remove leading zeros from an array representation of a number
    """
    for i in range(len(x)):
        if x[i] != 0:
            return x[i:]
    return [0]

def custom_radix_to_decimal(number_str, radix):
    """
        Convert a string representation of a number to an array representation of a number
    """
    if not 2 <= radix <= 16:
        raise ValueError("Radix must be between 2 and 16.")

    decimal_notation = []
    power = 0

    # For each value in the string convert it to a string version digit of radix
    for digit in number_str:
        if '0' <= digit <= '9':
            digit_value = ord(digit) - ord('0')
        else:
            digit_value = ord(digit.upper()) - ord('A') + 10

        decimal_notation.append(digit_value)
        power += 1

    return decimal_notation


def custom_decimal_to_radix(number_arr, radix):
    """
        Convert a array representation of a number to an string representation of a number
    """

    if number_arr is None:
        return number_arr

    if not 2 <= radix <= 16:
        raise ValueError("Radix must be between 2 and 16.")

    radix_notation = ""
    power = 0

    # For each value in the array convert it to a decimal version
    for digit in number_arr:
        if 0 <= digit <= 9:
            digit_value = chr(digit + ord('0'))
        else:
            digit_value = chr(digit - 10 + ord('A'))

        radix_notation += digit_value
        power += 1

    return remove_leading_zeros(radix_notation)
