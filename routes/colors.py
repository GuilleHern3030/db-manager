COLOR_DEFAULT = "\033[0m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_CYAN = "\033[96m"
COLOR_WHITE = "\033[97m"

def defaultColor():
    print(COLOR_DEFAULT,end="")

def printWithColor(color, content, end:str="\n", sep:str=" - "):
    end = f"{COLOR_DEFAULT} {end}"
    text = sep.join(map(str, content))
    return print(color, text, end=end, sep="")

def printRed(*content, end:str="\n", sep:str=" - "): 
    return printWithColor(COLOR_RED, content, end=end, sep=sep)

def printGreen(*content, end:str="\n", sep:str=" - "): 
    return printWithColor(COLOR_GREEN, content, end=end, sep=sep)

def printYellow(*content, end:str="\n", sep:str=" - "): 
    return printWithColor(COLOR_YELLOW, content, end=end, sep=sep)

def printBlue(*content, end:str="\n", sep:str=" - "): 
    return printWithColor(COLOR_BLUE, content, end=end, sep=sep)

def printMagenta(*content, end:str="\n", sep:str=" - "): 
    return printWithColor(COLOR_MAGENTA, content, end=end, sep=sep)

def printCyan(*content, end:str="\n", sep:str=" - "): 
    return printWithColor(COLOR_CYAN, content, end=end, sep=sep)

def printWhite(*content, end:str="\n", sep:str=" - "): 
    return printWithColor(COLOR_WHITE, content, end=end, sep=sep)