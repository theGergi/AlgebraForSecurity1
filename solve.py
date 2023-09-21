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

    output = ""
    radix = int(exercise["radix"])

    # print(exercise["x"])
    x_negative = False if exercise["x"][0] != "-" else True
    if x_negative:
        exercise["x"] = exercise["x"][1:]
    x = custom_radix_to_decimal(exercise["x"], radix)
    # print(exercise["x"], x_negative)

    if "y" in exercise.keys():
        # print(exercise["y"])
        y_negative = False if exercise["y"][0] != "-" else True
        if y_negative:
            exercise["y"] = exercise["y"][1:]
        y = custom_radix_to_decimal(exercise["y"], radix)
        # print(exercise["y"], y_negative)

    ### Parse and solve ###
    # Check type of exercise
    if exercise["type"] == "integer_arithmetic":
        # Check what operation within the integer arithmetic operations we need to solve
        if exercise["operation"] == "addition":
            # Solve integer arithmetic addition exercise
            if x_negative and y_negative:
                output = addition(x, y, radix)
                output = custom_decimal_to_radix(output, radix)
                output = "-" + output
            elif x_negative and not y_negative:
                if bigger_than(x, y):
                    output = subtraction(x, y, radix)
                    output = custom_decimal_to_radix(output, radix)
                    output = "-" + output
                else:
                    output = subtraction(y, x, radix)
                    output = custom_decimal_to_radix(output, radix)
            elif not x_negative and y_negative:
                if bigger_than(x, y):
                    output = subtraction(x, y, radix)
                    output = custom_decimal_to_radix(output, radix)
                else:
                    output = subtraction(y, x, radix)
                    output = custom_decimal_to_radix(output, radix)
                    output = "-" + output
            else:
                output = addition(x, y, radix)
                output = custom_decimal_to_radix(output, radix)
        elif exercise["operation"] == "subtraction":
            if not x_negative and y_negative:
                output = addition(x, y, radix)
                output = custom_decimal_to_radix(output, radix)
            elif x_negative and not y_negative:
                output = addition(x, y, radix)
                output = custom_decimal_to_radix(output, radix)
                output = "-" + output
            elif x_negative and y_negative:
                if bigger_than(x, y):
                    output = subtraction(x, y, radix)
                    output = custom_decimal_to_radix(output, radix)
                    output = "-" + output
                else:
                    output = subtraction(y, x, radix)
                    output = custom_decimal_to_radix(output, radix)
            else:
                if bigger_than(x, y):
                    output = subtraction(x, y, radix)
                    output = custom_decimal_to_radix(output, radix)
                else:
                    output = subtraction(y, x, radix)
                    output = custom_decimal_to_radix(output, radix)
                    output = "-" + output
        elif exercise["operation"] == "multiplication_primary":
            output = multiplication_primary(x, y, radix)
            output = custom_decimal_to_radix(output, radix)
            if x_negative != y_negative:
                output = "-" + output
        elif exercise["operation"] == "extended_euclidean_algorithm":
            output = ["","",""]
        # et cetera
    else: # exercise["type"] == "modular_arithmetic"
        modulo = custom_radix_to_decimal(exercise["modulus"], radix)
        if modulo[0] == 0:
            output = None
        # Check what operation within the modular arithmetic operations we need to solve
        elif exercise["operation"] == "reduction":
            # Solve modular arithmetic reduction exercise
            output = modular_reduction_array(x, modulo, radix)
            output = custom_decimal_to_radix(output, radix)
        elif exercise["operation"] == "addition":
            x = modular_reduction_array(x, modulo, radix)
            y = modular_reduction_array(y, modulo, radix)
            if x_negative and y_negative:
                output = modular_addition(x, y, modulo, radix)
                output = custom_decimal_to_radix(output, radix)
                output = "-" + output
            elif x_negative and not y_negative:
                if bigger_than(x, y):
                    output = modular_subtraction(x, y, modulo, radix)
                    output = custom_decimal_to_radix(output, radix)
                    output = "-" + output
                else:
                    output = modular_subtraction(y, x, modulo, radix)
                    output = custom_decimal_to_radix(output, radix)
            elif not x_negative and y_negative:
                if bigger_than(x, y):
                    output = modular_subtraction(x, y, modulo, radix)
                    output = custom_decimal_to_radix(output, radix)
                else:
                    output = modular_subtraction(y, x, modulo, radix)
                    output = custom_decimal_to_radix(output, radix)
                    output = "-" + output
            else:
                output = modular_addition(x, y, modulo, radix)
                output = custom_decimal_to_radix(output, radix)
        elif exercise["operation"] == "subtraction":
            x = modular_reduction_array(x, modulo, radix)
            y = modular_reduction_array(y, modulo, radix)
            if not x_negative and y_negative:
                output = modular_addition(x, y, modulo, radix)
                output = custom_decimal_to_radix(output, radix)
            elif x_negative and not y_negative:
                output = modular_addition(x, y, modulo, radix)
                output = custom_decimal_to_radix(output, radix)
                output = "-" + output
            elif x_negative and y_negative:
                if bigger_than(x, y):
                    output = modular_subtraction(x, y, modulo, radix)
                    output = custom_decimal_to_radix(output, radix)
                    output = "-" + output
                else:
                    output = modular_subtraction(y, x, modulo, radix)
                    output = custom_decimal_to_radix(output, radix)
            else:
                if bigger_than(x, y):
                    output = modular_subtraction(x, y, modulo, radix)
                    output = custom_decimal_to_radix(output, radix)
                else:
                    output = modular_subtraction(y, x, modulo, radix)
                    output = custom_decimal_to_radix(output, radix)
                    output = "-" + output
        # et cetera
    if exercise["operation"] != "extended_euclidean_algorithm":
        if output is None:
            answer = {"answer": output}
        else:
            answer = {"answer": str(output)}
    else:
        answer = {"answer-a": str(output[0]), "answer-b": str(output[1]), "answer-gcd":str(output[2])}

    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)
        

def run_tests():
    success = [False] * 14
    for i in range(14):
        print(f"==================Exercise {i}====================")
        solve_exercise(f"Examples\Simple\Exercises\exercise{i}.json", f"Testing\\answer{i}.json")
        with open(f"Examples\Simple\Answers\\answer{i}.json", "r") as exercise_file:
            # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data 
            true_answer = json.load(exercise_file)
        with open(f"Testing\\answer{i}.json", "r") as exercise_file:
            # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data 
            answer = json.load(exercise_file)
        if "answer" in true_answer.keys():
            print(true_answer["answer"], answer["answer"])
            if true_answer["answer"] == answer["answer"]:
                success[i] = True

    for i in range(len(success)):
        if not success[i]:
            print("Test " + str(i) + ": Failure")
        # else:
        #     print("Test " + str(i) + ": Success")
    

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

    return removeLeadingZeros(radix_notation)

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
    
def removeLeadingZeros(s):
    # Find the index of the first non-zero character
    i = 0
    while i < len(s) and s[i] == '0':
        i += 1

    # Slice the string to remove leading zeros
    return s[i:]

def karatsuba(x, y, radix):

    x=custom_radix_to_decimal(x,radix)
    y=custom_radix_to_decimal(x,radix)

    if len(x) > len(y):
        x, y = y, x
    n1 = len(x)
    n2 = len(y)
    while n2 > n1:
        x = "0" + x
        n1 += 1
    if n1 == 1:
        ans = int(x) * int(y)
        return str(ans)
    if n1 % 2 == 1:
        n1 += 1
        x = "0" + x
        y = "0" + y
    xl = ""
    xr = ""
    yl = ""
    yr = ""
    for i in range(n1 // 2):
        xl += x[i]
        yl += y[i]
        xr += x[n1 // 2 + i]
        yr += y[n1 // 2 + i]
    p = karatsuba(xl, yl)
    q = karatsuba(xr, yr)
    r = subtraction(
        karatsuba(addition(xl, xr),
                 addition(yl, yr)),
        addition(p, q))
    for i in range(n1):
        p = p + "0"
    for i in range(n1 // 2):
        r = r + "0"
    ans = addition(p, addition(q, r))
    ans = removeLeadingZeros(ans)
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
    while bigger_than(a, b):
        a = subtraction(a, b,10)
    return a

def gcd(a, b):
    while not is_zero(b):
        a, b = b, mod(a, b)
    return a

def extended_gcd(a, b):
    x0, x1, y0, y1 = [1], [0], [0], [1]

    while len(b) > 0:
        quotient, a, b = mod(a, b)  # Perform division and get quotient

        x0, x1 = x1, subtraction(x0, multiplication_primary(x1, quotient,10))
        y0, y1 = y1, subtraction(y0, multiplication_primary(y1, quotient,10))

    return a, x0, y0


def modular_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    
    if not is_zero(gcd) and gcd[-1] == 1:
        if len(x) > 1:
            raise ValueError("Modular inverse does not exist.")
        else:
            inverse = x[0] % m[-1]
            return inverse
    else:
        raise ValueError("Modular inverse does not exist.")

x = "312"
y = "1023"
modulo = "1022"
x = custom_radix_to_decimal(x, 4)
y = custom_radix_to_decimal(y, 4)
modulo = custom_radix_to_decimal(modulo, 4)
# modular_subtraction(x, y, modulo, 4)

# solve_exercise("Examples\Simple\Exercises\exercise0.json", "answer.json")

run_tests()

# # subtraction(x,y,10)
# # modular_reduction_array(x, 10, modulo)
# # multiplication(x,y,2)
# "radix": 4,
#     "x": "312",
#     "y": "1023",
#     "modulus": "1022",

# # modular(subtraction())
    
