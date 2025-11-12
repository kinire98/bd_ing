# Ejercicios cadenas

## Ejercicio 16
```python
user_input = input("Introduce una cadena: ")
print(max([len(i) for i in user_input.split(" ")]))
```

## Ejercicio 17
```python
# import sys


user_input = input("Enter a number: ")

# try:
#     int(user_input)
# except:
#     print("Not a number")
#     sys.exit()
#
# negative = user_input[0] == "-" 
#
# user_input = user_input[1:] if negative else user_input
#
#
# def add_points(number: str, negative: bool) -> str:
#     if len(number) < 4:
#         return ("-" if negative else "") + number
#     output = ""
#     for i in range(-1, -len(number) - 1, -1):
#         output = number[i] + output
#         if i * -1 % 3 == 0 and i != -(len(number)):
#             output = "." + output
#     return output
#
#
# print(add_points(user_input, negative))

#other solution

print(f"{int(user_input):,}".replace(",", "."))
```

## Ejercicio 18
```python
string = input("Enter your string: ")

positions = int(input(f"How many positions do you want to rotate? Max - {len(string) - 1}: "))

print(string[positions:] + string[:positions] if positions < len(string) and positions > 0 else "Invalid rotations")
```

## Ejercicio 19
```python
user_input = input("Enter your string: ")

print(" ".join(user_input.split())) # Solution 1

print(" ".join(list(filter(lambda s: s != '',user_input.split(" "))))) # Solution 2
```

## Ejercicio 20
```python
user_input = input("Enter the string: ")
vowels = "aAeEiIoOuU"
print("".join(["*" if i in vowels else i for i in user_input]))
```
## Ejercicio 21
```python
string = input("Enter your string: ")
substring = input("Enter the substring to find: ")

number_of_appeareances = 0

for i in range(0, len(string) - len(substring) + 1, 1):
    number_of_appeareances += 1 if string[i: i + len(substring)] == substring else 0

print(number_of_appeareances)
```
## Ejercicio 22
```python
user_input = input("Enter your string: ")

letters_already_seen = set([])
letters_already_removed = set([])

first_letters = []

for c in user_input:
    if c in letters_already_seen:
        if c not in letters_already_removed:
            first_letters.remove(c)
            letters_already_removed.add(c)
        continue
    letters_already_seen.add(c)
    first_letters.append(c)

print(first_letters[0] if len(first_letters) > 0 else "Every character was repeated")
```
## Ejercicio 23
```python
user_input = input("Enter the string: ")
vowels = "aAeEiIoOuU"
print("".join(["" if i in vowels else i for i in user_input]))
```
## Ejercicio 25
```python
user_input = input("Enter your string: ")

print(len([i for i in user_input if i.isupper()]))
```
## Ejercicio 26
```python
s = input("Enter the string: ")
n = int(input("Enter the frecuency: "))
char = input("Enter the character: ")

print(char.join(s[i:i+n] for i in range(0, len(s), n)))  
```
## Ejercicio 27
```python
user_input = input("Enter your string: ")

word_frecuency = dict()

most_repeated_word = ""
biggest_frecuency = 0

for w in user_input.split():
    w = w.lower()
    word_frecuency[w] = word_frecuency.get(w, 0) + 1
    if word_frecuency[w] > biggest_frecuency:
        biggest_frecuency = word_frecuency[w] 
        most_repeated_word = w
print(most_repeated_word)
```
## Ejercicio 28
```python
user_input = input("Enter your string: ")

print("".join([c for c in user_input if not c.isnumeric()]))
```
