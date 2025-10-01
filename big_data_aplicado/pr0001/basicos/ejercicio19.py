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
