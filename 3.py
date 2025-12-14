import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QMessageBox)
from PyQt6.QtGui import QPixmap, QImage, QTransform
from PyQt6.QtCore import Qt
from forms.form_3_ui import Ui_MainWindow


class ImageProcessor(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.original_image = None
        self.current_image = None
        self.angle = 0
        self.current_channel = 'RGB'

        self.btn_open.clicked.connect(self.open_image)
        self.btn_rotate_left.clicked.connect(self.rotate_left)
        self.btn_rotate_right.clicked.connect(self.rotate_right)
        self.btn_remove_red.clicked.connect(self.remove_red_channel)

        self.label_image.setMinimumSize(400, 400)
        self.label_image.setStyleSheet("border: 2px solid #ccc; border-radius: 5px;")
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setScaledContents(True)


    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Открыть картинку", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )

        if file_path:
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение!")
                return


            self.original_image = pixmap.toImage()
            self.current_image = self.original_image.copy()
            self.angle = 0
            self.current_channel = 'RGB'
            self.update_display()


    def rotate_left(self):
        if self.current_image:
            self.angle -= 90
            self.update_display()


    def rotate_right(self):
        if self.current_image:
            self.angle += 90
            self.update_display()


    def remove_red_channel(self):
        if not self.current_image or self.current_image.isNull():
            return

        if self.current_image.format() != QImage.Format.Format_RGB888:
            self.current_image = self.current_image.convertToFormat(QImage.Format.Format_RGB888)

        width = self.current_image.width()
        height = self.current_image.height()

        new_image = QImage(width, height, QImage.Format.Format_RGB888)

        for y in range(height):
            for x in range(width):
                color = self.current_image.pixelColor(x, y)
                new_color = color
                new_color.setRed(0)
                new_image.setPixelColor(x, y, new_color)

        self.current_image = new_image
        self.current_channel = 'GB'
        self.update_display()


    def update_display(self):
        if not self.current_image or self.current_image.isNull():
            return

        pixmap = QPixmap.fromImage(self.current_image)

        transform = QTransform()
        transform.rotate(self.angle)
        pixmap = pixmap.transformed(transform)
        scaled_pixmap = pixmap.scaled(
            self.label_image.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.label_image.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec())
