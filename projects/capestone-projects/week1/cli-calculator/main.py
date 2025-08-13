# working logic and script for the calculator tool
from math_ops import add, subtract, multiply, devide, square_root

# initiates the first loop to keep displaying the menu to the user.
while True:
    print("----Menu----")
    print("1.add")
    print("2.Subtract")
    print("3.Multiply")
    print("4.Devide")
    print("5.Square_root")
    print("6.Exit")
    try:  # starts a check for if the input is an integer and handles the invalid input
        option_selection = int(
            input("\nPlease select an option 1-6. \n"))
        if 1 <= option_selection <= 6:  # checks for is the user has selected from the menu
            # exits the loop as soon as user selects the option without interpreting further code.
            if option_selection == 6:
                print("\nExiting program. Bye!\n")
                break
            elif option_selection == 5:
                try:
                    root_num = float(input("\nNumber for square root: "))
                    print(
                        f"\nSquare root of {root_num} = {square_root(root_num)}\n")
                except ValueError:
                    print(
                        f"Invalid input entered for square root. Please enter a number.")
            # initiates a loop to make sure the user provides valid number before moving forward.
            while not option_selection == 5:
                try:  # checks if the user has provided a valid input in numbers
                    # asks and converts user input into float from str
                    num1 = float(input("\nFirst Number: "))
                    while True:  # initiates a loop to make sure the user provides valid number before moving forward.
                        try:  # initiates a check if the user input is a valid float number for calculations.
                            # asks for and converts user input into float form str.
                            num2 = float(input("\nSecond Number: "))
                            if option_selection == 1:  # if option 1 is selected, performs the add function.
                                print(
                                    f"\n{num1} + {num2} = {add(num1, num2)}\n")
                            # if the option 2 is selected, performs the subtract functions.
                            elif option_selection == 2:
                                print(
                                    f"\n{num1} - {num2} = {subtract(num1, num2)}\n")
                            elif option_selection == 3:  # if option 3 is selected, performs the multipy funtion.
                                print(
                                    f"\n{num1} * {num2} = {multiply(num1, num2)}\n")
                            elif option_selection == 4:  # if options 4 is selected, performs the devide function.
                                try:  # initiates a check to handle the devide by zero error.
                                    print(
                                        f"\n{num1} / {num2} = {devide(num1, num2)}\n")
                                except ZeroDivisionError:
                                    print("\nCan not devide by zero.\n")
                            # breaks the loop initiated for num2 value check.
                            break
                        except ValueError:  # handles the value error for num2.
                            print("\nPlease enter a number.\n")
                    break  # breaks the loop initaied for num1
                except ValueError:  # handles the value error for num1.
                    print("\nPlease enter a number.\n")
        else:
            print("\nPlease select an option form the menu.\n")
    except ValueError:  # completes the check intiated for the option selection menu.
        print("\nPlease enter a number.\n")
