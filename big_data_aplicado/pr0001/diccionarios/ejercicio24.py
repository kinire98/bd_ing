number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

number_dict = dict()

acc = 0

for i in range(len(number_list)):
    acc += number_list[i]
    number_dict[i] = acc

print(number_dict)
