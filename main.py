from PyQt6.QtWidgets import QApplication
import sys
from main_window import MainWindow
import resource_rc

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
