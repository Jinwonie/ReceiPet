import sqlite3
from conf import Config
from src import insert_inv_code

if __name__ == "__main__":
    con = sqlite3.connect(Config.SQL_DIR)
    cursor = con.cursor()
    insert_inv_code(con, cursor)
    con.commit()
    con.close()
