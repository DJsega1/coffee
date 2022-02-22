import sqlite3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5 import uic


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.select_data()

    def select_data(self):
        res = self.connection.cursor().execute(
            "SELECT * FROM coffee").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название сорта", "Степень прожарки", "Молотый/в зернах",
             "Описание вкуса", "Цена", "Объём упаковки"])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row[-1])))


def closeEvent(self, event):
    self.connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
