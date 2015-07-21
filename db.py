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


def get_all_items():
    cur.execute('SELECT * FROM items')
    items = cur.fetchall()
    print(items)

def get_fridge_items():
    cur.execute('SELECT * FROM items WHERE fridge = TRUE')
    fridge_items = cur.fetchall()
    print(fridge_items)

def get_grocery_items():
    cur.execute('SELECT * FROM items WHERE grocery = TRUE')
    grocery_items = cur.fetchall()
    print(grocery_items)

def update_quantity(name, new_quantity):
    cur.execute('UPDATE items SET quantity=? WHERE name = ?', (name, new_quantity))
    con.commit()

def delete_item(name):
    cur.execute('DELETE FROM items WHERE name = ?', name)
    con.commit()


# add_item(name='apples', fridge=True, grocery=False, date='2015-07-20', quantity=5)

get_all_items()

con.close()
