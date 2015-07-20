import sqlite3

''' Starting database '''
con = sqlite3.connect('fridge.db')
cur = con.cursor()
cur.execute('SELECT SQLITE_VERSION()')
data = cur.fetchone()
print(data)


def start_db():
    cur.execute('''CREATE TABLE items (name varchar(100) PRIMARY KEY, fridge Boolean, grocery Boolean, last_updated date, quantity int)''')


def add_item(name, fridge, grocery, date, quantity):
    cur.execute("INSERT INTO items VALUES (?, ?, ?, ?, ?)",(name, fridge, grocery, date, quantity))
    con.commit()


def get_item():
    cur.execute('SELECT * FROM items')
    items = cur.fetchall()
    print(items)

add_item(name='apples', fridge=True, grocery=False, date='2015-07-20', quantity=5)

get_item()

con.close()
