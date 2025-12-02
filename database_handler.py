from sqlite3 import connect
from uuid import uuid4

database = 'database.db'

buttonLogTable = '''CREATE TABLE IF NOT EXISTS button_log (
        uuid TEXT PRIMARY KEY,
        value INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        useragent TEXT,
        ip TEXT
    );'''

buttonLogInsert = 'INSERT INTO button_log(uuid, value, useragent, ip) VALUES(?,?,?,?)'
buttonLogGetValue = 'SELECT value FROM button_log ORDER BY value DESC LIMIT 1'

def createTables():
    print("Creating tables...")
    with connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(buttonLogTable)
        print("Button log table created.")
        conn.commit()
    print("All tables created..")

def insertButtonLog(value, useragent, ip):
    print("Button pressed. Inserting into log...")
    with connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(buttonLogInsert, (str(uuid4()), value, useragent, ip))
        conn.commit()

def getButtonValue():
    with connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(buttonLogGetValue)
        value = cursor.fetchone()
        return value[0]