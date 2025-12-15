from sqlite3 import connect
from uuid import uuid4
from os import getenv
import requests
from consts import FACT_URL

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

factTable = '''CREATE TABLE IF NOT EXISTS fact (
    id INTEGER PRIMARY KEY CHECK(id = 1),
    text TEXT NOT NULL,
    permalink TEXT NOT NULL
  );'''

buttonIncrement = 'UPDATE counter SET value = value + 1 RETURNING value'
buttonValue = 'SELECT value FROM counter'
buttonLogInsert = 'INSERT INTO button_log(uuid, value, useragent, ip) VALUES(?,?,?,?)'

currentFact = 'SELECT text, permalink FROM fact WHERE id=1'
setFact = '''
  INSERT INTO fact(id, text, permalink) VALUES (1, ?, ?)
  ON CONFLICT(id) DO UPDATE SET
    text=excluded.text,
    permalink=excluded.permalink
'''

def createTables():
  with connect(DATABASE_FILE) as conn:
    cursor = conn.cursor()

    # Create the table that stores the current count
    cursor.execute(counterTable)
    # If that table is empty, set the value to 0
    cursor.execute('SELECT COUNT(*) FROM counter;')
    if cursor.fetchone()[0] == 0:
      cursor.execute('INSERT INTO counter DEFAULT VALUES;')

    # Create the table that logs button presses
    cursor.execute(buttonLogTable)

    # Create the table that stores the current fact
    cursor.execute(factTable)
    # If that table is empty, set the value to this fact
    cursor.execute('SELECT COUNT(*) FROM fact;')
    if cursor.fetchone()[0] == 0:
      fact = requests.get(FACT_URL).json()
      cursor.execute(setFact, (fact['text'], fact['permalink']))

    conn.commit()

def increment(useragent, ip):
  with connect(DATABASE_FILE) as conn:
    cursor = conn.cursor()
    cursor.execute(buttonIncrement)
    new_count = cursor.fetchone()[0]
    cursor.execute(buttonLogInsert, (str(uuid4()), new_count, useragent, ip))
    conn.commit()

def getButtonValue():
  with connect(DATABASE_FILE) as conn:
    cursor = conn.cursor()
    cursor.execute(buttonValue)
    return cursor.fetchone()[0]

def getCurrentFact():
  with connect(DATABASE_FILE) as conn:
    cursor = conn.cursor()
    cursor.execute(currentFact)
    row = cursor.fetchone()

    if row: fact = {"text": row[0], "permalink": row[1]}
    else: fact = None

    return fact

def rerollFact():
  with connect(DATABASE_FILE) as conn:
    cursor = conn.cursor()
    fact = requests.get(FACT_URL).json()
    cursor.execute(setFact, (fact['text'], fact['permalink']))
    return fact