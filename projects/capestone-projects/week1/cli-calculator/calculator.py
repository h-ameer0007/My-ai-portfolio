# a simple calculator made with python

import math  # imports the fuctions from math module

# defines the addition operation


def add():
    return x + y

# defines the subtraction operation


def subtract():
    return x-y

# defines the multiplication operation


def multiply():
    return x*y

# defines the devision operation


def devide():
    return x/y


# initializes the variables for operations
x = 0
y = 0

# an open loop that prints menu of selection and allows user to continue operations untill quit.
while True:
    print("----Menu----")  # prints the menu lable
    print("1.Add")        # prints the addition option
    print("2.Subtract")   # prints the subtraction option
    print("3.Multiply")   # prints the multiplication option
    print("4.Devide")     # prints the devition option
    print("5.Quit")       # prints the quit option
    print("Select an option.")  # prints the selction operation line
    option_selection = input("")  # takes the user input from the selction menu
    # checks for if the input is a numeric value and if is in menu
    if option_selection.isdigit() and (0 < int(option_selection) <= 5):
        # the input is converted into an intiger
        if int(option_selection) == 5:
            # ptints the quiting message
            print("Quiting the program... Goodbye.")
            # breaks the loop
            break
        # asks for first number
        First_number = input("First Number : ")

        if First_number.isdigit():  # checks if it is a numeric value
            # converts it into a number with decimal point
            x = float(First_number)
           # if the value provided is other then a number
        else:  # prints the error message
            print("Please provide a number.")
          # asks for second number
        Second_number = input("Second Number : ")

        if Second_number.isdigit():  # checks if it is a numeric value
            # converts it into a number with decimal point
            y = float(Second_number)
         # if the value provided is other then a number
        else:
            print("Please provide a number.")  # prints the error message
        # checks if the additoin option is selected
        if int(option_selection) == 1:
            # calls the addtion function and prints the result
            print(f" >> {x} + {y} =", add(), "<<")
        if int(option_selection) == 2:
            # calls the subtraction function and prints the result
            print(f" >> {x} - {y} =", subtract(), "<<")
        if int(option_selection) == 3:
            # calls the multiplication function and prints the result
            print(f" >> {x} * {y} =", multiply(), "<<")

        if int(option_selection) == 4:
            # checks if the second number for divition is 0.
            if int(y) == 0:
                # if the number is devided by 0 the print the error message.
                print("Can not devide by zero.")
                continue
            else:
                # if not zero then calls the devision funtion and prints the result.
                print(f" >> {x} / {y} =", devide(), "<<")
    # if the provided input is not a numeric value then it prints the error message and keeps the loop running.
    else:
        print("Please select a number from the options.")
