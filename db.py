import sqlite3

class Items:
    def __init__(self, database_name="fridge.db"):
        ''' Starting database '''
        self.con = sqlite3.connect(database_name)
        self.cur = self.con.cursor()
        try:
            self.create_items_table()
        except:
            print("Table already exists")

    def create_items_table(self):
        self.cur.execute('''CREATE TABLE items (name varchar(100) PRIMARY KEY, fridge Boolean, grocery Boolean, last_updated date, quantity int)''')

    @staticmethod
    def row_to_dict(db_row):
        """Converts database row to dictionary """
        return {
            'name': db_row[0],
            'fridge': db_row[1],
            'grocery': db_row[2],
            'date': db_row[3],
            'quantity': db_row[4]
        }


    def add_item(self, name, fridge, grocery, date, quantity):
        self.cur.execute("INSERT INTO items VALUES (?, ?, ?, ?, ?)",(name, fridge, grocery, date, quantity))
        self.con.commit()

    def get_all_items(self):
        self.cur.execute('SELECT * FROM items')
        items = self.cur.fetchall()
        return items

    def get_one_item(self, name):
        self.cur.execute('SELECT * FROM items WHERE name = ?', (name,))
        return self.cur.fetchone()

    def get_fridge_items(self):
        self.cur.execute('SELECT * FROM items WHERE fridge = 1')
        fridge_items = self.cur.fetchall()
        return fridge_items

    def get_grocery_items(self):
        self.cur.execute('SELECT * FROM items WHERE grocery = 1')
        grocery_items = self.cur.fetchall()
        return grocery_items

    def update_quantity(self, name, new_quantity):
        self.cur.execute('UPDATE items SET quantity=? WHERE name = ?', (new_quantity, name))
        self.con.commit()

    def update_location(self, name, fridge, grocery):
        self.cur.execute('UPDATE items SET fridge = ?, grocery = ? WHERE name = ?', (fridge, grocery, name))

    def delete_item(self, name):
        self.cur.execute('DELETE FROM items WHERE name = ?', (name,))
        self.con.commit()

    def close_db(self):
        self.con.close()

if __name__ == "__main__":
    our_fridge = Items()
    our_fridge.add_item(name="yogurt", fridge=0, grocery=1, date='2015-07-20', quantity=3)
    our_fridge.get_fridge_items()
    our_fridge.get_grocery_items()
    our_fridge.get_all_items()
