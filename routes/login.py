from . import clear, getInput
from .colors import *
from manager.methods import connect
from localdata.saver import saveInLocalData

def log(data):
    if data.autoConnect == False:
        clear()
        printRed("               SQL MANAGER  ")
        printBlue("------------------------------------------------")
        data.printDataBase()
        print()
        printYellow(" What do you want to do?")
        print(f"  0.{COLOR_RED} Close {COLOR_DEFAULT}")
        print(f"  1.{COLOR_GREEN} Start {COLOR_DEFAULT}")
        print(f"  2.{COLOR_BLUE} Set DataBase type {COLOR_DEFAULT}")
        print(f"  3.{COLOR_CYAN} Set Host {COLOR_DEFAULT}")
        print(f"  4.{COLOR_CYAN} Set DataBase {COLOR_DEFAULT}")
        print(f"  5.{COLOR_CYAN} Set Port {COLOR_DEFAULT}")
        print(f"  6.{COLOR_CYAN} Set User {COLOR_DEFAULT}")
        print(f"  7.{COLOR_CYAN} Set Password {COLOR_DEFAULT}")
        printBlue("------------------------------------------------")
        printYellow("\n Write the number of your instruction:")

    # Si todos los parámetros fueron pasados por consola, se inicia automáticamente
    action = getInput(7) if data.autoConnect == False else 1

    if action == 0: return None
    elif action == 2: data.sqlType = input("DATABASE type (mysql, postgre, sqlite): ")
    elif action == 3: data.host = input("HOST: ")
    elif action == 4: data.dbname = input("DATABASE: ")
    elif action == 5: data.port = input("PORT: ")
    elif action == 6: data.user = input("USER: ")
    elif action == 7: data.password = input("PASSWORD: ")
    elif action == 1:
        print(f" \n Connecting...\n ")
        sql = connect(data)
        if sql.isConnected():
            saveInLocalData(data)
            return sql
    
    if data.autoConnect == False: input("\n Press ENTER to continue...\n")
    data.autoConnect = False

    return log(data)