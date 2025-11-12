

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

