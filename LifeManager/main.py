from PyQt6.QtWidgets import QApplication
from gui.todo_app import ToDoApp
from database.database import init_db
import sqlite3


if __name__ == "__main__":
    init_db()
    app = QApplication([])
    window = ToDoApp()
    window.show()
    app.exec()
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

