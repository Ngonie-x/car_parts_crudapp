from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"

        # data table
        self.data_table = MDDataTable(
            size_hint=(0.9, 0.53),
            use_pagination= True,
            # check=True,
            # pos_hint={'center_x': .5, 'y':.05},
            column_data=[
                ("Id", dp(10)),
                ("Descrition", dp(70)),
                ("Price", dp(30)),
                ("Date", dp(30)),
            ],
        )

        self.root.ids['datatable'].add_widget(self.data_table)
    

if __name__ == '__main__':
    app = MainApp()
    app.run()