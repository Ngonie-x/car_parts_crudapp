import subprocess
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class ExtractToPdf:
    def __init__(self, data):
        self.data = [list(i) for i in data]
        self.data.insert(0, ['Id', 'Description', 'Price', 'Date', 'Measure', 'Category', 'Track?', 'Image_Path'])
        self.doc = SimpleDocTemplate('products.pdf', pagesize=letter)
        self.elements = []
        self.create_table()

    def create_table(self):
        t = Table(self.data)
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.green),('TEXTCOLOR',(0,0),(-1,0),colors.red),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ]))
        self.elements.append(t)

        # write the document to disk
        self.doc.build(self.elements)
        self.open_pdf()

    def open_pdf(self):
        subprocess.Popen(['start', 'products.pdf'], shell=True)