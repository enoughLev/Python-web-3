import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

from forms.form_2_ui import Ui_MainWindow


def show_status_message(text):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("Статус операции")
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.setModal(False)
    msg_box.exec()


class FileCreator(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.path = ""
        self.text = []
        self.file_name = ""

        self.create_btn.clicked.connect(self.on_create_click)
        self.open_btn.clicked.connect(self.on_open_click)
        self.save_btn.clicked.connect(self.on_save_click)

    def on_create_click(self):
        self.path = QFileDialog.getSaveFileName(self, 'Создание файла', '', 'Текстовый файл (*.txt)')
        if len(self.path[0]) != 0:
            with open(self.path[0], "w") as file:
                file.close()
            self.plain_panel.setPlainText('')

    def on_open_click(self):
        self.path = QFileDialog.getOpenFileName(self, 'Выбор файла', '', 'Текстовый файл (*.txt)')
        if len(self.path[0]) != 0:
            with open(self.path[0], "r") as file:
                text = file.read()
                self.path_label.setText(self.path[0])
                self.plain_panel.setPlainText(text)

    def on_save_click(self):
        if len(self.path[0]) != 0:
            with open(self.path[0], "w") as file:
                file.write(self.plain_panel.toPlainText())
                file.close()
            show_status_message("Файл успешно сохранен")
        else:
            show_status_message("Ошибка с сохранением файла!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileCreator()
    ex.show()
    sys.exit(app.exec())
