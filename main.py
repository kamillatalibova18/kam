import sys
import MySQLdb
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication,QMainWindow,QMessageBox,QListWidgetItem
from products import Products
from addcod import AddWin
from workshop_cod import WorkshopWin
from change_cod import ChangeWin
conn = MySQLdb.connect("localhost","root","root","furniture")
cursor = conn.cursor()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Products()
        self.ui.setupUi(self)
        self.load_products()
        self.ui.pushButton.clicked.connect(self.add)
        self.ui.pushButton_2.clicked.connect(self.open_work)
        self.ui.listWidget.itemClicked.connect(self.on_item_click)

    def on_item_click(self,item):
        products_id = item.data(Qt.ItemDataRole.UserRole)
        products_data = self.get_clicked_data(products_id)
        if products_data:
            self.open_change = ChangeWin(self,products_data)
            self.open_change.show()
        else:
            QMessageBox.information(self,"Ошибка","ошибкаа")

    def get_clicked_data(self, products_id):
        cursor.execute("""SELECT Products.id,Products.name,Products.min_partner_price,Products.article,Products.description,
            Products.time, Models.name, Material.name, Products_type.name
            from Products
            JOIN Models on Products.id_model = Models.id
            join Material on Products.id_material = Material.id
            join Products_type on Products.id_type_product = Products_type.id
            where Products.id = %s""",(products_id, ))
        products = cursor.fetchone()
        conn.commit()
        return {
            "products_id": products[0],
            "products_name": products[1],
            "products_price": products[2],
            "article": products[3],
            "description": products[4],
            "models": products[6],
            "material": products[7],
            "typee": products[8]
        }




    def open_work(self):
        self.close()
        self.open_work = WorkshopWin(self)
        self.open_work.show()

    def add(self):
        self.close()
        self.open_add = AddWin(self)
        self.open_add.show()

    def load_products(self):
        try:
            self.ui.listWidget.clear()
            cursor.execute("""SELECT Products.id,Products.name,Products.min_partner_price,Products.article,Products.description,
            Products.time, Models.name, Material.name, Products_type.name
            from Products
            JOIN Models on Products.id_model = Models.id
            join Material on Products.id_material = Material.id
            join Products_type on Products.id_type_product = Products_type.id""")
            products = cursor.fetchall()
            conn.commit()

            for product in products:
                (products_id, products_name, products_price, products_article, description, timee,models_name, material, typee) = product

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
                self.ui.listWidget.addItem(item)
        except Exception as e:
            QMessageBox.critical(self,"ошибка",f"ошибка: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())