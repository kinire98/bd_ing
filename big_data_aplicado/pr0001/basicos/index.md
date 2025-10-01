# Ejercicios basicos
## Ejercicio 16

```python
number = int(input("Enter a number: "))

result = 0

while number > 10:
    result += number % 10
    number //= 10

result += number

print(result)
```

## Ejercicio 17

```python
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

```

## Ejercicio 18
```python
temperature = int(input("Input your temperature: "))

origin = input("Origin unit [K/C/F]: ")

match origin:
    case "K":
        destination = input("Destination unit [C/F]:")
        match destination:
            case "C":
                print(str(temperature - 273.15) + "C")
            case "F":
                print(str((temperature - 273.15) * (9/5) + 32) + "F")
            case _:
                print("ERROR: You didn't select a valid unit")
    case "C":
        destination = input("Destination unit [K/F]:")
        match destination:
            case "K":
                print(str(temperature + 273.15) + "K")
            case "F":
                print(str(temperature * (9/5) + 32) + "F")
            case _:
                print("ERROR: You didn't select a valid unit")
    case "F":
        destination = input("Destination unit [C/K]:")
        match destination:
            case "C":
                print(str((temperature - 32) / (9/5)) + "C")
            case "K":
                print(str((temperature - 32 + 273.15) / (9/5)) + "C")
            case _:
                print("ERROR: You didn't select a valid unit")
    case _:
        print("ERROR: You didn't select a valid unit")
```

## Ejercicio 19

```python
import sys
import random
length = int(input("Input the lenght or your password [min 4]: "))

if length < 4:
    print("Password must have at least four characters")
    sys.exit()    

lowercase = False
uppercase = False
symbol = False 
number = False

lowercase_char = "lakskdjfhgmznxbcvqpwoeiruty"
uppercase_char = "FDASLKJHGMZNXBVCQWIEURYTPHO"
number_char = "0469587123"
symbols_char = ")(*&^%$#@!-_=+[{}]\\|;:'\",<.>/?`~"

characters = lowercase_char + uppercase_char + number_char + symbols_char

password = ""

for i in range(length):
    if length - i - 1 <= 4:
        if lowercase == False:
            index = int(random.random() * len(lowercase_char) - 1)
            password += lowercase_char[index]
            lowercase = True
            continue
        if uppercase == False:
            index = int(random.random() * len(uppercase_char) - 1)
            password += uppercase_char[index]
            uppercase = True
            continue
        if number == False:
            index = int(random.random() * len(number_char) - 1)
            password += number_char[index]
            number = True
            continue
        if symbol == False:
            index = int(random.random() * len(symbols_char) - 1)
            password += symbols_char[index]
            symbol = True
            continue
    index = int(random.random() * len(characters) - 1)
    password += characters[index]
    if characters[index] in lowercase_char:
        lowercase = True
    elif characters[index] in uppercase_char:
        uppercase = True
    elif characters[index] in number_char:
        number = True
    else:
        symbol = True


print(password)
```

## Ejercicio 20

```python 
import random 
from typing import List

random_list = [random.randint(0, 150) for _ in range(300)]

print("=============================================RANDOM=============================================")
print(random_list)
print("================================================================================================")

def quick_sort(sort_list: List[int])-> List[int]:
    if len(sort_list) == 1:
        return sort_list
    if len(sort_list) == 0:
        return sort_list
    pivot = sort_list[-1]
    del sort_list[-1]
    left = []
    right = []
    for el in sort_list:
        if el >= pivot:
            right.append(el)
        else:
            left.append(el)

    return quick_sort(left) + [pivot] + quick_sort(right)

print()
print()
print()
print()
print()
print()
print("=============================================SORTED=============================================")
print(quick_sort(random_list))
print("================================================================================================")
```
