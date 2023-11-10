from . import clear, getInput
from manager.methods import *

def manage(sql, data):
    while(True):
        clear()

        print("  SQL MANAGER  ")
        print("------------------------")
        data.printDataBase()
        print("------------------------")
        print("What would you like to do?")
        print(" 0. Close")
        print(" 1. Restart connection")
        if sql.isConnected():
            print(" 2. View users")
            print(" 3. Create user")
            print(" 4. Grant privileges to user")
            print(" 5. Select table")
            print(" 6. Create table")
            if data.table != None:
                print(f" 7. Privileges of '{data.table}'")
                print(f" 8. Columns of '{data.table}'")
                print(f" 9. Read '{data.table}'")
                print(f" 10. Add row in '{data.table}'")
                print(f" 11. Remove row from '{data.table}'")
                print(f" 12. Edit row from '{data.table}'")
                print(f" 13. Delete the table '{data.table}' (irreversible)")
                print(f" 14. Download '{data.table}' in CSV format")
                print(f" 15. Upload CSV in '{data.table}'")
                print(f" 16. Custom command")
        print("------------------------")
        
        action = getInput(16) if data.table != None else getInput(3)
        print()

        try:
        
            if action == 0: break
            elif action == 1: sql = reconnect(sql, data) # Reinciar conexión
            elif action == 2: viewUsers(sql) # Ver todos los usuarios de la base de datos
            elif action == 3: createUser(sql) # Crear un usuario para la base de datos
            elif action == 4: grantPrivileges(sql, data.table) # Dar permisos a un usuario
            elif action == 5: selectTable(sql.getTables(), data) # Seleccionar tabla
            elif action == 6: createTable(sql, data) # Crear tabla
            elif action == 7: getPrivileges(sql, data.table) # Ver privilegios de la tabla
            elif action == 8: tableColumns(sql, data.table) # Columnas de la tabla
            elif action == 9: tableRows(sql, data.table) # Filas de la tabla
            elif action == 10: addRow(sql, data.table) # Agregar fila
            elif action == 11: removeRow(sql, data.table) # Eliminar fila
            elif action == 12: editRow(sql, data.table) # Editar fila
            elif action == 13: dropTable(sql, data) # Eliminar tabla
            elif action == 14: convertTableToCSV(sql, data.table) # Convertir Tabla en CSV
            elif action == 15: convertCSVToTable(sql, data.table) # Agregar CSV en la tabla
            elif action == 16: customCommand(sql) # Ejecutar un comando personalizado
        
        except Exception as err: 
            print("ERROR")
            print(err)

        if data.table != None and len(sql.getTables()) == 0: sql.close()

        input("\nPress ENTER to continue...\n")

    try: sql.close() 
    except: pass
    sql = None
    clear()