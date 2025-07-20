"""UI page for managing school classes."""

from PyQt6.QtWidgets import (
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QStackedWidget,
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QTextEdit,
    QLabel,
)
from PyQt6.QtCore import Qt

import db


class ClassesPage(QWidget):
    """Widget displaying and editing classes."""

    GRADES = list(range(1, 12))

    def __init__(self):
        super().__init__()
        self._classes = {}
        self._setup_ui()
        self.load()

    # ------------------------------------------------------------------
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        splitter.addWidget(self.tree)

        self.stack = QStackedWidget()
        splitter.addWidget(self.stack)

        # grade overview page
        self.grade_page = QWidget()
        grade_layout = QVBoxLayout(self.grade_page)
        self.sections_table = QTableWidget(0, 1)
        self.sections_table.setHorizontalHeaderLabels(["Sections"])
        grade_layout.addWidget(self.sections_table)
        self.add_section_btn = QPushButton("Add section")
        grade_layout.addWidget(self.add_section_btn)
        self.stack.addWidget(self.grade_page)

        # section detail page
        self.section_page = QWidget()
        form = QFormLayout(self.section_page)
        self.teacher_edit = QLineEdit()
        self.students_spin = QSpinBox()
        self.students_spin.setRange(0, 1000)
        self.notes_edit = QTextEdit()
        form.addRow(QLabel("Class teacher"), self.teacher_edit)
        form.addRow(QLabel("Students"), self.students_spin)
        form.addRow(QLabel("Notes"), self.notes_edit)
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.delete_btn = QPushButton("Delete")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.delete_btn)
        form.addRow(btn_layout)
        self.stack.addWidget(self.section_page)

        self.tree.itemClicked.connect(self._on_tree_clicked)
        self.add_section_btn.clicked.connect(self._add_section)
        self.save_btn.clicked.connect(self._save_section)
        self.delete_btn.clicked.connect(self._delete_section)

    # ------------------------------------------------------------------
    def load(self) -> None:
        """Load classes from database."""
        self._classes = {}
        self.tree.clear()
        records = db.load_classes()
        for rec in records:
            key = (rec["grade"], rec["letter"])
            self._classes[key] = {
                "teacher": rec.get("teacher", ""),
                "students": rec.get("students", 0),
                "notes": rec.get("notes", ""),
            }
        self._fill_tree()

    def save(self) -> None:
        """Save all classes to database."""
        records = []
        for (grade, letter), info in self._classes.items():
            records.append(
                {
                    "grade": grade,
                    "letter": letter,
                    "teacher": info.get("teacher", ""),
                    "students": info.get("students", 0),
                    "notes": info.get("notes", ""),
                }
            )
        db.save_classes(records)

    # ------------------------------------------------------------------
    def _fill_tree(self) -> None:
        self.tree.clear()
        grade_items = {}
        for grade in self.GRADES:
            item = QTreeWidgetItem([f"{grade} class"])
            self.tree.addTopLevelItem(item)
            grade_items[grade] = item
        for (grade, letter) in sorted(self._classes.keys()):
            parent = grade_items.get(grade)
            if parent:
                child = QTreeWidgetItem([letter])
                parent.addChild(child)
                parent.setExpanded(True)

    def _on_tree_clicked(self, item: QTreeWidgetItem) -> None:
        parent = item.parent()
        if parent is None:
            grade = int(item.text(0).split()[0])
            self._show_grade_page(grade)
        else:
            grade = int(parent.text(0).split()[0])
            letter = item.text(0)
            self._show_section_page(grade, letter)

    def _show_grade_page(self, grade: int) -> None:
        self.stack.setCurrentWidget(self.grade_page)
        self.sections_table.setRowCount(0)
        for (g, letter), info in sorted(self._classes.items()):
            if g == grade:
                row = self.sections_table.rowCount()
                self.sections_table.insertRow(row)
                self.sections_table.setItem(row, 0, QTableWidgetItem(letter))
        self.add_section_btn.setProperty("grade", grade)

    def _show_section_page(self, grade: int, letter: str) -> None:
        self.stack.setCurrentWidget(self.section_page)
        key = (grade, letter)
        info = self._classes.get(key, {})
        self.section_page.setProperty("grade", grade)
        self.section_page.setProperty("letter", letter)
        self.teacher_edit.setText(info.get("teacher", ""))
        self.students_spin.setValue(info.get("students", 0))
        self.notes_edit.setPlainText(info.get("notes", ""))

    # ------------------------------------------------------------------
    def _add_section(self) -> None:
        grade = self.add_section_btn.property("grade")
        if not grade:
            return
        letters = [l for (g, l) in self._classes.keys() if g == grade]
        next_letter = chr(ord('A') + len(letters))
        self._classes[(grade, next_letter)] = {"teacher": "", "students": 0, "notes": ""}
        self._fill_tree()
        self._show_grade_page(grade)
        self.save()

    def _save_section(self) -> None:
        grade = self.section_page.property("grade")
        letter = self.section_page.property("letter")
        if not grade or not letter:
            return
        self._classes[(grade, letter)] = {
            "teacher": self.teacher_edit.text(),
            "students": self.students_spin.value(),
            "notes": self.notes_edit.toPlainText(),
        }
        self._fill_tree()
        self.save()

    def _delete_section(self) -> None:
        grade = self.section_page.property("grade")
        letter = self.section_page.property("letter")
        if not grade or not letter:
            return
        self._classes.pop((grade, letter), None)
        self._fill_tree()
        self.stack.setCurrentWidget(self.grade_page)
        self.save()

    # ------------------------------------------------------------------
    def search(self, text: str) -> None:
        """Filter tree items by search text."""
        text = text.lower().strip()
        for i in range(self.tree.topLevelItemCount()):
            grade_item = self.tree.topLevelItem(i)
            match_grade = text in grade_item.text(0).lower()
            show_grade = False
            for j in range(grade_item.childCount()):
                child = grade_item.child(j)
                match_child = text in child.text(0).lower()
                child.setHidden(not (not text or match_child))
                show_grade = show_grade or not child.isHidden()
            grade_item.setHidden(not (not text or match_grade or show_grade))
