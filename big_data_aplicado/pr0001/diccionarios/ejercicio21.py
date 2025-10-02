dic = {"ab": 1, "aB": 2, "Ab": 3, "AB": 4}


def invert(string: str) -> str:
    stri = ""
    for c in string:
        if c.islower():
            stri += c.upper()
        else:
            stri += c.lower()
    return stri

print({invert(key): value for (key, value) in dic.items()})
