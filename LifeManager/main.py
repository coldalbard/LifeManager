from PyQt6.QtWidgets import QApplication
from gui.todo_app import ToDoApp
from database.database import init_db


if __name__ == "__main__":
    init_db()
    app = QApplication([])
    window = ToDoApp()
    window.show()
    app.exec()


