import csvdb.converter as csv
from . import getPath, printResult, printList
from routes.colors import *

def connect(data):
    from sql import SQL
    sql = SQL(data.host, data.dbname, data.port, data.user, data.password, data.sqlType)
    return sql

# option 1
def reconnect(sql, data):
    printGreen("\nReconnecting...\n")
    try: sql.close()
    except: pass
    return connect(data)

# option 2
def showUsers(sql):
    printYellow(sql.queryGetUsers(),"\n")
    printList(sql.getUsers())

# option 3
def createUser(sql):
    printList(sql.getUsers(), subitem=0, end=", ")
    print()
    query = sql.queryCreateUser()
    printYellow(query)
    printResult(sql.commit(query))

# option 4
def deleteUser(sql):
    printList(sql.getUsers(), subitem=0, end=", ")
    print()
    query = sql.queryDeleteUser()
    printYellow(query)
    printResult(sql.commit(query))

# option 5
def grantPrivilegesToUser(sql, table = None):
    printList(sql.getUsers(), subitem=0, end=", ")
    print()
    query = sql.queryGrantPrivilegesToUser(table=table)
    printYellow(query)
    printResult(sql.commit(query))

# option 6
def selectTable(tables, data) -> str:
    printYellow(f"Tables:{COLOR_GREEN}", " - ".join(tables))
    if len(tables) > 0: 
        tab = input("Write the TABLE name: ")
        print()

        if len(tab) == 0: 
            printRed("You canceled the selection of a table.")
        
        elif not tab in tables: 
            printRed("This table does not exists.")
            data.table = None

        else:
            printGreen(f"You selected the table '{tab}'")
            data.table = tab
    else: 
        printMagenta("No public tables registered.")
        data.table = None

# option 7
def createTable(sql, data):
    if sql.isConnected():
        tables = sql.getTables(0)
        printYellow(f"Tables registered:{COLOR_GREEN}", " - ".join(tables))
        printCyan("Write the TABLE NAME you want to create ")
        newtable = input(" -> ")
        print()
        if len(newtable) == 0: printRed("You canceled the creation of a table.")
        elif not newtable in tables: 
            result = sql.createTable(newtable)
            print()
            print("Success" if result == True else result)
            if result == True: data.table = newtable
        else: printMagenta(f"The table '{newtable}' already exists.")

# option 8
def showPrivilegesInTable(sql, table:str = None):
    query = sql.queryGetPrivilegesInTable(table)
    printYellow(query)
    privileges = sql.getPrivilegesInTable(table)
    printList(privileges)

# option 9
def tableColumns(sql, table):
    columns = sql.getColumns(table)
    printYellow(sql.queryGetColumns(table))
    printList(columns)

# option 10
def tableRows(sql, table):
    columns = sql.getColumns(table)
    printYellow(sql.queryGetRows(table))
    printCyan("------------------------")
    sql.printColumns(columns)
    printCyan("------------------------")
    rows = sql.getRows(table)
    sql.printRows(rows)
    printCyan("------------------------")

# option 11
def addRow(sql, table):
    query = sql.queryAddRow(table)
    printYellow(query)
    printResult(sql.commit(query))

# option 12
def removeRow(sql, table):
    query = sql.queryRemoveRow(table)
    printYellow(query)
    printResult(sql.removeRow(query))

# option 13
def editRow(sql, table):
    query = sql.queryEditRow(table)
    printYellow(query)
    printResult(sql.editRow(query))

# option 14
def dropTable(sql, data):
    print(f"Are you sure you want to delete the table '{data.table}'?")
    print("If so, write the table name:")
    confirmation = input(f"{COLOR_MAGENTA} -> {COLOR_RED}")
    printYellow()
    if confirmation == data.table:
        result = sql.deleteTable(data.table)
        if result == True:
            printGreen(f"You deleted the table '{confirmation}'.") 
            data.table = None
        else: printRed(result)
    else: printMagenta(f"You canceled the delete of the table '{data.table}'.")

# option 15
def convertTableToCSV(sql, table):
    path = getPath(f"{table}.csv")
    result = csv.create(sql.getRows(table), sql.getColumns(table), path)
    printResult(result)

# option 16
def convertCSVToTable(sql, table):
    print(f"Write the path of the CSV")
    path = input(" -> ")
    printResult(csv.push(path, sql, table))

# option 17
def customCommand(sql):
    printMagenta("Your command require 'fetch' or 'commit'?")
    required = input("Write the required option -> ")
    if required == "fetch": 
        printYellow(f"Write your '{required}' command:")
        command = input(" -> ")
        result = sql.fetch(command)
        printResult(result)
    elif required == "commit": 
        printYellow(f"Write your '{required}' command:")
        command = input(" -> ")
        result = sql.commit(command)
        for res in result: print(res)
