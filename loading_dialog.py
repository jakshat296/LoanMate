import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
import resources

class FingerprintDialog(QDialog):
    def __init__(self):
        super(FingerprintDialog, self).__init__()

        self.setWindowTitle("Fingerprint Matching")
        self.setWindowIcon(QIcon("://icons/resources/icons/download.ico"))
        self.setGeometry(100, 100, 300, 100)

        layout = QVBoxLayout()

        self.message_label = QLabel("Please wait.", self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font: 18pt \"Segoe UI\";\n")
        layout.addWidget(self.message_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_message)
        self.timer.start(1000)  # Update message every second

        self.setLayout(layout)

    def update_message(self):
        current_text = self.message_label.text()
        if "....." in current_text:
            current_text = "Please wait"
        else:
            current_text += "."
        self.message_label.setText(current_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = FingerprintDialog()
    dialog.exec_()
    sys.exit(app.exec_())
