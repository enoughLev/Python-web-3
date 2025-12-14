import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from forms.form_7_ui import Ui_MainWindow


class PianoApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.note_paths = {}
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.load_notes()
        self.connect_buttons()

    def load_notes(self):
        notes_path = "./notes/"
        notes = ['ci.wav', 'do.wav', 're.wav', 'mi.wav', 'fa.wav', 'la.wav', 'sol.wav']
        for note in notes:
            file_path = os.path.join(notes_path, note)
            if os.path.exists(file_path):
                self.note_paths[note] = file_path


    def connect_buttons(self):
        self.btn_c.clicked.connect(lambda: self.play_note('do.wav'))
        self.btn_d.clicked.connect(lambda: self.play_note('re.wav'))
        self.btn_e.clicked.connect(lambda: self.play_note('mi.wav'))
        self.btn_f.clicked.connect(lambda: self.play_note('fa.wav'))
        self.btn_g.clicked.connect(lambda: self.play_note('sol.wav'))
        self.btn_a.clicked.connect(lambda: self.play_note('la.wav'))
        self.btn_b.clicked.connect(lambda: self.play_note('ci.wav'))

    def play_note(self, filename):
        file_path = self.note_paths.get(filename)
        if file_path:
            self.player.setSource(QUrl.fromLocalFile(file_path))
            self.player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PianoApp()
    window.show()
    sys.exit(app.exec())
