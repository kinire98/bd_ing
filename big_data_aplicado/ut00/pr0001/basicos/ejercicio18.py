temperature = int(input("Input your temperature: "))

origin = input("Origin unit [K/C/F]: ")

match origin:
    case "K":
        destination = input("Destination unit [C/F]:")
        match destination:
            case "C":
                print(str(temperature - 273.15) + "C")
            case "F":
                print(str((temperature - 273.15) * (9/5) + 32) + "F")
            case _:
                print("ERROR: You didn't select a valid unit")
    case "C":
        destination = input("Destination unit [K/F]:")
        match destination:
            case "K":
                print(str(temperature + 273.15) + "K")
            case "F":
                print(str(temperature * (9/5) + 32) + "F")
            case _:
                print("ERROR: You didn't select a valid unit")
    case "F":
        destination = input("Destination unit [C/K]:")
        match destination:
            case "C":
                print(str((temperature - 32) / (9/5)) + "C")
            case "K":
                print(str((temperature - 32 + 273.15) / (9/5)) + "C")
            case _:
                print("ERROR: You didn't select a valid unit")
    case _:
        print("ERROR: You didn't select a valid unit")
