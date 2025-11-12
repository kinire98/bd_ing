s = input("Enter the string: ")
n = int(input("Enter the frecuency: "))
char = input("Enter the character: ")

print(char.join(s[i:i+n] for i in range(0, len(s), n)))  
