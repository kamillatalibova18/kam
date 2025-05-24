import sys
import MySQLdb
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication,QMainWindow,QMessageBox,QListWidgetItem
from change_pr import Ui_change_product
conn = MySQLdb.connect("localhost","root","root","furniture")
cursor = conn.cursor()

class ChangeWin(QMainWindow):
    def __init__(self, main_window, products_data):
        super().__init__()

        self.ui = Ui_change_product()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.products_data = products_data
        self.products_id = products_data["products_id"]
        self.load_model()
        self.load_material()
        self.load_typee()
        self.ui.lineEdit_name_furniture.setText(products_data["products_name"])
        self.ui.lineEdit_article.setText(str(products_data["article"]))
        self.ui.lineEdit_description.setText(products_data["description"])
        self.ui.lineEdit_min_price.setText(str(products_data["products_price"]))
        index1 = self.ui.comboBox_material.findText(products_data["material"])
        self.ui.comboBox_material.setCurrentIndex(index1)
        index2 = self.ui.comboBox_model.findText(products_data["models"])
        self.ui.comboBox_model.setCurrentIndex(index2)
        index3 = self.ui.comboBox_type_product.findText(products_data["typee"])
        self.ui.comboBox_type_product.setCurrentIndex(index3)
        self.ui.pushButton_change_products.clicked.connect(self.change)

    def change(self):
        try:
            name = self.ui.lineEdit_name_furniture.text()
            price = self.ui.lineEdit_min_price.text()
            article = self.ui.lineEdit_article.text()
            description = self.ui.lineEdit_description.text()
            material = self.ui.comboBox_material.currentData()
            model = self.ui.comboBox_model.currentData()
            typee = self.ui.comboBox_type_product.currentData()
            cursor.execute("""update Products set name = %s, min_partner_price = %s, article = %s, description = %s, id_material = %s,id_model = %s, id_type_product = %s
            where Products.id = %s""",(name,price,article,description,material,model,typee, self.products_id))
            conn.commit()
            QMessageBox.information(self,"Успех","ВААУ")
        except Exception as e:
            QMessageBox(self,"ошибка",f"ошибааа: {e}")



    def load_typee(self):
        self.ui.comboBox_type_product.addItem("все", None)
        cursor.execute("""select id, name from Products_type""")
        types = cursor.fetchall()
        for typee in types:
            self.ui.comboBox_type_product.addItem(typee[1], typee[0])

    def load_material(self):
        self.ui.comboBox_material.addItem("все", None)
        cursor.execute("""select id, name from Material""")
        materials = cursor.fetchall()
        for material in materials:
            self.ui.comboBox_material.addItem(material[1], material[0])

    def load_model(self):
        self.ui.comboBox_model.addItem("все", None)
        cursor.execute("""select id, name from Models""")
        models = cursor.fetchall()
        for model in models:
            self.ui.comboBox_model.addItem(model[1], model[0])

