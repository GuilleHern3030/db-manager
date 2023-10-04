from src.sql.manager import SQL
from os import system as osExecute, name as osName
from sys import argv as consoleParam

host = consoleParam[1] if len(consoleParam) > 1 else "localhost"
dbname = consoleParam[2] if len(consoleParam) > 2 else "dbname"
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
        print(f"Debes escribir un número del {min} al {max}.")
        return getInput(max, min, tryies - 1) if tryies > 0 else 0

clear()
print("  SQL MANAGER  ")
print("------------------------")
printDataBase()
print()
print("¿Qué desea hacer?")
print(" 0. Salir")
print(" 1. Iniciar")
print(" 2. Cambiar Host")
print(" 3. Cambiar DataBase")
print(" 4. Cambiar Port")
print(" 5. Cambiar User")
print(" 6. Cambiar Password")
print(" 7. Cambiar tipo de base de datos")
print("------------------------")
print("\nEscriba el número de su instrucción:")

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
    elif action == 2: host = input("Escriba el HOST: ")
    elif action == 3: dbname = input("Escriba el DATABASE: ")
    elif action == 4: port = input("Escriba el PORT: ")
    elif action == 5: user = input("Escriba el USER: ")
    elif action == 6: password = input("Escriba el PASSWORD: ")
    elif action == 7: sqlType = input("Tipo de DATABASE (mysql, postgre): ")

while(sql != None):
    clear()
    print("  SQL MANAGER  ")
    print("------------------------")
    printDataBase()
    print("------------------------")
    print("¿Qué desea hacer?")
    print(" 0. Salir")
    print(" 1. Seleccionar tabla")
    print(" 2. Crear tabla")
    if table != None:
        print(f" 3. Columnas de la tabla '{table}'")
        print(f" 4. Leer tabla '{table}'")
        print(f" 5. Agregar fila en '{table}'")
        print(f" 6. Eliminar fila de '{table}'")
        print(f" 7. Editar fila de '{table}'")
        print(f" 8. Eliminar tabla '{table}'")
    print("------------------------")
    
    action = getInput(8) if table != None else getInput(2)
    print()

    try:
    
        if action == 0: break

        elif action == 1: # Seleccionar tabla
            tables = sql.getTables()
            print("Tablas:", " - ".join(tables))
            if len(tables) > 0: 
                tab = input("Escriba el nombre de la TABLA: ")
                print()
                if len(tab) == 0: print("Cancelaste la selección de una tabla")
                elif tab == "-OMIT-": table = None
                elif not tab in tables: print("Esa tabla no existe en la base de datos")
                else:
                    print(f"Se ha seleccionado la tabla '{tab}'")
                    table = tab
            else: print("No hay tablas registradas")
            
        elif action == 2: # Crear tabla
            tables = sql.getTables()
            print("Tablas existentes:", " - ".join(tables))
            print("Escriba el nombre de la TABLA que quiere crear ")
            newtable = input(" -> ")
            print()
            if len(newtable) == 0: print("Cancelaste la creación de una tabla")
            elif not newtable in tables: 
                result = sql.addRow(query)
                print("Success" if result == True else result)
                if result == True: table = newtable
            else: print("Error: Esa tabla ya existe")

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
            print(f"¿Estás seguro de querer eliminar la tabla '{table}'")
            print("Si es así, escriba el nombre de la tabla:")
            confirmation = input(" -> ")
            print()
            if confirmation == table:
                result = sql.deleteTable(table)
                if result == True:
                    print(f"Eliminaste la tabla '{confirmation}'") 
                    table = None
                else: print(result)
            else: print(f"Cancelaste el borrado de la tabla '{table}'")
    
    except Exception as err: 
        print("ERROR")
        print(err)

    input("\nPresiona ENTER para continuar...")

try: sql.close() 
except: pass
sql = None
clear()