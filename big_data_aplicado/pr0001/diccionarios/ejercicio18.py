odd = "odd"
even = "even"


dic = {
        odd: [],
        even: [],
        }

for i in range(1, 21, 1):
    if i & 1 == 0:
        dic[even].append(i)
    else:
        dic[odd].append(i)

print(dic)
