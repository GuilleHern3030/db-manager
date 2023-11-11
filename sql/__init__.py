def SQL(dbHost, dbName, dbPort, dbUser, dbPassword, dbType):
    try:

        if dbType == 'mysql':
            from .mysql import MYSQL
            return MYSQL(dbHost, dbName, dbPort, dbUser, dbPassword)
        
        elif dbType == 'postgre':
            from .postgre import POSTGRE
            return POSTGRE(dbHost, dbName, dbPort, dbUser, dbPassword)
        
        elif dbType == 'sqlite':
            from .sqlite import SQLITE
            return SQLITE(dbHost, dbName, dbPort, dbUser, dbPassword)
        
        else: raise Exception(f"{dbType} databases is not supported.")
    except Exception as err:
        from .invalid import InvalidDB
        return InvalidDB(err)

def inputNotNull(ask:str, tryies=3):
    ans = input(ask)
    while (tryies > 0 and len(ans) == 0):
        tryies -= 1
        ans = input(ask)
    if len(ans) == 0: raise Exception("Invalid input")
    else: return ans

def inputIfNull(param:str, ask:str, tryies=3):
    if param == None or len(param) == 0: 
        return inputNotNull(ask, tryies)
    else: return param
    
def inputList(aList:list, nullIsEqualsTo="NULL", emptyIsEqualsTo=None) -> dict:
    dictionary = {}
    for i in range(len(aList)):
        key = aList[i] 
        value = input(f"Write the '{aList[i]}' value: ")
        if value == "NULL": value = nullIsEqualsTo
        if len(value) == 0: value = emptyIsEqualsTo
        if value != None and len(value) > 0:
            if value == nullIsEqualsTo: dictionary[key] = nullIsEqualsTo 
            elif value == emptyIsEqualsTo: dictionary[key] = emptyIsEqualsTo
            elif value.isdigit(): dictionary[key] = value
            else: dictionary[key] = f"'{value}'"
    return dictionary

def inputPrivileges(table:str|None=""):
    privileges = []
    if table == None or len(table) == 0: table = "ALL TABLES"
    ask = lambda privilege, question: privileges.append(privilege) if input(question) == "yes" else None
    ask("SELECT", f"Can the user READ ROWS in the table '{table}'? (yes/no)\n -> ")
    ask("INSERT", f"Can the user INSERT ROWS in the table '{table}'? (yes/no)\n -> ")
    ask("UPDATE", f"Can the user EDIT ROWS in the table '{table}'? (yes/no)\n -> ")
    ask("DELETE", f"Can the user DELETE ROWS in the table '{table}'? (yes/no)\n -> ")
    return privileges

def isParamStartsWith(param:str|None, startsWith:str):
    return isinstance(param, str) and param.startswith(startsWith)