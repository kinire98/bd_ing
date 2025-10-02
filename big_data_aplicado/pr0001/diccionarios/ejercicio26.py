tuples_list = [("a", 1), ("b", 2), ("a", 1), ("a", 2)]

tuples_dict = dict()

for el in tuples_list:
    tuples_dict[el] = tuples_dict.get(el, 0) + 1
print(tuples_dict)
