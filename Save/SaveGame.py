def SaveGame(level):
    try:
        f = open("./Save/SaveData.txt", "x")
    except:
        f = open("./Save/SaveData.txt", "w")
    f.write(str(level)+"\n")
    f.close()

def LoadGame():
    f = open("./Save/SaveData.txt", "r")
    lines = f.readlines()
    f.close()
    return int(lines[0])
