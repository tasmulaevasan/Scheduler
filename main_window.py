from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from teacher_item import TeacherItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)

        self.teachers_page = uic.loadUi("teachers.ui")
        self.stackedWidget.addWidget(self.teachers_page)
        self.teachers_page.teachersListLayout.addWidget(TeacherItem())

        self.teachers_page.add_btn.clicked.connect(self._add_teacher)

        self.teachers_btn_1.toggled.connect(self._show_teachers)
        self.teachers_btn_2.toggled.connect(self._show_teachers)

    def _show_teachers(self, checked):
        if checked:
            self.stackedWidget.setCurrentWidget(self.teachers_page)

    def _add_teacher(self):
        index = self.teachers_page.teachersListLayout.count() + 1
        self.teachers_page.teachersListLayout.addWidget(TeacherItem(index))
