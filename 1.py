import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow

from statistics import median
from forms.form_1_ui import Ui_MainWindow


class FilePath(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.path = ""
        self.numbers = []
        self.choose_btn.clicked.connect(self.on_path_choose)
        self.save_btn.clicked.connect(self.save_file)
        self.save_label.setStyleSheet("color: green")
        self.save_label.setHidden(True)

    def is_number(self, num):
        try:
            int(num)
            return True
        except ValueError:
            print("INFO: File have to only contains integer numbers!")
            return False

    def on_path_choose(self):
        self.save_label.setHidden(True)
        self.path = QFileDialog.getOpenFileName(self, 'Выбор файл', '', 'Текстовый файл (*.txt)')
        if len(self.path[0]) != 0:
            self.path_label.setText(f"{self.path[0]}")
            if self.read_file():
                self.calc_data()
        else:
            print("INFO: Select correct path!")

    def read_file(self):
        with open(self.path[0], "r") as file:
            nums = file.read().split()
            if not all(self.is_number(num) for num in nums):
                return False
            self.numbers = [int(x) for x in nums]
            file.close()
        if not self.numbers:
            print("INFO: File is empty!")
            return False
        return True

    def calc_data(self):
        self.max_label.setText(f"{max(self.numbers)}")
        self.min_label.setText(f"{min(self.numbers)}")
        self.avg_label.setText(f"{median(self.numbers)}")

    def save_file(self):
        file_path = QFileDialog.getSaveFileName(self, 'Сохранение файла', '', 'Текстовый файл (*.txt)')
        if self.numbers:
            with open(file_path[0], "w") as file:
                file.write(
                    f"Max number: {max(self.numbers)} \nAverage number: {median(self.numbers)} \nMin number: {min(self.numbers)}")
                file.close()
            self.save_label.setHidden(False)
        else:
            print("INFO: Numbers is not defined!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FilePath()
    ex.show()
    sys.exit(app.exec())
