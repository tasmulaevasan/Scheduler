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
