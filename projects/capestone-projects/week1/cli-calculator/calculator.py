# A Robust CLI Calculator.

# defines add function
def add(num1, num2):
    return num1 + num2
# defines subtract function


def subtract(num1, num2):
    return num1-num2
# defines multiply function


def multiply(num1, num2):
    return num1 * num2
# defines decide function


def devide(num1, num2):
    return num1/num2


# initiates the first loop to keep displaying the menu to the user.
while True:
    print("----Menu----")
    print("----1.add----")
    print("----2.Subtract----")
    print("----3.Multiply----")
    print("----4.Devide----")
    print("----5.Exit----")
    try:  # starts a check for if the input is an integer and handles the invalid input
        option_selection = int(
            input("Please select an option 1-5. "))
        if 1 <= option_selection <= 5:  # checks for is the user has selected from the menu
            # exits the loop as soon as user selects the option without interpreting further code.
            if option_selection == 5:
                print("Exiting program. Bye!")
                break
            while True:  # initiates a loop to make sure the user provides valid number before moving forward.
                try:  # checks if the user has provided a valid input in numbers
                    # asks and converts user input into float from str
                    num1 = float(input("First Number: "))
                    while True:  # initiates a loop to make sure the user provides valid number before moving forward.
                        try:  # initiates a check if the user input is a valid float number for calculations.
                            # asks for and converts user input into float form str.
                            num2 = float(input("Second Number: "))
                            if option_selection == 1:  # if option 1 is selected, performs the add function.
                                print(f"{num1} + {num2} ={add(num1, num2)}")
                            # if the option 2 is selected, performs the subtract functions.
                            elif option_selection == 2:
                                print(
                                    f"{num1} - {num2} ={subtract(num1, num2)}")
                            elif option_selection == 3:  # if option 3 is selected, performs the multipy funtion.
                                print(
                                    f"{num1} * {num2} ={multiply(num1, num2)}")
                            elif option_selection == 4:  # if options 4 is selected, performs the devide function.
                                try:  # initiates a check to handle the devide by zero error.
                                    print(
                                        f"{num1} / {num2} ={devide(num1, num2)}")
                                except ZeroDivisionError:
                                    print("Can not devide by zero.")
                            # breaks the loop initiated for num2 value check.
                            break
                        except ValueError:  # handles the value error for num2.
                            print("Please enter a number.")
                    break  # breaks the loop initaied for num1
                except ValueError:  # handles the value error for num1.
                    print("Please enter a number.")
        else:
            print("Please select an option form the menu.")
    except ValueError:  # completes the check intiated for the option selection menu.
        print("Please enter a number.")
