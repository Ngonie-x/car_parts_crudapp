from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.picker import MDDatePicker
from db import Database


class MainApp(MDApp):
    def build(self):
        # set the theme color
        self.theme_cls.primary_palette = "DeepPurple"

        # row id to keep track of the id that have been selected
        self.row_ids = []

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
        self.data_table.bind(on_check_press=self.on_check_press)
        self.root.ids['datatable'].add_widget(self.data_table)

    # data table
    def on_check_press(self, instance_table, current_row):
        '''Called when the checkbox in the data table is clicked'''
        print(current_row)
        self.row_ids.append(current_row[0])
        self.root.ids['description_field'].text = current_row[1]
        self.root.ids['price_field'].text = current_row[2]
        self.root.ids['date_field'].text = current_row[3]

   # Date picker
    def on_start(self):
       '''Called when the program is started'''
       self.reload_data_table()

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
        id_check = self.root.ids['id_check']

        if id_check.active == True:
            try:
                self.data_table.row_data = self.database.get_product_by_id(int(self.root.ids['search'].text))
            except:
                pass
        else:
            self.data_table.row_data = self.database.get_products_by_description(str(self.root.ids['search'].text))

    
    # Database Operations
    def insert_data(self):
        """Insert data into the database"""
        description = self.root.ids['description_field'].text
        price = self.root.ids['price_field'].text
        date = self.root.ids['date_field'].text

        self.database.create_entry(description, price, date)
        self.reload_data_table()
        self.clear_text_entries()

        
    def update_data(self):
        '''Update the data in the database for the given primary key'''
        description = self.root.ids['description_field'].text
        price = self.root.ids['price_field'].text
        date = self.root.ids['date_field'].text
        if self.row_ids != []:
            self.database.update_product(self.row_ids[-1], description, price, date)
            self.reload_data_table()
        
        self.row_ids = []
        self.clear_text_entries()


    def delete_data(self):
        '''Delete data with the given id'''
        if self.row_ids != []:
            for id in self.row_ids:
                self.database.delete_product(id)

            self.reload_data_table()
            self.row_ids = []
            self.clear_text_entries()   

        else:
            print("Select rows first!")

    def reload_data_table(self):
        '''Reload the datatable after an action e.g update, delete or insert'''
        self.data_table.row_data = self.database.get_products()

    def clear_text_entries(self):
        '''Clears the text entries after an action'''
        self.root.ids['description_field'].text = ''
        self.root.ids['price_field'].text = ''
        self.root.ids['date_field'].text = ''



if __name__ == '__main__':
    app = MainApp()
    app.run()