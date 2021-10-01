from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dialog import MDDialog
from db import Database



class MainApp(MDApp):
    dialog = None

    def build(self):
        # set the theme color
        self.theme_cls.primary_palette = "DeepPurple"

        #create the database and connect
        self.database = Database()

        # create the data table
        self.create_datatable()

    def create_datatable(self):
        # data table
        self.data_table = MDDataTable(
            size_hint=(1, 0.53),
            use_pagination= True,
            check=True,
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

    
    def remove_datatable(self):
        self.root.ids['datatable'].remove_widget(self.data_table)

    # data table
    def on_check_press(self, instance_table, current_row):
        '''Called when the checkbox in the data table is clicked'''
        self.root.ids['description_field'].text = current_row[1]
        self.root.ids['price_field'].text = current_row[2]
        self.root.ids['date_field'].text = current_row[3]
        self.enable_or_disable_insert_btn()
        self.enable_or_disable_update_delete_btns()
        

    def enable_or_disable_insert_btn(self):
        '''Enable or disable the insert button'''
        if self.data_table.get_row_checks() != []:
            self.root.ids['insertbtn'].disabled = True
        else:
            self.root.ids['insertbtn'].disabled = False

    def enable_or_disable_update_delete_btns(self):
        '''Enable or disable the update and the delete buttons'''
        row_ids = self.data_table.get_row_checks()
        if row_ids != []:
            if len(row_ids) == 1:
                self.root.ids['updatebtn'].disabled = False
                self.root.ids['deletebtn'].disabled = False
            elif len(row_ids)>1:
                self.root.ids['updatebtn'].disabled = True
                self.root.ids['deletebtn'].disabled = False
            else:
                self.root.ids['updatebtn'].disabled = True
                self.root.ids['deletebtn'].disabled = True

        else:
            self.root.ids['updatebtn'].disabled = True
            self.root.ids['deletebtn'].disabled = True
            self.clear_text_entries()

            

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
        id = self.data_table.get_row_checks()[0][0]
        
        self.database.update_product(id, description, price, date)
        self.reload_data_table()
        
        self.clear_text_entries()




    def delete_data(self):
        '''Delete data with the given id'''
        row_ids = [i[0] for i in self.data_table.get_row_checks()]
        if row_ids != []:
            for id in row_ids:
                self.database.delete_product(id)

            self.reload_data_table()
            self.clear_text_entries()   
        else:
            print("Select rows first!")

    def reload_data_table(self):
        '''Reload the datatable after an action e.g update, delete or insert'''
        self.remove_datatable()
        self.create_datatable()
        self.data_table.row_data = self.database.get_products()

    def clear_text_entries(self):
        '''Clears the text entries after an action'''
        self.root.ids['description_field'].text = ''
        self.root.ids['price_field'].text = ''
        self.root.ids['date_field'].text = ''


    def cancel(self):
        '''Clear text entries, reload data table, restores everything to default'''
        self.reload_data_table()
        self.clear_text_entries()
        self.enable_or_disable_insert_btn()
        self.enable_or_disable_update_delete_btns()

    def export_to_pdf(self):
        '''Export data to pdf'''
        try:
            self.database.export_data_to_pdf()
        except PermissionError:
            self.show_alert_dialog()

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="An application is using products.pdf. Please close it to proceed.",
                radius=[20, 7, 20, 7],
            )
        self.dialog.open()

if __name__ == '__main__':
    app = MainApp()
    app.run()