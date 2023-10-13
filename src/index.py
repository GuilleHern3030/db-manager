from sql.manager import SQL
from os import system as osExecute, name as osName
from sys import argv as consoleParam
import csv.converter as csv

host = consoleParam[1] if len(consoleParam) > 1 else "localhost"
dbname = consoleParam[2] if len(consoleParam) > 2 else "test"
port = consoleParam[3] if len(consoleParam) > 3 else "3306"
user = consoleParam[4] if len(consoleParam) > 4 else "root"
password = consoleParam[5] if len(consoleParam) > 5 else ""
sqlType = consoleParam[6] if len(consoleParam) > 6 else "mysql"
table = None

def clear(): osExecute('cls' if osName == 'nt' else 'clear')

def printDataBase():
    print("Host:", host)
    print("DataBase:", dbname)
    print("Port:", port)
    print("User:", user)
    print("Password:", password)
    print("DBType:", sqlType)
    if table != None: print("Table:", table)

def getInput(max:int, min:int=0, tryies:int=3) -> int:
    action = input(" -> ")
    if (action.isdigit() and int(action) >= min and int(action) <= max): 
        return int(action)
    else:
        print(f"You must write a number from {min} to {max}.")
        return getInput(max, min, tryies - 1) if tryies > 0 else 0

clear()
print("  SQL MANAGER  ")
print("------------------------")
printDataBase()
print()
print("¿Qué desea hacer?")
print(" 0. Close")
print(" 1. Start")
print(" 2. Set Host")
print(" 3. Set DataBase")
print(" 4. Set Port")
print(" 5. Set User")
print(" 6. Set Password")
print(" 7. Set DataBase type")
print("------------------------")
print("\nWrite the number of your instruction:")

action = None
sql = None
while(sql == None or sql.isConnected() == False):

    # Si todos los parámetros fueron pasados por consola, se inicia automáticamente
    action = getInput(7) if len(consoleParam) <= 6 else 1
    consoleParam.clear()

    if action == 0: break
    elif action == 1: 
        sql = SQL(host, dbname, port, user, password, sqlType)
        if not sql.isConnected(): sql = None
    elif action == 2: host = input("HOST: ")
    elif action == 3: dbname = input("DATABASE: ")
    elif action == 4: port = input("PORT: ")
    elif action == 5: user = input("USER: ")
    elif action == 6: password = input("PASSWORD: ")
    elif action == 7: sqlType = input("DATABASE type (mysql, postgre): ")

while(sql != None):
    clear()
    print("  SQL MANAGER  ")
    print("------------------------")
    printDataBase()
    print("------------------------")
    print("What would you like to do?")
    print(" 0. Close")
    print(" 1. Select table")
    print(" 2. Create table")
    if table != None:
        print(f" 3. Columns of '{table}'")
        print(f" 4. Read '{table}'")
        print(f" 5. Add row in '{table}'")
        print(f" 6. Remove row from '{table}'")
        print(f" 7. Edit row from '{table}'")
        print(f" 8. Delete the table '{table}' (irreversible)")
        print(f" 9. Download '{table}' in CSV format")
        print(f" 10. Push CSV in '{table}'")
    print("------------------------")
    
    action = getInput(10) if table != None else getInput(2)
    print()

    try:
    
        if action == 0: break

        elif action == 1: # Seleccionar tabla
            tables = sql.getTables()
            print("Tablas:", " - ".join(tables))
            if len(tables) > 0: 
                tab = input("Write the TABLE name: ")
                print()
                if len(tab) == 0: print("You canceled the selection of a table.")
                elif tab == "-OMIT-": table = None
                elif not tab in tables: print("This table does not exists.")
                else:
                    print(f"You selected the table '{tab}'")
                    table = tab
            else: print("No public tables registered.")
            
        elif action == 2: # Crear tabla
            tables = sql.getTables()
            print("Tables registered:", " - ".join(tables))
            print("Write the TABLE NAME you want to create ")
            newtable = input(" -> ")
            print()
            if len(newtable) == 0: print("You canceled the creation of a table.")
            elif not newtable in tables: 
                result = sql.createTable(newtable)
                print()
                print("Success" if result == True else result)
                if result == True: table = newtable
            else: print(f"The table '{newtable}' already exists.")

        elif action == 3: # Columnas de la tabla
            columns = sql.getColumns(table)
            print(sql.queryDescribeColumns(table))
            for column in columns: print(column)

        elif action == 4: # Filas de la tabla
            columns = sql.getColumns(table)
            print(sql.querySelectRows(table))
            print("------------------------")
            sql.printColumns(columns)
            print("------------------------")
            rows = sql.getRows(table)
            sql.printRows(rows)
            print("------------------------")

        elif action == 5: # Agregar fila
            query = sql.queryAddRow(table)
            print(query)
            result = sql.addRow(query)
            print("Success" if result == True else result)

        elif action == 6: # Eliminar fila
            query = sql.queryRemoveRow(table)
            print(query)
            result = sql.removeRow(query)
            print("Success" if result == True else result)

        elif action == 7: # Editar fila
            query = sql.queryEditRow(table)
            print(query)
            result = sql.editRow(query)
            print("Success" if result == True else result)
            
        elif action == 8: # Eliminar tabla
            print(f"Are you sure you want to delete the table '{table}'?")
            print("If so, write the table name:")
            confirmation = input(" -> ")
            print()
            if confirmation == table:
                result = sql.deleteTable(table)
                if result == True:
                    print(f"You deleted the table '{confirmation}'.") 
                    table = None
                else: print(result)
            else: print(f"You canceled the delete of the table '{table}'.")

        elif action == 9: # Convertir Tabla en CSV
            path = f"./{table}.csv"
            result = csv.create(sql.getRows(table), sql.getColumns(table), path)
            if result == True: print("Success")
            else: print(result)

        elif action == 10: # Agregar CSV en la tabla
            print(f"Write the path of the CSV")
            path = input(" -> ")
            result = csv.push(path, sql, table)
            if result == True: print("Success")
            else: print(result)
    
    except Exception as err: 
        print("ERROR")
        print(err)

    input("\nPress ENTER to continue...\n")

try: sql.close() 
except: pass
sql = None
clear()