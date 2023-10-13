from tkinter import filedialog

SEPARATOR = ","

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
        print()
        return True
    except Exception as err: return err

def push(path:str, sql, table:str) -> bool:
    try:
        if path == None or len(path) == 0: raise Exception("No csv selected")
        firstLine = True
        columns = ",".join(list(map(lambda columns: columns[0], sql.getColumns(table))))
        with open(path, "r") as file:
            for line in file:
                if firstLine:
                    firstLine = False
                    continue
                cells = line.strip()
                query = f"({columns}) VALUES ({cells})"
                print(query)
                sql.addRow(table, query)
        print()
        return True
    except Exception as err: return err
