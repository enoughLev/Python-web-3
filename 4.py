import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
from forms.form_4_ui import Ui_MainWindow


class TransparencyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.original_pixmap = None
        self.current_alpha = 100

        self.btn_open.clicked.connect(self.open_image)
        self.slider_alpha.valueChanged.connect(self.update_transparency)
        self.btn_reset.clicked.connect(self.reset_transparency)


    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть изображение", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.original_pixmap = QPixmap(file_path)
            if not self.original_pixmap.isNull():
                self.current_alpha = 100
                self.slider_alpha.setValue(100)
                self.update_transparency()


    def update_transparency(self):
        if not self.original_pixmap:
            return

        alpha_value = self.slider_alpha.value()
        self.current_alpha = alpha_value

        target_size = self.label_image.size()
        display_pixmap = QPixmap(target_size)
        display_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(display_pixmap)
        painter.setOpacity(alpha_value / 100.0)
        scaled_original = self.original_pixmap.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio,
                                                      Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled_original)
        painter.end()

        self.label_image.setPixmap(display_pixmap)


    def reset_transparency(self):
        self.slider_alpha.setValue(100)


    def save_image(self):
        if not self.original_pixmap:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить", "image.png", "PNG (*.png)")
        if file_path:
            image = self.original_pixmap.toImage()
            alpha = int(255 * self.current_alpha / 100)
            for y in range(image.height()):
                for x in range(image.width()):
                    color = image.pixelColor(x, y)
                    color.setAlpha(alpha)
                    image.setPixelColor(x, y, color)
            image.save(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparencyApp()
    window.show()
    sys.exit(app.exec())
