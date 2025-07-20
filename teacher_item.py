from PyQt6.QtWidgets import QWidget
from PyQt6 import uic


class TeacherItem(QWidget):
    def __init__(self, index=1, parent=None):
        super().__init__(parent)
        uic.loadUi("teachersItem.ui", self)
        self.index_label.setText(str(index))
