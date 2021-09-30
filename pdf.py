from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class ExtractToPdf:
    def __init__(self, data):
        self.data = [list(i) for i in data]
        self.data.insert(0, ['Id', 'Description', 'Price', 'Date'])
        self.doc = SimpleDocTemplate('products.pdf', pagesize=letter)
        self.elements = []
        self.create_table()

    def create_table(self):
        t = Table(self.data)
        t.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.green),('TEXTCOLOR',(0,0),(1,-1),colors.red)]))
        self.elements.append(t)
        # write the document to disk
        self.doc.build(self.elements)