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
import time
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
                output = add_minus(output)
        elif exercise["operation"] == "subtraction":
            output, negative = subtraction_with_negative(x,y,radix,x_negative, y_negative)
            output = custom_decimal_to_radix(output, radix)
            if negative:
                output = add_minus(output)
        elif exercise["operation"] == "multiplication_primary":
            output = multiplication_primary(x, y, radix)
            output = custom_decimal_to_radix(output, radix)
            if x_negative != y_negative:
                output = add_minus(output)
        elif exercise["operation"] == "multiplication_karatsuba":
            output = multiplication_karatsuba(x, y, radix)
            output = custom_decimal_to_radix(output, radix)
            if x_negative != y_negative:
                output = add_minus(output)
        elif exercise["operation"] == "extended_euclidean_algorithm":
            output = ["","",""]
            if bigger_than(x, y):
                gcd, b, a, b_negative, a_negative = extended_gcd(y, x, radix, y_negative, x_negative,0)
            else:
                gcd, a, b, a_negative, b_negative = extended_gcd(x, y, radix, y_negative, x_negative,0)

            output[0] = custom_decimal_to_radix(a, radix)
            if a_negative:
                output[0] = add_minus(output[0])
            output[1] = custom_decimal_to_radix(b, radix)
            if b_negative:
                output[1] = add_minus(output[1])
            output[2] = custom_decimal_to_radix(gcd, radix)
        # et cetera
    else: # exercise["type"] == "modular_arithmetic"
        modulo = custom_radix_to_decimal(exercise["modulus"], radix)
        if modulo[0] == 0:
            output = None
        # Check what operation within the modular arithmetic operations we need to solve
        elif exercise["operation"] == "reduction":
            # Solve modular arithmetic reduction exercise
            output = modular_reduction(x, modulo, radix)
            output = custom_decimal_to_radix(output, radix)
        elif exercise["operation"] == "addition":
            output = modular_addition(x, y, modulo, radix, x_negative, y_negative)
            output = custom_decimal_to_radix(output, radix)
        elif exercise["operation"] == "subtraction":
            output = modular_subtraction(x, y, modulo, radix, x_negative, y_negative)
            output = custom_decimal_to_radix(output, radix)
        elif exercise["operation"] == "multiplication":
            output = modular_multiplication(x,y,modulo,radix, x_negative, y_negative)
            output = custom_decimal_to_radix(output, radix)
        elif exercise["operation"] == "inversion":
            # x = modular_reduction(x, modulo, radix)
            output, output_negative = modular_inverse(x, modulo, radix, x_negative, False)
            output = custom_decimal_to_radix(output, radix)
            if output_negative:
                output = add_minus(output)
            
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

def run_tests(folder):
    success = [False] * 14
    for i in range(14):
        print(f"==================Exercise {i}====================")
        start = time.time()
        solve_exercise(f"Examples\{folder}\Exercises\exercise{i}.json", f"Testing\{folder}\\answer{i}.json")
        print(time.time() - start)
        with open(f"Examples\{folder}\Answers\\answer{i}.json", "r") as exercise_file:
            # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data 
            true_answer = json.load(exercise_file)
        with open(f"Testing\{folder}\\answer{i}.json", "r") as exercise_file:
            # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data 
            answer = json.load(exercise_file)
        if "answer" in true_answer.keys():
            # print(true_answer["answer"], "\n",answer["answer"])
            if true_answer["answer"] == answer["answer"]:
                success[i] = True
        else:
            if true_answer["answer-a"] == answer["answer-a"] and true_answer["answer-b"] == answer["answer-b"] and true_answer["answer-gcd"] == answer["answer-gcd"]:
                success[i] = True
        if all(success):
            print("ALL TESTS PASSED!")

    for i in range(len(success)):
        if not success[i]:
            print("Test " + str(i) + ": Failure")
        # else:
        #     print("Test " + str(i) + ": Success")
    




modulo = "1A"

x = "66587035715148446346874731846737087867008364220700646718283271560481083137227376177353087637571246438000788848844043451382070421132448404267540763350327263047261277412373587812752565827213141264341350587525784132132617778141377084563767181255587704670110266704281572371438721426721346002636542666222542780033173664347471165344483368515708487004336742657467470836824234701358687027723561383147242771403324856404287700510525526603266106246534507031451184573467716178048411678486004860244311600628287530503767628508475421730505"
y = "5651444666070846668348266018827322313138265145873280557014274777278384433362481865118770803017464760411330230083622882610472626545522771834518083446072541276231680755213580880284122700478248423407183137704225068141582003322843403540172154702242177813841463480866685880424820425816676100278114044080170131833244417012877634064326454304042472258787543255621208443067063086302161630425547405087482868650511381563337064542343648736868438030374684556201011674330416678010666471000823638214273211055745288401132068630856630558703"
x = custom_radix_to_decimal(x, 16)
y = custom_radix_to_decimal(y, 16)
modulo = custom_radix_to_decimal(modulo, 10)
# print(division_with_remainder(x,y, 10))
# print(modular_reduction(x,y, 10))
# print(extended_gcd(x, y, 7, False, False))
# print(multiplication_primary_with_negative(x,[0],3,True, True))
# print(modular_inverse(x, modulo, 14, False, False))
# mod(x,y,10,True,False)

# print(multiplication_karatsuba(x,y,13))
# import time

# print("subtraction")
# start0 = time.time()
# for i in range(1):
#     subtraction(x,y,12)
# print(time.time() - start0)

# print("multiplication")
# start1 = time.time()
# for i in range(1):
#     multiplication_primary(x,y,13)
# print(time.time() - start1)

# print("addition")
# start2 = time.time()
# for i in range(1):
#     addition(x,y,12)
# print(time.time() - start2)

# print("addition with negative")
# start3 = time.time()
# for i in range(1):
#     addition_with_negative(x,y,12, False, True)
# print(time.time() - start3)

# print("subtraction with negative")
# start4 = time.time()
# for i in range(1):
#     subtraction_with_negative(x,y,12, False, True)
# print(time.time() - start4)

# print(remove_leading_zeros_array([0,0]))

# print(modular_subtraction([7], [6], [4], 10, True, False))
# print(modular_addition([7], [7], [4], 10, False, True))
# print(modular_multiplication([7], [9], [4], 10, True, True))
# print(remove_leading_zeros_array([0, 0, 0, 0, 7, 2, 5, 5, 6]))
# print(multiplication_primary(x, y, 10))
# solve_exercise("Examples\Simple\Exercises\exercise0.json", "answer.json")

run_tests("Simple")
run_tests("Realistic")

# print(div(x, y, 10, False, False))
# print(extended_gcd(x,y, 7,False, False))

# # modular(subtraction())

