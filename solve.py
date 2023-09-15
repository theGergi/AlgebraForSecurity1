##
# 2WF90 Algebra for Security -- Software Assignment 1 
# Integer and Modular Arithmetic
# solve.py
#
#
# Group number:
# group_number 
#
# Author names and student IDs:
# author_name_1 (author_student_ID_1) 
# author_name_2 (author_student_ID_2)
# author_name_3 (author_student_ID_3)
# author_name_4 (author_student_ID_4)
##

# Import built-in json library for handling input/output 
import json



def solve_exercise(exercise_location : str, answer_location : str):
    """
    solves an exercise specified in the file located at exercise_location and
    writes the answer to a file at answer_location. Note: the file at
    answer_location might not exist yet and, hence, might still need to be created.
    """
    
    # Open file at exercise_location for reading.
    with open(exercise_location, "r") as exercise_file:
        # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data 
        exercise = json.load(exercise_file)
    


    ### Parse and solve ###

    # Check type of exercise
    if exercise["type"] == "integer_arithmetic":
        # Check what operation within the integer arithmetic operations we need to solve
        if exercise["operation"] == "addition":
            # Solve integer arithmetic addition exercise
            pass
        elif exercise["operation"] == "subtraction":
            # Solve integer arithmetic subtraction exercise
            pass
        # et cetera
    else: # exercise["type"] == "modular_arithmetic"
        # Check what operation within the modular arithmetic operations we need to solve
        if exercise["operation"] == "reduction":
            # Solve modular arithmetic reduction exercise
            pass
        # et cetera


    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)
    


    

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

    return radix_notation

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
    print(x)
    print(y)
    for i in range(len(x) - 1, -1, -1):
        z[i] = x[i] + y[i] + c
        if z[i] >= radix:
            z[i] = z[i] - radix
            c = 1
        else:
            c = 0
    print(z)
    print(custom_decimal_to_radix(z, radix))

x = "6295"
y = "A825"

x = custom_radix_to_decimal(x, 16)
y = custom_radix_to_decimal(y, 16)

addition(x,y,16)



    