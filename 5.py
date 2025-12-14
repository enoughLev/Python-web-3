import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox,
                             QInputDialog)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt6.QtCore import Qt
from forms.form_5_ui import Ui_MainWindow


class FlagGenerator(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.flag_pixmap = None

        self.btn_generate.clicked.connect(self.generate_flag)

    def generate_flag(self):
        num_colors, ok = QInputDialog.getInt(
            self, "Количество цветов", "Введите количество цветов флага (3-10):",
            3, 3, 10, 1
        )

        if not ok:
            return

        width = 400
        height = 300
        flag_image = QImage(width, height, QImage.Format.Format_RGB32)

        painter = QPainter(flag_image)
        painter.fillRect(flag_image.rect(), Qt.GlobalColor.white)

        stripe_height = height // num_colors

        for i in range(num_colors):
            hue = random.randint(0, 359)
            saturation = random.randint(70, 100)
            lightness = random.randint(50, 80)

            color = QColor.fromHsl(hue, saturation, lightness)
            painter.fillRect(0, i * stripe_height, width, stripe_height, color)

        painter.end()
        self.flag_pixmap = QPixmap.fromImage(flag_image)
        self.label_flag.setPixmap(self.flag_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlagGenerator()
    window.show()
    sys.exit(app.exec())
