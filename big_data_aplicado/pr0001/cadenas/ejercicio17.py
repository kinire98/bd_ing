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
