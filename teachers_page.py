from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

import db
from teacher_item import TeacherItem


class TeachersPage(QWidget):
    """Page widget managing the list of teachers."""

    def __init__(self):
        super().__init__()
        uic.loadUi("teachers.ui", self)
        self._items = []

        self.add_btn.clicked.connect(self.add_teacher)
        self.save_btn.clicked.connect(self.save)

        self.load()

    # ---------------------------------------------------------
    def load(self):
        """Load teachers from database."""
        for item in self._items:
            self.teachersListLayout.removeWidget(item)
            item.deleteLater()
        self._items = []

        records = db.load_teachers()
        if not records:
            self.add_teacher()
            return
        for rec in records:
            self.add_teacher(rec)

    def save(self):
        """Save all teachers to database."""
        data = [item.get_data() for item in self._items]
        db.save_teachers(data)

    # ---------------------------------------------------------
    def add_teacher(self, data: dict | None = None):
        index = len(self._items) + 1
        item = TeacherItem(index)
        item.delete_requested.connect(self._remove_item)
        if data:
            item.set_data(data)
        self._items.append(item)
        self.teachersListLayout.addWidget(item)

    def _remove_item(self, item: TeacherItem):
        self.teachersListLayout.removeWidget(item)
        item.deleteLater()
        self._items.remove(item)
        self._refresh_indexes()

    def _refresh_indexes(self):
        for idx, item in enumerate(self._items, 1):
            item.set_index(idx)

    # ---------------------------------------------------------
    def search(self, text: str):
        """Show only items that match the search text."""
        text = text.lower().strip()
        for item in self._items:
            item.setVisible(not text or item.matches(text))
