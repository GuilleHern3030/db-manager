import csv.converter as csv
from . import getPath

def printResult(result):
    print("Success" if result == True else result)

def connect(data):
    from sql.manager import SQL
    sql = SQL(data.host, data.dbname, data.port, data.user, data.password, data.sqlType)
    return sql

def reconnect(sql, data):
    try: sql.close()
    except: pass
    return connect(data)

def selectTable(tables, data) -> str:
    print("Tables:", " - ".join(tables))
    if len(tables) > 0: 
        tab = input("Write the TABLE name: ")
        print()

        if len(tab) == 0: 
            print("You canceled the selection of a table.")
        
        elif not tab in tables: 
            print("This table does not exists.")
            data.table = None

        else:
            print(f"You selected the table '{tab}'")
            data.table = tab
    else: 
        print("No public tables registered.")
        data.table = None

def createTable(sql, data):
    if sql.isConnected():
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
            if result == True: data.table = newtable
        else: print(f"The table '{newtable}' already exists.")

def tableColumns(sql, table):
    columns = sql.getColumns(table)
    print(sql.queryDescribeColumns(table))
    for column in columns: print(column)

def tableRows(sql, table):
    columns = sql.getColumns(table)
    print(sql.querySelectRows(table))
    print("------------------------")
    sql.printColumns(columns)
    print("------------------------")
    rows = sql.getRows(table)
    sql.printRows(rows)
    print("------------------------")

def addRow(sql, table):
    query = sql.queryAddRow(table)
    print(query)
    printResult(sql.addRow(query))

def removeRow(sql, table):
    query = sql.queryRemoveRow(table)
    print(query)
    printResult(sql.removeRow(query))

def editRow(sql, table):
    query = sql.queryEditRow(table)
    print(query)
    printResult(sql.editRow(query))

def dropTable(sql, data):
    print(f"Are you sure you want to delete the table '{data.table}'?")
    print("If so, write the table name:")
    confirmation = input(" -> ")
    print()
    if confirmation == data.table:
        result = sql.deleteTable(data.table)
        if result == True:
            print(f"You deleted the table '{confirmation}'.") 
            data.table = None
        else: print(result)
    else: print(f"You canceled the delete of the table '{data.table}'.")

def convertTableToCSV(sql, table):
    path = getPath(f"{table}.csv")
    result = csv.create(sql.getRows(table), sql.getColumns(table), path)
    printResult(result)

def convertCSVToTable(sql, table):
    print(f"Write the path of the CSV")
    path = input(" -> ")
    printResult(csv.push(path, sql, table))

def createUser(sql):
    query = sql.queryCreateUser()
    print(query)
    printResult(sql.__query_commit__(query))

def viewUsers(sql):
    print(sql.queryViewUsers(),"\n")
    users = sql.getUsers()
    for user in users: print(user)

def grantPrivileges(sql, table = None):
    users = sql.getUsers()
    for user in users: print(user[0], end=", ")
    print()
    query = sql.queryGrantPrivilegesToUser(table)
    print(query)
    printResult(sql.__query_commit__(query))

def getPrivileges(sql, table:str = ""):
    query = sql.queryViewPrivilegesInTable(table)
    print(query)
    privileges = sql.getPrivilegesInTable(table)
    for privilege in privileges: print(privilege)

def customCommand(sql):
    print("Your command require 'fetch' or 'commit'?")
    required = input("Write the required option -> ")
    if required == "fetch": 
        print(f"Write your '{required}' command:")
        command = input(" -> ")
        result = sql.__query_fetchAll__(command)
        printResult(result)
    elif required == "commit": 
        print(f"Write your '{required}' command:")
        command = input(" -> ")
        result = sql.__query_commit__(command)
        for res in result: print(res[0])
