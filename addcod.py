import sys
import MySQLdb
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication,QMainWindow,QMessageBox,QListWidgetItem
from add_products import AddForm

conn = MySQLdb.connect("localhost","root","root","furniture")
cursor = conn.cursor()

class AddWin(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.ui = AddForm()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.ui.pushButton_back_add_produc.clicked.connect(self.back)
        self.ui.pushButton_add_products.clicked.connect(self.add_products)
        self.load_model()
        self.load_material()
        self.load_typee()
        self.update_list()

    def load_typee(self):
        self.ui.comboBox_type_product.addItem("все",None)
        cursor.execute("""select id, name from Products_type""")
        types = cursor.fetchall()
        for typee in types:
            self.ui.comboBox_type_product.addItem(typee[1],typee[0])

    def load_material(self):
        self.ui.comboBox_material.addItem("все",None)
        cursor.execute("""select id, name from Material""")
        materials = cursor.fetchall()
        for material in materials:
            self.ui.comboBox_material.addItem(material[1],material[0])


    def load_model(self):
        self.ui.comboBox_model.addItem("все",None)
        cursor.execute("""select id, name from Models""")
        models = cursor.fetchall()
        for model in models:
            self.ui.comboBox_model.addItem(model[1],model[0])

    def add_products(self):
        try:
            name = self.ui.lineEdit_name_furniture.text()
            price = self.ui.lineEdit_min_price.text()
            article = self.ui.lineEdit_article.text()
            description = self.ui.lineEdit_description.text()
            material = self.ui.comboBox_material.currentData()
            model = self.ui.comboBox_model.currentData()
            typee = self.ui.comboBox_type_product.currentData()

            if not name or not price or not article or not description or not material or not model or not typee:
                QMessageBox.warning(self, "Ошибка", "Заполните все поля")
                return

            cursor.execute("""insert into Products(name, min_partner_price, article, description, id_material,id_model,id_type_product)
                        values(%s,%s,%s,%s,%s,%s, %s)""", (name, price, article, description, material, model, typee))
            self.update_list()
            QMessageBox.information(self,"Успех","Данные успешно добавлены")
        except Exception as e:
            QMessageBox.critical(self,"ОШИБКА",f"ошибка: {e}")

    def update_list(self):
        try:
            self.main_window.ui.listWidget.clear()
            cursor.execute("""SELECT Products.id,Products.name,Products.min_partner_price,Products.article,Products.description,
            Products.time, Models.name, Material.name, Products_type.name
            from Products
            JOIN Models on Products.id_model = Models.id
            join Material on Products.id_material = Material.id
            join Products_type on Products.id_type_product = Products_type.id""")
            products = cursor.fetchall()
            conn.commit()

            for product in products:
                (products_id, products_name, products_price, products_article, description, timee,models_name, material,typee) = product

                item_text = (
                    f"Тип: {typee} | Наименование: {products_name}\n"
                    f"Материал: {material}\n"
                    f"Артикул: {products_article}\n"
                    f"Цена: {products_price}\n"
                    f"Описание: {description}\n"
                    f"Модель; {models_name}\n"
                    "-----------------------------------------------------------"
                )
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, products_id)
                self.main_window.ui.listWidget.addItem(item)
        except Exception as e:
            QMessageBox.critical(self,"ошибка",f"ошибка: {e}")


    def back(self):
        self.close()
        self.main_window.show()

