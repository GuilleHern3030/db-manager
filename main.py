from routes.login import log
from routes.sqlmanager import manage
from manager.data import Data

def main():
    data = Data()
    sql = log(data)
    if sql != None: 
        manage(sql, data)

if __name__ == '__main__':
    try: main()
    except Exception as err:
        print()
        print("An error has been ocurred!")
        print(err)
        input()
