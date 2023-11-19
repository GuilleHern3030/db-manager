from io import StringIO
import csv

SEPARATOR = ","

def parseColumns(columnList:list, valuesList:list) -> dict:
    dictionary = {}
    for i in range(len(columnList)):
        #value = valuesList[i].replace('"', "'")
        value = valuesList[i].strip('"').strip().strip('"')
        if value.lower() == "null" or value.lower() == "nan": value = "NULL"
        elif value.isdigit(): value = value
        else: value = f"'{value}'"
        dictionary[columnList[i]] = value
    return dictionary

def push(path:str, sql, table:str) -> bool:
    try:
        if path == None or len(path) == 0: raise Exception("No csv selected")
        firstLine = True
        columns = list(map(lambda columns: columns[0], sql.getColumns(table)))
        with open(path, "r") as file:
            for line in file:
                if firstLine:
                    firstLine = False
                    continue
                text = StringIO(line)
                content = csv.reader(text, delimiter=',')
                cells = []
                for cell in content: cells.extend(cell)
                columnsDict = parseColumns(columns, cells)
                print(sql.queryAddRow(table, columnsDict))
                result = sql.addRow(table, parseColumns(columns, cells))
                if result != True: raise(result)
        print()
        return True
    except Exception as err: return err

def create(rows, columns, path:str = None) -> bool:
    try:
        if path == None or len(path) == 0: raise Exception("No csv selected")
        with open(path, "w") as file:
            header = SEPARATOR.join(list(map(lambda columns: f'"{columns[0]}"', columns)))
            file.write(header + "\n")
            for row in rows: 
                cells = list()
                for cell in row:
                    try: cells.append("NULL" if cell == None or cell == '' or cell.lower() == 'null' or cell.lower() == 'nan' else f'"{cell}"')
                    except: cells.append(f'"{cell}"') # is a number
                file.write(SEPARATOR.join(cells) + "\n")
        print("CSV created in:")
        print(path)
        print()
        return True
    except Exception as err: return err