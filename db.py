import sqlite3
import datetime
from pdf import ExtractToPdf


class Database:
    def __init__(self):
        self.con = sqlite3.connect('products.db')
        self.cursor = self.con.cursor()

        self.create_products_table()


    def create_products_table(self):
        '''Create the table containig parts if it does not exist'''
        self.cursor.execute("CREATE TABLE IF NOT EXISTS products(id integer PRIMARY KEY AUTOINCREMENT, description varchar(50) NOT NULL, price FLOAT NOT NULL, date_created DATE, measure varchar(15), category varchar(15), track BOOLEAN NOT NULL CHECK (track IN (0, 1)), picture varchar(30))")
        self.con.commit()

    def create_entry(self, description, price, date_created, measure, category, track, picture):
        '''Create a products entry'''
        self.cursor.execute("INSERT INTO products(description, price, date_created, measure, category, track, picture) VALUES (?, ?, ?, ?, ?, ?, ?)", (description, float(price), date_created, measure, category, track, picture))
        self.con.commit()

    def get_products(self):
        '''Get the products in the database'''
        all_products = self.cursor.execute("SELECT id, description, price, date_created, measure, category, track FROM products")
        return all_products

    def get_product_by_id(self, id):
        '''Get the element with the specified id'''
        product = self.cursor.execute("SELECT id, description, price, date_created, measure, category, track FROM products WHERE id=?", (id,))
        return product

    def get_products_by_description(self, description):
        '''Get elements with a description similar to that given by the user'''
        products = self.cursor.execute("SELECT id, description, price, date_created, measure, category, track FROM products WHERE description LIKE ?", ('%'+description+'%',))
        return products

    def update_product(self, id, description, price, date_created, measure, category, track, picture):
        '''Update the selected product'''
        self.cursor.execute("UPDATE products SET description=?, price=?, date_created=?, measure=?, category=?, track=?, picture=? WHERE id=?", (description, price, date_created, measure, category, track, picture,id))
        self.con.commit()

    def delete_product(self, id):
        '''Delete the product'''
        self.cursor.execute("DELETE FROM products WHERE id=?", (id,))
        self.con.commit()
    
    def get_product_picture(self, id):
        '''Get product picture location'''
        pic = self.cursor.execute("SELECT picture FROM products WHERE id=?", (id,))
        return str(list(pic)[0][0])

    def export_data_to_pdf(self):
        all_products = self.cursor.execute("SELECT * FROM products")
        ExtractToPdf(all_products)

    def close_db_connection(self):
        '''Close the connection to the database'''
        self.con.close()