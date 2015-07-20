import sqlite3

con = sqlite3.connect('fridge.db')

cur = con.cursor()

cur.execute('SELECT SQLITE_VERSION()')

data = cur.fetchone()

print(data)

cur.execute('''CREATE TABLE items (name varchar(100) PRIMARY KEY, fridge Boolean, grocery Boolean, last_updated date, quantity int)''')

con.close()
