words = ["i", "get", "knocked", "down", "but", "i", "get", "up", "again", "you'll", "never", "keep", "me", "down"]

first_letters = {}

for w in words:
    first_letters.setdefault(w[0], []).append(w)

print(first_letters)
