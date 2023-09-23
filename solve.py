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
from methods import *


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
            output, negative = addition_with_negative(x,y,radix,x_negative, y_negative)
            output = custom_decimal_to_radix(output, radix)
            if negative:
                output = "-" + output
        elif exercise["operation"] == "subtraction":
            output, negative = subtraction_with_negative(x,y,radix,x_negative, y_negative)
            output = custom_decimal_to_radix(output, radix)
            if negative:
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
    



x = "131"
y = "130"
modulo = "1022"

# x = "10"
# y = "20"
x = custom_radix_to_decimal(x, 16)
y = custom_radix_to_decimal(y, 16)
modulo = custom_radix_to_decimal(modulo, 16)
# modular_subtraction(x, y, modulo, 4)
# print(subtraction(x, y, 4, False, False))
# solve_exercise("Examples\Simple\Exercises\exercise0.json", "answer.json")

run_tests()


# print(extended_gcd(x,y,True, True, 10))

# # modular(subtraction())