number = int(input("Enter a number: "))

result = 0

while number > 10:
    result += number % 10
    number //= 10

result += number

print(result)
