import sys
import MySQLdb
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem

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

    def back(self):
        self.close()
        self.main_window.show()
