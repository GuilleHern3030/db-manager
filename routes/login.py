from . import clear, getInput
from manager.methods import connect

def log(data):
    if data.autoConnect == False:
        clear()
        print("  SQL MANAGER  ")
        print("------------------------")
        data.printDataBase()
        print()
        print("What do you want to do?")
        print(" 0. Close")
        print(" 1. Start")
        print(" 2. Set DataBase type")
        print(" 3. Set Host")
        print(" 4. Set DataBase")
        print(" 5. Set Port")
        print(" 6. Set User")
        print(" 7. Set Password")
        print("------------------------")
        print("\nWrite the number of your instruction:")

    # Si todos los parámetros fueron pasados por consola, se inicia automáticamente
    action = getInput(7) if data.autoConnect == False else 1

    if action == 0: return None
    elif action == 2: data.sqlType = input("DATABASE type (mysql, postgre): ")
    elif action == 3: data.host = input("HOST: ")
    elif action == 4: data.dbname = input("DATABASE: ")
    elif action == 5: data.port = input("PORT: ")
    elif action == 6: data.user = input("USER: ")
    elif action == 7: data.password = input("PASSWORD: ")
    elif action == 1: 
        sql = connect(data)
        if sql.isConnected():
            return sql
    
    if data.autoConnect == False: input("\nPress ENTER to continue...\n")
    data.autoConnect = False

    return log(data)