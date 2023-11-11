from os import path
from sys import argv as programPath

def getPath(fileName:str):
    absPath = path.dirname(programPath[0])
    return path.join(absPath, fileName)

def printResult(result): 
    print("Success" if result == True else result)
    
def printList(aList, subitem=None, end="\n"):
    if len(aList) == 0: print("None")
    elif (subitem == None):
        for item in aList: print(item, end=end)
    else:
        for item in aList: print(item[subitem], end=end)