user_input = input("Enter your string: ")

print("".join([c for c in user_input if not c.isnumeric()]))
