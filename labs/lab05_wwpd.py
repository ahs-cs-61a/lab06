# lab05 WWPD?


# IMPORTS

import inspect
import tests.wwpd_storage as s

st = s.wwpd_storage 


# COLORED PRINTS - custom text type to terminal: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal, ANSI colors: http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html

class bcolors:
    HIGH_MAGENTA = '\u001b[45m'
    HIGH_GREEN = '\u001b[42m'
    HIGH_YELLOW = '\u001b[43;1m'
    MAGENTA = ' \u001b[35m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33;1m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\u001b[0m'
    
def print_error(message):
    print("\n" + bcolors.HIGH_YELLOW + bcolors.BOLD + "ERROR:" + bcolors.RESET + bcolors.YELLOW + bcolors.BOLD + " " + message + bcolors.ENDC)

def print_message(message):
    print("\n" + bcolors.HIGH_MAGENTA + bcolors.BOLD + "MESSAGE:" + bcolors.RESET + bcolors.MAGENTA + bcolors.BOLD + " " + message + bcolors.ENDC)

def print_success(message):
    print("\n" + bcolors.HIGH_GREEN + bcolors.BOLD + "SUCCESS:" + bcolors.RESET + bcolors.GREEN + bcolors.BOLD + " " + message + bcolors.ENDC)


# INCORRECT ANSWER LOOP, INSTRUCTIONS, COMPLETE, OPTIONS

def repeat():
    print("Try again:")
    return input()

def intro(name):
    print("\nWhat Would Python Display?: " + name)
    print("Type the expected output, 'function' if you think the answer is a function object, 'infinite loop' if it loops forever, 'nothing' if nothing is displayed, or 'error' if it errors; use single quotes '' when needed.\n")

def complete():
    print_success("All questions for this question set complete.")

def options():
    print_message("All questions for this question set complete. Restart question set?")
    guess = input("Y/N?\n")
    guess = guess.lower()
    while guess != "y" and guess != "n":
        print_error("Unknown input, please try again.")
        guess = input()
    if guess == "y":
        return "restart"
    return False


# WWPD? ALGORITHM 

def wwpd(name, question_set, stored_list):

    intro(name)

    matched = str([i[:-1] for i in question_set])[1:-1] in str([i[:-1] for i in stored_list])
    restart = matched and options() == "restart"
    done = False

    for q in question_set:
        q[4] = True
        if q not in stored_list or restart:
            done = True 
            if q[1]:
                print(q[1])
            if q[2]:
                print(q[2])
            guess = input()
            while guess != q[3]:
                guess = repeat()
            if not matched:
                op = open("tests/wwpd_storage.py", "w")
                for j in range(len(stored_list)):
                    if q[0] < stored_list[j][0]:
                        stored_list.insert(j, q)
                        break
                if q not in stored_list: 
                    stored_list.append(q)
                op.write("wwpd_storage = " + str(stored_list))
                op.close()
    if done:
        complete()


# REFERENCE FUNCTIONS, CLASSES, METHODS, SEQUENCES, ETC.

# https://inst.eecs.berkeley.edu/~cs61a/su22/disc/disc05/

class Student:

    extension_days = 3 # this is a class variable

    def __init__(self, name, staff):
        self.name = name # this is an instance variable
        self.understanding = 0
        staff.add_student(self)
        print("Added", self.name)

    def visit_office_hours(self, staff):
        staff.assist(self)
        print("Thanks, " + staff.name)

class Professor:

    def __init__(self, name):
        self.name = name
        self.students = {}

    def add_student(self, student):
        self.students[student.name] = student

    def assist(self, student):
        student.understanding += 1

    def grant_more_extension_days(self, student, days):
        student.extension_days = days


# https://inst.eecs.berkeley.edu/~cs61a/su22/lab/lab04/

class Car:
    num_wheels = 4
    gas = 30
    headlights = 2
    size = 'Tiny'

    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.color = 'No color yet. You need to paint me.'
        self.wheels = Car.num_wheels
        self.gas = Car.gas

    def paint(self, color):
        self.color = color
        return self.make + ' ' + self.model + ' is now ' + color

    def drive(self):
        if self.wheels < Car.num_wheels or self.gas <= 0:
            return 'Cannot drive!'
        self.gas -= 10
        return self.make + ' ' + self.model + ' goes vroom!'

    def pop_tire(self):
        if self.wheels > 0:
            self.wheels -= 1

    def fill_gas(self):
        self.gas += 20
        return 'Gas level: ' + str(self.gas)


# QUESTION SET - ELEMENT FORMAT: [<QUESTION NUMBER>, <INITIAL PRINTS> (usually empty), <QUESTION>, <ANSWER>]
# INSPECT MODULE - convert function/class body into String: https://docs.python.org/3/library/inspect.html 

student_oop_qs = [
    [1, inspect.getsource(Student) + "\n" + inspect.getsource(Professor) + '\n>>> callahan = Professor("Callahan")', '>>> elle = Student("Elle", callahan)', "Added Elle"],
    [2, "", ">>> elle.visit_office_hours(callahan)", "Thanks, Callahan"],
    [3, "", '>>> elle.visit_office_hours(Professor("Paulette"))', "Thanks, Paulette"],
    [4, "", ">>> elle.understanding", "2"],
    [5, "", ">>> [name for name in callahan.students]", "['Elle']"],
    [6, "", 'x = Student("Vivian", Professor("Stromwell")).name', "Added Vivian"],
    [7, "", ">>> x", "'Vivian'"],
    [8, "", ">>> elle.extension_days", "3"],
    [9, ">>> callahan.grant_more_extension_days(elle, 7)", ">>> elle.extension_days", "7"],
    [10, "", ">>> Student.extension_days", "3"]
    ]

classy_cars_qs = [
    [11, "\n" + inspect.getsource(Car) + "\n>>> deneros_car = Car('Tesla', 'Model S')", ">>> deneros_car.model", "'Model S'"],
    [12, ">>> deneros_car.gas = 10", ">>> deneros_car.drive()", "'Tesla Model S goes vroom!'"],
    [13, "", ">>> deneros_car.drive()", "'Cannot drive!'"],
    [14, "", ">>> deneros_car.fill_gas()", "'Gas level: 20'"],
    [15, "", ">>> Car.gas", "30"],
    [16, ">>> deneros_car = Car('Tesla', 'Model S')\n>>> deneros_car.wheels = 2", ">>> deneros_car.wheels", "2"],
    [17, "", ">>> Car.num_wheels", "4"],
    [18, "", ">>> deneros_car.drive()", "'Cannot drive!'"],
    [19, "", ">>> Car.drive()", "error"],
    [20, "", ">>> Car.drive(deneros_car)", "'Cannot drive!'"]
]

all_qs = [student_oop_qs, classy_cars_qs]

for set in all_qs:
    for q in set:
        q.append(False)


# WWPD? QUESTIONS

def wwpd_student_oop():
    wwpd("Student OOP", student_oop_qs, st)

def wwpd_classy_cars():
    wwpd("Classy Cars", classy_cars_qs, st)
