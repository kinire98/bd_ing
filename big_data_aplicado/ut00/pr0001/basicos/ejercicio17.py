num1 = int(input("Enter a number: "))
num2 = int(input("Enter another number: "))

operation = input("Select an operation [+ - * /]: ")

match operation:
    case "+":
        print("Result:")
        print(num1 + num2)
    case "-":
        print("Result:")
        print(num1 - num2)
    case "*":
        print("Result:")
        print(num1 * num2)
    case "/":
        print("Result:")
        print(num1 / num2)
    case _:
        print("You didn't select a valid operation")
