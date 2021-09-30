import sqlite3
import datetime


class Database:
    def __init__(self):
        self.con = sqlite3.connect('products.db')
        self.cursor = self.con.cursor()

        self.create_parts_table()


    def create_parts_table(self):
        '''Create the table containig parts if it does not exist'''
        self.cursor.execute("CREATE TABLE IF NOT EXISTS products(id integer PRIMARY KEY AUTOINCREMENT, description varchar(50) NOT NULL, price FLOAT NOT NULL, date_created DATE)")
        self.con.commit()

    def create_entry(self, description, price, date_created):
        '''Create a products entry'''
        self.cursor.execute("INSERT INTO products(description, price, date_created) VALUES (?, ?, ?)", (description, float(price), date_created))
        self.con.commit()

    def get_products(self):
        '''Get the products in the database'''
        all_products = self.cursor.execute("SELECT * FROM products")
        return all_products

    def get_product_by_id(self, id):
        '''Get the element with the specified id'''
        product = self.cursor.execute("SELECT * FROM products WHERE id=?", (id,))
        return product

    def get_products_by_description(self, description):
        '''Get elements with a description similar to that given by the user'''
        products = self.cursor.execute("SELECT * FROM products WHERE description LIKE ?", ('%'+description+'%',))
        return products

    def update_product(self, id, description, price, date_created):
        '''Update the selected product'''
        self.cursor.execute("UPDATE products SET description=?, price=?, date_created=? WHERE id=?", (description, price, date_created, id))
        self.con.commit()

    def delete_product(self, id):
        '''Delete the product'''
        self.cursor.execute("DELETE FROM products WHERE id=?", (id))
        self.con.commit()

    def close_db_connection(self):
        '''Close the connection to the database'''
        self.con.close()