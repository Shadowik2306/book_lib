import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from interface_main import Ui_MainWindow
from info import Ui_MainInfo
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.find)

    def find(self):
        if self.comboBox.currentText() == 'Название':
            key = 'Name'
        else:
            key = 'Author'
        con = sqlite3.connect('base.db')
        cur = con.cursor()
        self.dct_of_buttons = {}
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1)
        self.tableWidget.setHorizontalHeaderLabels(['Вывод'])
        for find in cur.execute(f'SELECT * FROM Lib WHERE {key} LIKE'
                                f' "%{self.lineEdit.text()}%"').fetchall():
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            but = QPushButton(find[0])
            self.dct_of_buttons[but] = find
            but.clicked.connect(self.give_info)
            self.tableWidget.setCellWidget(0, self.tableWidget.rowCount() - 1, but)

    def give_info(self):
        self.wid = InfoWind(self.sender(), self.dct_of_buttons)
        self.wid.show()


class InfoWind(QMainWindow, Ui_MainInfo):
    def __init__(self, sender, dct):
        super().__init__()
        self.setupUi(self)
        self.inf = dct[sender]
        self.start()

    def start(self):
        img = QPixmap(self.inf[4])
        self.label.setPixmap(img)
        self.name.setText(self.inf[0])
        self.author.setText(self.inf[1])
        self.birthyear.setText(str(self.inf[2]))
        self.genre.setText(self.inf[3])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec())
