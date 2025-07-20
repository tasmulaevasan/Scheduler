from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from teachers_page import TeachersPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)

        self.icon_only_widget.hide()

        self.teachers_page = TeachersPage()
        self.stackedWidget.addWidget(self.teachers_page)

        self.teachers_btn_1.toggled.connect(self._show_teachers)
        self.teachers_btn_2.toggled.connect(self._show_teachers)
        self.search_btn.clicked.connect(self._search)
        self.search_input.returnPressed.connect(self._search)

        self.stackedWidget.setCurrentIndex(0)
        self.teachers_btn_2.setChecked(True)

    def _show_teachers(self, checked: bool):
        if checked:
            self.stackedWidget.setCurrentWidget(self.teachers_page)

    def _search(self):
        text = self.search_input.text()
        if self.stackedWidget.currentWidget() == self.teachers_page:
            self.teachers_page.search(text)
