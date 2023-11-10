from os import path
from sys import argv as programPath

def getPath(fileName:str):
    absPath = path.dirname(programPath[0])
    return path.join(absPath, fileName)