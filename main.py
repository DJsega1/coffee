import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget, QApplication
from PyQt5 import uic


class Edit(QWidget):
    def __init__(self, conn, parent, id=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.id = id
        self.parent = parent
        self.pushButton.clicked.connect(self.submit)
        self.connection = conn

    def submit(self):
        if self.id is None:
            self.connection.cursor().execute(
                '''INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (None,
                 self.lineEdit_2.text(),
                 self.lineEdit_3.text(),
                 self.lineEdit_4.text(),
                 self.lineEdit_5.text(),
                 self.lineEdit_6.text(),
                 self.lineEdit_7.text())
            )
        else:
            self.connection.cursor().execute(
                '''UPDATE coffee SET id = ?,
                 sort_name = ?, degree_of_roasting = ?, ground_beans = ?, taste_description = ?,
                  cost = ?, packing_volume = ? WHERE id = ?''',
                (self.id,
                 self.lineEdit_2.text(),
                 self.lineEdit_3.text(),
                 self.lineEdit_4.text(),
                 self.lineEdit_5.text(),
                 self.lineEdit_6.text(),
                 self.lineEdit_7.text(),
                 self.id)
            )
        self.connection.commit()
        self.parent.select_data()
        self.close()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.add_data)
        self.pushButton_2.clicked.connect(self.edit_data)
        self.tableWidget.itemSelectionChanged.connect(self.on_selection)
        self.form = None
        self.select_data()

    def on_selection(self):
        item = self.tableWidget.selectedItems()
        if item:
            self.tableWidget.selectRow(item[0].row())
            self.pushButton_2.setEnabled(True)
        else:
            self.pushButton_2.setEnabled(False)

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

    def add_data(self):
        self.form = Edit(self.connection, self)
        self.form.setWindowTitle("Add")
        self.form.show()

    def edit_data(self):
        self.form = Edit(self.connection, self, id=self.tableWidget.currentRow() + 1)
        self.form.setWindowTitle("Edit")
        self.form.show()


def closeEvent(self, event):
    self.connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
