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
