from . import clear, getInput
from .colors import *
from manager.methods import *

def manage(sql, data):
    while(True):
        clear()

        printRed("               SQL MANAGER  ")
        printBlue("------------------------------------------------")
        data.printDataBase()
        printBlue("------------------------------------------------")
        printYellow(" What would you like to do?")
        print(f"  0. {COLOR_RED} Close {COLOR_DEFAULT}")
        print(f"  1. {COLOR_WHITE} Restart connection{COLOR_DEFAULT}")
        if sql.isConnected():
            print(f"  2. {COLOR_MAGENTA} View users {COLOR_DEFAULT}")
            print(f"  3. {COLOR_MAGENTA} Create user {COLOR_DEFAULT}")
            print(f"  4. {COLOR_MAGENTA} Delete user {COLOR_DEFAULT}")
            print(f"  5. {COLOR_MAGENTA} Grant privileges to user {COLOR_DEFAULT}")
            print(f"  6. {COLOR_GREEN} Select table {COLOR_DEFAULT}")
            print(f"  7. {COLOR_GREEN} Create table {COLOR_DEFAULT}")
            if data.table != None:
                print(f"  8. {COLOR_GREEN} Privileges of '{data.table}'{COLOR_DEFAULT}")
                print(f"  9. {COLOR_GREEN} Columns of '{data.table}'{COLOR_DEFAULT}")
                print(f"  10.{COLOR_GREEN} Read '{data.table}'{COLOR_DEFAULT}")
                print(f"  11.{COLOR_GREEN} Add row in '{data.table}'{COLOR_DEFAULT}")
                print(f"  12.{COLOR_GREEN} Remove row from '{data.table}'{COLOR_DEFAULT}")
                print(f"  13.{COLOR_GREEN} Edit row from '{data.table}'{COLOR_DEFAULT}")
                print(f"  14.{COLOR_GREEN} Delete the table '{data.table}'{COLOR_RED} (irreversible){COLOR_DEFAULT}")
                print(f"  15.{COLOR_BLUE} Download '{data.table}' in CSV format{COLOR_DEFAULT}")
                print(f"  16.{COLOR_BLUE} Upload CSV in '{data.table}'{COLOR_DEFAULT}")
                print(f"  17.{COLOR_CYAN} Custom command{COLOR_DEFAULT}")
        printBlue("------------------------------------------------")
        
        action = None
        if not sql.isConnected(): action = getInput(1)
        elif data.table == None: action = getInput(7)
        else: action = getInput(17)
        print()

        try:
        
            if action == 0: break
            elif action == 1: sql = reconnect(sql, data) # Reinciar conexión
            elif action == 2: showUsers(sql) # Ver todos los usuarios de la base de datos
            elif action == 3: createUser(sql) # Crear un usuario para la base de datos
            elif action == 4: deleteUser(sql) # Elimina un usuario para la base de datos
            elif action == 5: grantPrivilegesToUser(sql, data.table) # Dar permisos a un usuario
            elif action == 6: selectTable(sql.getTables(0), data) # Seleccionar tabla
            elif action == 7: createTable(sql, data) # Crear tabla
            elif action == 8: showPrivilegesInTable(sql, data.table) # Ver privilegios de la tabla
            elif action == 9: tableColumns(sql, data.table) # Columnas de la tabla
            elif action == 10: tableRows(sql, data.table) # Filas de la tabla
            elif action == 11: addRow(sql, data.table) # Agregar fila
            elif action == 12: removeRow(sql, data.table) # Eliminar fila
            elif action == 13: editRow(sql, data.table) # Editar fila
            elif action == 14: dropTable(sql, data) # Eliminar tabla
            elif action == 15: convertTableToCSV(sql, data.table) # Convertir Tabla en CSV
            elif action == 16: convertCSVToTable(sql, data.table) # Agregar CSV en la tabla
            elif action == 17: customCommand(sql) # Ejecutar un comando personalizado
        
        except Exception as err: 
            printMagenta(" ERROR ")
            printRed(err)

        if data.table != None and len(sql.getTables()) == 0: sql.close()

        input("\n Press ENTER to continue...\n")

    try: sql.close() 
    except: pass
    sql = None
    clear()