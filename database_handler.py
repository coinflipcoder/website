from sqlite3 import connect
from uuid import uuid4
from consts import DATABASE_FILE

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
    with connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(buttonLogTable)
        conn.commit()

def insertButtonLog(value, useragent, ip):
    with connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(buttonLogInsert, (str(uuid4()), value, useragent, ip))
        conn.commit()

def getButtonValue():
    with connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(buttonLogGetValue)
        value = cursor.fetchone()
        if value == None: return 0
        return value[0]