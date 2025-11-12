dic = {
        "val1": [1, 2, 3, 4],
        "val2": [2, 3, 4, 5],
        "val3": [5, 6, 7, 8],
        "val5": [10, 11, 12, 13],
        "val6": [1234, 1234, 1234, 1234],
        }

new_dic = {}

for key, val in dic.items():
    for i in val:
        new_dic[i] = key

print(new_dic)
