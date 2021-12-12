from kivy.core.window import Window

# setting the window size
Window.size = (1000, 770)

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.picker import MDDatePicker
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import time

from db import Database


class ScreenManagement(ScreenManager):
    pass

class MainScreen(MDScreen):
    pass

class CameraScreen(MDScreen):
    def on_pre_enter(self):
        '''Start the camera when entering the screen'''
        self.camera = ProductCamera(size_hint=(1, .9))
        self.ids['cambox'].add_widget(self.camera)
        
        
    def on_pre_leave(self):
        '''Stop the camera when leaving the screen'''
        self.ids['cambox'].remove_widget(self.camera)
        self.camera.stop_camera()
        
    def capture(self):
        '''Capture the image'''
        return self.camera.capture_img()
        
        

class ProductCamera(Image):
    '''Class to capture product images'''
    def __init__(self, **kwargs):
        super(ProductCamera, self).__init__(**kwargs)

        # connect to the 0th camera
        self.record = cv2.VideoCapture(0)

        # set the drawing interval
        Clock.schedule_interval(self.update, 0.01)

    def update(self, dt):
        # load frame
        ret, self.frame = self.record.read()
        # convert to kivy texture
        buf = cv2.flip(self.frame, 0).tobytes()
        texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt="bgr", bufferfmt='ubyte')

        # change the texture of the instance
        self.texture = texture
    
    def stop_camera(self):
        '''Stop the camera'''
        self.record.release()
        Clock.unschedule(self.update)
        
    def capture_img(self):
        '''Capture the image'''
        timestr = time.strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f'./images/img_{timestr}.png', self.frame)
        return f'./images/img_{timestr}.png'
        

class MeasurementConfirm(OneLineAvatarIconListItem):
    '''Class to confirm the measurement unit'''
    divider = None
    
    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class CategoryConfirm(OneLineAvatarIconListItem):
    '''Class to confirm the category'''
    divider = None
    
    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
    

class MainApp(MDApp):
    dialog = None
    
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.root.transition= CardTransition()
        #create the database and connect
        self.database = Database()

        # create the data table
        self.create_datatable()
    
    # Date picker
    def on_start(self):
       '''Called when the program is started'''
       self.reload_data_table()
       
    def go_to_cam_screen(self):
        '''Switch to the camera screen'''
        self.root.current = 'camerascreen'

    def return_to_main(self):
        '''Switch to the main screen'''
        self.root.current = 'mainscreen'
        
    ################# Dialogs ######################################
    def show_measurement_dialog(self):
        '''Show the measurement dialog'''
        if not self.dialog:
            self.dialog = MDDialog(
                title='Select Measurement',
                type='confirmation',
                items = [
                    MeasurementConfirm(text="Kilograms"),
                    MeasurementConfirm(text="Meters"),
                    MeasurementConfirm(text="Centimeters"),
                    MeasurementConfirm(text="Units"),
                    
                ],
                buttons = [
                    MDFlatButton(
                        text = 'CANCEL',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.primary_color,
                        on_release=self.cancel_dialog
                    ),
                    MDFlatButton(
                        text = 'OK',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.primary_color,
                        on_release=self.get_measurement_val
                    ),
                ]
            )
        self.dialog.open()
        
    def show_category_dialog(self):
        '''Show the category dialog box'''
        if not self.dialog:
            self.dialog = MDDialog(
                title='Select Measurement',
                type='confirmation',
                items = [
                    CategoryConfirm(text="Fruits"),
                    CategoryConfirm(text="Vegetables"),
                ],
                buttons = [
                    MDFlatButton(
                        text = 'CANCEL',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.primary_color,
                        on_release=self.cancel_dialog
                    ),
                    MDFlatButton(
                        text = 'OK',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.primary_color,
                        on_release=self.get_category_val
                    ),
                ]
            )
        self.dialog.open()
        
    def get_measurement_val(self, inst):
        '''Get the value of the checked item in the measurement dialog'''
        for item in self.dialog.items:
            if item.ids.check.active == True:
                self.root.screens[0].ids['measurement_lbl'].text = item.text
        self.dialog.dismiss()
        self.dialog = None
                
    def get_category_val(self, inst):
        '''Get the value of the checked item in the category dialog'''
        for item in self.dialog.items:
            if item.ids.check.active == True:
                self.root.screens[0].ids['category_lbl'].text = item.text
        self.dialog.dismiss()
        self.dialog = None
        
    
    def cancel_dialog(self, inst):
        self.dialog.dismiss()
        
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="An application is using products.pdf. Please close it to proceed.",
                radius=[20, 7, 20, 7],
            )
        self.dialog.open()
        
    ################### End Dialogs ##########################
    
    ###################Start Database Logic #################
        
    def create_datatable(self):
        # data table
        self.data_table = MDDataTable(
            size_hint=(1, 1),
            use_pagination= True,
            check=True,
            column_data=[
                ("Id", dp(20)),
                ("Description", dp(30)),
                ("Price", dp(25)),
                ("Date", dp(25)),
                ("Measure", dp(25)),
                ("Category", dp(25)),
                ("Track?", dp(25)),
            ],
            row_data = [],
        )
        self.data_table.bind(on_check_press=self.on_check_press)
        self.root.screens[0].ids['datatable'].add_widget(self.data_table)

    
    def remove_datatable(self):
        self.root.screens[0].ids['datatable'].remove_widget(self.data_table)


    # Search
    def search(self):
        '''Search values in the database'''
        id_check = self.root.screens[0].ids['id_check']

        if id_check.active == True:
            try:
                self.data_table.row_data = self.database.get_product_by_id(int(self.root.screens[0].ids['search'].text))
            except:
                pass
        else:
            self.data_table.row_data = self.database.get_products_by_description(str(self.root.screens[0].ids['search'].text))

    
    # Database Operations
    def insert_data(self):
        """Insert data into the database"""
        description = self.root.screens[0].ids['description_field'].text
        price = self.root.screens[0].ids['price_field'].text
        date = self.root.screens[0].ids['date_field'].text
        measure = self.root.screens[0].ids['measurement_lbl'].text
        category = self.root.screens[0].ids['category_lbl'].text
        track = 0 if self.root.screens[0].ids['track_check'].active else 1
        picture = self.root.screens[0].ids['product_label'].text
        
        

        self.database.create_entry(description, price, date, measure, category, track, picture)
        self.reload_data_table()
        self.clear_text_entries()

        
    def update_data(self):
        '''Update the data in the database for the given primary key'''
        description = self.root.screens[0].ids['description_field'].text
        price = self.root.screens[0].ids['price_field'].text
        date = self.root.screens[0].ids['date_field'].text
        measure = self.root.screens[0].ids['measurement_lbl'].text
        category = self.root.screens[0].ids['category_lbl'].text
        track = 0 if self.root.screens[0].ids['track_check'].active else 1
        picture = self.root.screens[0].ids['product_label'].text
        id = self.data_table.get_row_checks()[0][0]
        
        self.database.update_product(id, description, price, date, measure, category, track, picture)
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
            
    def export_to_pdf(self):
        '''Export data to pdf'''
        try:
            self.database.export_data_to_pdf()
        except PermissionError:
            self.show_alert_dialog()
            
    
    def get_image_name(self, img_name):
        '''Get the name of the image of the photo taken and set source and label'''
        self.root.screens[0].ids['product_img'].source = img_name
        self.root.screens[0].ids['product_label'].text = img_name


    ############# End database Logic #######################
    
    
    ############# Start datatable logic #############################

    # data table
    def on_check_press(self, instance_table, current_row):
        '''Called when the checkbox in the data table is clicked'''
        self.root.screens[0].ids['description_field'].text = current_row[1]
        self.root.screens[0].ids['price_field'].text = current_row[2]
        self.root.screens[0].ids['date_field'].text = current_row[3]
        self.root.screens[0].ids['measurement_lbl'].text = current_row[4]
        self.root.screens[0].ids['category_lbl'].text = current_row[5]
        print(current_row[0])
        img_path = self.database.get_product_picture(int(current_row[0]))
        print(img_path)
        self.root.screens[0].ids['product_img'].source = img_path
        self.root.screens[0].ids['product_label'].text = img_path
        self.root.screens[0].ids['track_check'].active = True if current_row[6] == '1' else False
        
        
        self.enable_or_disable_insert_btn()
        self.enable_or_disable_update_delete_btns()
        

    def enable_or_disable_insert_btn(self):
        '''Enable or disable the insert button'''
        if self.data_table.get_row_checks() != []:
            self.root.screens[0].ids['insertbtn'].disabled = True
        else:
            self.root.screens[0].ids['insertbtn'].disabled = False

    def enable_or_disable_update_delete_btns(self):
        '''Enable or disable the update and the delete buttons'''
        row_ids = self.data_table.get_row_checks()
        if row_ids != []:
            if len(row_ids) == 1:
                self.root.screens[0].ids['updatebtn'].disabled = False
                self.root.screens[0].ids['deletebtn'].disabled = False
            elif len(row_ids)>1:
                self.root.screens[0].ids['updatebtn'].disabled = True
                self.root.screens[0].ids['deletebtn'].disabled = False
            else:
                self.root.screens[0].ids['updatebtn'].disabled = True
                self.root.screens[0].ids['deletebtn'].disabled = True

        else:
            self.root.screens[0].ids['updatebtn'].disabled = True
            self.root.screens[0].ids['deletebtn'].disabled = True
            self.clear_text_entries()
            
    def reload_data_table(self):
        '''Reload the datatable after an action e.g update, delete or insert'''
        self.remove_datatable()
        self.create_datatable()
        self.data_table.row_data = self.database.get_products()

    def clear_text_entries(self):
        '''Clears the text entries after an action'''
        self.root.screens[0].ids['description_field'].text = ''
        self.root.screens[0].ids['price_field'].text = ''
        self.root.screens[0].ids['date_field'].text = ''


    def cancel(self):
        '''Clear text entries, reload data table, restores everything to default'''
        self.reload_data_table()
        self.clear_text_entries()
        self.enable_or_disable_insert_btn()
        self.enable_or_disable_update_delete_btns()
            
    
    ######################## End datatable logic ###############################
       
       
    ############ Date picker logic #####################     
    def on_save(self, instance, value, date_range):
        '''Called when we select a date from the datetime picker'''
        self.root.screens[0].ids['date_field'].text = str(value)
        print(value)


    def show_date_picker(self):
        '''Show the datepicker'''
        self.root.screens[0].ids['date_field'].focus = False
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    ########### End date picker logic ########################

    
    

    

    
        
    
        
    
    
        

if __name__ == "__main__":
    app = MainApp()
    app.run()