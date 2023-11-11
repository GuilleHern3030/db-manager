from os import system as osExecute, name as osName
from manager.data import Data

data = Data()

def clear(): osExecute('cls' if osName == 'nt' else 'clear')

def getInput(max:int, min:int=0, tryies:int=3) -> int:
    action = input("  -> ")
    if (action.isdigit() and int(action) >= min and int(action) <= max): 
        return int(action)
    else:
        print(f" You must write a number from {min} to {max}.")
        return getInput(max, min, tryies - 1) if tryies > 0 else 0
    