def calculator():
    print("Simple Calculator (+, -, *, /)")
    try:
        a = float(input("Enter first number: "))
        op = input("Enter operator (+, -, *, /): ").strip()
        b = float(input("Enter second number: "))

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                print("Error: Division by zero is not allowed.")
                return
            result = a / b
        else:
            print("Invalid operator.")
            return

        print(f"Result: {result}")
    except ValueError:
        print("Invalid input. Please enter numbers only.")


if __name__ == "__main__":
    calculator()
