number_list = [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]

number_dict = dict()

for i in range(len(number_list)):
    number_dict.setdefault(number_list[i], []).append(i)
print(number_dict)
