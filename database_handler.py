from sqlite3 import connect
from uuid import uuid4
from os import getenv

DATABASE_FILE = getenv("DATABASE_PATH", "./database.db")

counterTable = '''CREATE TABLE IF NOT EXISTS counter (
    value INTEGER NOT NULL DEFAULT 0
  );'''

buttonLogTable = '''CREATE TABLE IF NOT EXISTS button_log (
    uuid TEXT PRIMARY KEY,
    value INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    useragent TEXT,
    ip TEXT
  );'''

buttonIncrement = 'UPDATE counter SET value = value + 1 RETURNING value;'
buttonValue = 'SELECT value FROM counter;'
buttonLogInsert = 'INSERT INTO button_log(uuid, value, useragent, ip) VALUES(?,?,?,?)'

def createTables():
  with connect(DATABASE_FILE) as conn:
    cursor = conn.cursor()
    # Create the table that stores the current count
    cursor.execute(counterTable)

    # If that table is empty, set the value to 0
    cursor.execute('SELECT COUNT(*) FROM counter')
    if cursor.fetchone()[0] == 0:
      cursor.execute('INSERT INTO counter DEFAULT VALUES')

    cursor.execute(buttonLogTable)
    conn.commit()

def increment(useragent, ip):
  with connect(DATABASE_FILE) as conn:
    cursor = conn.cursor()
    cursor.execute(buttonIncrement)
    new_count = cursor.fetchone()[0]

    cursor.execute(buttonLogInsert, (str(uuid4()), new_count, useragent, ip))
    conn.commit()
    return new_count

def getButtonValue():
  with connect(DATABASE_FILE) as conn:
    cursor = conn.cursor()
    cursor.execute(buttonValue)
    return cursor.fetchone()[0]