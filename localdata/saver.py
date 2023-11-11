from . import FileData, localDB, TABLE_NAME, TABLE_COLUMNS

def saveInLocalData(data):
    try:
        from manager.methods import connect
        fileData = FileData(data)
        fileData.encrypt()
        sql = connect(localDB())
        sql.deleteTable(TABLE_NAME)
        sql.createTable(TABLE_NAME, TABLE_COLUMNS)
        sql.addRow(TABLE_NAME, fileData.dictionary())
        sql.close()
    except: pass