import sys
import MySQLdb
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem

from products import Products
from addcod import AddWin

conn = MySQLdb.connect("localhost","root","root","furniture")
cursor = conn.cursor()

#класс запуска главной формы
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Products()
        self.ui.setupUi(self)
        #ссылка на функцию вывода информации на главном экране
        self.load_products()
        self.ui.pushButton.clicked.connect(self.open_add)

    def open_add(self):
        self.close()
        self.add_window = AddWin(self)
        self.add_window.show()


    #функция вывода в лист виджет
    def load_products(self):
        try:
            self.ui.listWidget.clear()
            cursor.execute("""SELECT Products.id, Products.name,Products.min_partner_price,Products.article,Products.description,
            Products.time, Material.name,Models.name,Products_type.name
            from Products
            join Models on Products.id_model = Models.id
            JOIN Material on Products.id_material = Material.id
            JOIN Products_type on Products.id_type_product = Products_type.id""")
            products = cursor.fetchall()
            conn.commit()

            for product in products:
                (product_id,product_name, product_min, product_article, product_description,
                 product_time, material_name, model_name,product_type) = product

            item_text = (
                f"Тип: {product_type} | Наименование: {product_name}\n"
                f"Артикул: {product_article}\n"
                f"Минимальная цена: {product_min}\n"
                f"Материал: {material_name}\n"
                "--------------------------------------------------------------"
            )

            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, product_id)
            self.ui.listWidget.addItem(item)

        except Exception as e:
            QMessageBox.critical(self,"Ошибка",f"Произошла ошибка: {e}")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
