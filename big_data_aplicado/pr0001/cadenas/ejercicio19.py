user_input = input("Enter your string: ")

print(" ".join(user_input.split()))

print(" ".join(list(filter(lambda s: s != '',user_input.split(" ")))))
