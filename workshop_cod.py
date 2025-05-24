import sys
import MySQLdb
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication,QMainWindow,QMessageBox,QListWidgetItem
from workshop import Ui_workshop

conn = MySQLdb.connect("localhost","root","root","furniture")
cursor = conn.cursor()

class WorkshopWin(QMainWindow):
    def __init__(self, main_window):
        super().__init__()

        self.ui = Ui_workshop()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.ui.pushButton_back_worlshop.clicked.connect(self.back)
        self.load_workshop()
        self.ui.comboBox_products_workshop.currentIndexChanged.connect(self.filter_name)
        self.load_work()

    def filter_name(self):
        workshop_id = self.ui.comboBox_products_workshop.currentData()
        if workshop_id is None:
            self.load_work()
            return
        self.ui.listWidget_workshop.clear()
        cursor.execute("""select Products_Workshop.id, Products_Workshop.time_minutes, Workshop.name, Products.name,Workshop.workers_count
        from Products_Workshop
        join Products on Products_Workshop.product_id = Products.id
        join Workshop on Products_Workshop.workshop_id = Workshop.id
        where Workshop.id = %s""",(workshop_id, ))
        workshops = cursor.fetchall()

        for workshop in workshops:
            (products_id, products_time, workshop_name, products_name,workshop_workers) = workshop

            item_text = (
                f"Время изготовления: {products_time}\n"
                f"Название продукта: {products_name}\n"
                f"Кол-во рабочих: {workshop_workers}\n"
                "----------------------------------------"
            )
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, products_id)
            self.ui.listWidget_workshop.addItem(item)
    def load_work(self):
        try:
            self.ui.listWidget_workshop.clear()
            cursor.execute("""select Products_Workshop.id, Products_Workshop.time_minutes, Workshop.name, Products.name,Workshop.workers_count
            from Products_Workshop
            join Products on Products_Workshop.product_id = Products.id
            join Workshop on Products_Workshop.workshop_id = Workshop.id""")
            workshops = cursor.fetchall()

            for workshop in workshops:
                (products_id, products_time, workshop_name, products_name, workshop_workers) = workshop

                item_text = (
                    f"Время изготовления: {products_time}\n"
                    f"Название продукта: {products_name}\n"
                    f"Кол-во рабочих: {workshop_workers}\n"
                    "----------------------------------------"
                )
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, products_id)
                self.ui.listWidget_workshop.addItem(item)
        except Exception as e:
            QMessageBox.critical(self,"ошибка",f"ошибка: {e}")




    def load_workshop(self):
        self.ui.comboBox_products_workshop.addItem("все",None)
        cursor.execute("""select id, name from Workshop""")
        workshops = cursor.fetchall()
        for workshop in workshops:
            self.ui.comboBox_products_workshop.addItem(workshop[1],workshop[0])

    def back(self):
        self.close()
        self.main_window.show()

