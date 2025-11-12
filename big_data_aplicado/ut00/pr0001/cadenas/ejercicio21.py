string = input("Enter your string: ")
substring = input("Enter the substring to find: ")

number_of_appeareances = 0

for i in range(0, len(string) - len(substring) + 1, 1):
    number_of_appeareances += 1 if string[i: i + len(substring)] == substring else 0

print(number_of_appeareances)
