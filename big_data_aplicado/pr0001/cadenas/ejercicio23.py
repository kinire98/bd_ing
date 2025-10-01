
user_input = input("Enter the string: ")
vowels = "aAeEiIoOuU"
print("".join(["" if i in vowels else i for i in user_input]))
