import json
import sqlite3

DB_FILE = "teachers.db"


def _get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS teachers(
               id INTEGER PRIMARY KEY,
               is_active INTEGER,
               name TEXT,
               subjects TEXT
           )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS classes(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               grade INTEGER,
               letter TEXT,
               teacher TEXT,
               students INTEGER,
               notes TEXT
           )"""
    )
    return conn


def load_teachers():
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, is_active, name, subjects FROM teachers ORDER BY id")
    teachers = []
    for row in cur.fetchall():
        subjects = json.loads(row[3]) if row[3] else []
        teachers.append(
            {
                "id": row[0],
                "is_active": bool(row[1]),
                "name": row[2] or "",
                "subjects": subjects,
            }
        )
    conn.close()
    return teachers


def save_teachers(teachers):
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM teachers")
    for teacher in teachers:
        cur.execute(
            "INSERT INTO teachers(id, is_active, name, subjects) VALUES (?, ?, ?, ?)",
            (
                teacher.get("id"),
                int(teacher.get("is_active", True)),
                teacher.get("name", ""),
                json.dumps(teacher.get("subjects", [])),
            ),
        )
    conn.commit()
    conn.close()


def load_classes():
    """Return list of class records from database."""
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT grade, letter, teacher, students, notes FROM classes ORDER BY grade, letter"
    )
    records = []
    for row in cur.fetchall():
        records.append(
            {
                "grade": row[0],
                "letter": row[1],
                "teacher": row[2] or "",
                "students": row[3] or 0,
                "notes": row[4] or "",
            }
        )
    conn.close()
    return records


def save_classes(classes):
    """Save list of class records to database."""
    conn = _get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM classes")
    for cls in classes:
        cur.execute(
            "INSERT INTO classes(grade, letter, teacher, students, notes) VALUES (?, ?, ?, ?, ?)",
            (
                cls.get("grade"),
                cls.get("letter"),
                cls.get("teacher", ""),
                cls.get("students", 0),
                cls.get("notes", ""),
            ),
        )
    conn.commit()
    conn.close()
