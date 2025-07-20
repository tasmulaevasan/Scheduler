from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6 import uic


class TeacherItem(QWidget):
    def __init__(self, index=1, parent=None):
        super().__init__(parent)
        uic.loadUi("teachersItem.ui", self)
        self.index_label.setText(str(index))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)

        self.teachers_page = uic.loadUi("teachers.ui")
        self.stackedWidget.addWidget(self.teachers_page)
        self.teachers_page.teachersListLayout.addWidget(TeacherItem())

        self.teachers_btn_1.toggled.connect(self._show_teachers)
        self.teachers_btn_2.toggled.connect(self._show_teachers)

    def _show_teachers(self, checked):
        if checked:
            self.stackedWidget.setCurrentWidget(self.teachers_page)