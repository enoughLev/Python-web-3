import sys
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from forms.form_8_ui import Ui_MainWindow


class LSystemApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.axiom = ""
        self.rules = {}
        self.angle_div = 0

        self.btn_open.clicked.connect(self.open_lsystem_file)
        self.slider_iterations.valueChanged.connect(self.redraw)
        self.slider_scale.valueChanged.connect(self.redraw)

        self.slider_iterations.setRange(1, 50)
        self.slider_scale.setRange(50, 500)
        self.slider_iterations.setValue(3)
        self.slider_scale.setValue(300)  # x3 по умолчанию

        self.label_status.setText("Откройте файл L-системы")


    def open_lsystem_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть L-систему", "", "Text (*.txt)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = []
                    for line in f:
                        stripped = line.strip()
                        if stripped:
                            lines.append(stripped)

                self.name = lines[0]
                self.angle_div = int(lines[1])
                self.axiom = lines[2]
                self.rules = {}

                for line in lines[3:]:
                    if len(line) >= 3 and line[1] == '=':
                        self.rules[line[0]] = line[2:]

                self.redraw()
                self.label_status.setText(f"Загружено: {self.name}")

            except Exception as e:
                self.label_status.setText(f"Ошибка: {str(e)[:50]}")


    def generate_string(self):
        current = self.axiom
        iters = self.slider_iterations.value()

        max_length = 50000 if iters <= 10 else 20000 if iters <= 15 else 5000

        for i in range(iters):
            if len(current) > max_length:
                current = current[:max_length // 2]  # Обрезаем строку
                break
            current = ''.join(self.rules.get(c, c) for c in current)

        return current[:max_length]


    def redraw(self):
        if not self.axiom:
            return

        pixmap = self.draw_lsystem()
        self.label_canvas.setPixmap(pixmap)
        self.label_status.setText(f"{self.name}: {self.slider_iterations.value()} итераций")


    def draw_lsystem(self):
        w, h = 800, 600
        image = QImage(w, h, QImage.Format.Format_ARGB32)
        image.fill(QColor(255, 255, 255, 0))

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        scale = self.slider_scale.value() / 100.0
        step = min(3.0 * scale, 10.0)

        angle_step = 360.0 / self.angle_div * math.pi / 180
        x, y = w // 2, h // 2
        angle = -math.pi / 2

        pen = QPen(Qt.GlobalColor.black, max(1, int(3 / scale)))  # Толщина пера
        painter.setPen(pen)

        lstring = self.generate_string()

        draw_limit = 10000 if len(lstring) > 10000 else len(lstring)

        painter.drawLine(int(x), int(y), int(x), int(y - 10))

        for i, cmd in enumerate(lstring[:draw_limit]):
            if cmd == 'F':
                nx = x + step * math.cos(angle)
                ny = y + step * math.sin(angle)
                painter.drawLine(int(x), int(y), int(nx), int(ny))
                x, y = nx, ny
            elif cmd == '+':
                angle += angle_step
            elif cmd == '-':
                angle -= angle_step

            if i % 1000 == 0:
                painter = QPainter(image)
                painter.setPen(pen)

        painter.end()
        return QPixmap.fromImage(image).scaled(
            self.label_canvas.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LSystemApp()
    window.show()
    sys.exit(app.exec())
