string = input("Enter your string: ")

positions = int(input(f"How many positions do you want to rotate? Max - {len(string) - 1}: "))

print(string[positions:] + string[:positions] if positions < len(string) and positions > 0 else "Invalid rotations")
