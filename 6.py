import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QColorDialog
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PyQt6.QtCore import Qt
from forms.form_6_ui import Ui_MainWindow


class SmileyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.smiley_color = QColor(255, 255, 0)
        self.current_pixmap = None

        self.btn_color.clicked.connect(self.choose_color)
        self.slider_scale.valueChanged.connect(self.update_scale)

        self.slider_scale.setMinimum(25)
        self.slider_scale.setMaximum(200)
        self.slider_scale.setValue(100)

        self.draw_smiley_base()
        self.update_scale()


    def choose_color(self):
        color = QColorDialog.getColor(self.smiley_color, self, "Выберите цвет смайлика")
        if color.isValid():
            self.smiley_color = color
            self.draw_smiley_base()
            self.update_scale()


    def draw_smiley_base(self):
        size = 400
        image = QImage(size, size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x, center_y = 200, 200
        radius = 160

        painter.setBrush(self.smiley_color)
        painter.setPen(QPen(QColor(0, 0, 0), 3))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(140, 160, 20, 20)
        painter.drawEllipse(240, 160, 20, 20)

        painter.setPen(QPen(QColor(0, 0, 0), 12))
        painter.setBrush(Qt.GlobalColor.transparent)
        painter.drawArc(160, 210, 80, 40, 0 * 16, -180 * 16)

        painter.end()
        self.current_pixmap = QPixmap.fromImage(image)


    def update_scale(self):
        if not self.current_pixmap:
            return

        scale = self.slider_scale.value() / 100.0
        scaled_size = self.current_pixmap.size() * scale

        display_pixmap = QPixmap(self.label_smiley.size())
        display_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(display_pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        scaled_pixmap = self.current_pixmap.scaled(
            scaled_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        x = (display_pixmap.width() - scaled_pixmap.width()) // 2
        y = (display_pixmap.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x, y, scaled_pixmap)

        painter.end()
        self.label_smiley.setPixmap(display_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmileyApp()
    window.show()
    sys.exit(app.exec())
