from PyQt6.QtWidgets import QWidget, QListWidgetItem
from PyQt6.QtCore import pyqtSignal
from PyQt6 import uic


class TeacherItem(QWidget):
    """Widget representing one teacher in the list."""

    delete_requested = pyqtSignal(QWidget)

    SUBJECTS = [
        "Математика",
        "Физика",
        "Информатика",
        "Химия",
        "История",
    ]

    def __init__(self, index: int = 1, parent=None):
        super().__init__(parent)
        uic.loadUi("teachersItem.ui", self)
        self.set_index(index)
        self.isActive_checkbox.setChecked(True)
        self.subjects_comboBox.addItems(self.SUBJECTS)
        self.add_subject_btn.setText("+")
        self.delete_btn.setText("Удалить")

        self.add_subject_btn.clicked.connect(self._add_subject)
        self.delete_btn.clicked.connect(lambda: self.delete_requested.emit(self))
        self.subject_list.itemDoubleClicked.connect(self._remove_subject)

    def set_index(self, index: int) -> None:
        self.index_label.setText(str(index))

    def _add_subject(self):
        subject = self.subjects_comboBox.currentText()
        if not subject:
            return
        for i in range(self.subject_list.count()):
            if self.subject_list.item(i).text() == subject:
                return
        self.subject_list.addItem(subject)

    def _remove_subject(self, item: QListWidgetItem):
        row = self.subject_list.row(item)
        self.subject_list.takeItem(row)

    def get_data(self) -> dict:
        subjects = [self.subject_list.item(i).text() for i in range(self.subject_list.count())]
        return {
            "id": int(self.index_label.text()),
            "is_active": self.isActive_checkbox.isChecked(),
            "name": self.name_edit.text(),
            "subjects": subjects,
        }

    def set_data(self, data: dict) -> None:
        self.set_index(data.get("id", 1))
        self.isActive_checkbox.setChecked(data.get("is_active", True))
        self.name_edit.setText(data.get("name", ""))
        for subj in data.get("subjects", []):
            self.subject_list.addItem(subj)

    def matches(self, text: str) -> bool:
        text = text.lower()
        return text in self.name_edit.text().lower() or text == self.index_label.text()
