from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.picker import MDDatePicker
from db import Database


class MainApp(MDApp):
    def build(self):
        # set the theme color
        self.theme_cls.primary_palette = "DeepPurple"

        #create the database and connect
        self.database = Database()

        # data table
        self.data_table = MDDataTable(
            size_hint=(1, 0.53),
            use_pagination= True,
            check=True,
            # pos_hint={'center_x': .5, 'y':.05},
            column_data=[
                ("Id", dp(30)),
                ("Description", dp(60)),
                ("Price", dp(30)),
                ("Date", dp(30)),
            ],
            row_data = [],
        )

        self.root.ids['datatable'].add_widget(self.data_table)
        self.data_table.row_data = [
            ('1', 'Food for thought', 21.56, '21/04/2021'),
            ('2', 'Food for thought', 21.56, '21/04/2021'),
            ('3', 'Food for thought', 21.56, '21/04/2021'),
            ('4', 'Food for thought', 21.56, '21/04/2021'),
            ('5', 'Food for thought', 21.56, '21/04/2021'),
            ('6', 'Food for thought', 21.56, '21/04/2021'),
            ('7', 'Food for thought', 21.56, '21/04/2021')
        ]

   # Data table

    def on_save(self, instance, value, date_range):
        '''Called when we select a date from the datetime picker'''
        self.root.ids['date_field'].text = str(value)
        print(value)


    def show_date_picker(self):
        '''Show the datepicker'''
        self.root.ids['date_field'].focus = False
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()


    # Search
    def search(self):
        '''Search values in the database'''
        print(self.root.ids['search'].text)

    def insert_date(self, description, price, date):
        '''Inserts data into the database'''
        self.database.create_entry(description, price, date)

    
    # Database Operations
    def insert_data(self):
        """Insert data into the database"""
        description = self.root.ids['description_field'].text
        price = self.root.ids['price_field'].text
        date = self.root.ids['date_field'].text

        self.database.create_entry(description, price, date)
        self.reload_data_table()
        
    def update_data(self, id,description, price, date):
        '''Update the data in the database for the given primary key'''
        self.database.update_product(id, description, price, date)
        self.reload_data_table()

    def delete_data(self, id):
        '''Delete data with the given id'''
        self.database.delete_product(id)
        self.reload_data_table()

    def reload_data_table(self):
        '''Reload the datatable after an action e.g update, delete or insert'''
        self.data_table.row_data = self.database.get_products()



if __name__ == '__main__':
    app = MainApp()
    app.run()