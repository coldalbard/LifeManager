from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLineEdit, QDateTimeEdit)
from PyQt6.QtCore import Qt, QDateTime
from LifeManager.database.database import get_connection


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список задач")
        self.resize(400, 500)
        self.layout = QVBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Введите новую задачу")
        self.layout.addWidget(self.task_input)
        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        buttons = QHBoxLayout()
        self.add_btn = QPushButton("Добавить")
        self.done_btn = QPushButton("Отметить как выполнено")
        self.del_btn = QPushButton("Удалить")
        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.done_btn)
        buttons.addWidget(self.del_btn)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по задачам...")
        self.search_input.textChanged.connect(self.load_tasks)
        self.layout.addWidget(self.search_input)

        self.layout.addLayout(buttons)
        self.setLayout(self.layout)
        self.date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.layout.addWidget(self.date_input)

        self.load_tasks()

        self.add_btn.clicked.connect(self.add_task)
        self.done_btn.clicked.connect(self.mark_done)
        self.del_btn.clicked.connect(self.delete_task)

    def load_tasks(self):
        self.task_list.clear()
        keyword = self.search_input.text()
        with get_connection() as conn:
            cursor = conn.cursor()
            if keyword:
                cursor.execute("SELECT id, title, is_done, due_date FROM tasks WHERE title LIKE ?", ('%' + keyword + '%',))
            else:
                cursor.execute("SELECT id, title, is_done, due_date FROM tasks")
            for task_id, title, is_done, due in cursor.fetchall():
                display = f"{title} - до {due}" if due else title
                item = QListWidgetItem(display)
                item.setData(1000, task_id)
                if is_done:
                    item.setCheckState(Qt.CheckState.Checked)
                else:
                    item.setCheckState(Qt.CheckState.Unchecked)
                self.task_list.addItem(item)

    def add_task(self):
        title = self.task_input.text()
        due = self.date_input.dateTime().toString("yyyy-MM-dd HH:mm")
        if title.strip():
            with get_connection() as conn:
                conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
                self.task_input.clear()
                self.load_tasks()

    def mark_done(self):
        selected = self.task_list.currentItem()
        if selected:
            task_id = selected.data(1000)
            with get_connection() as conn:
                conn.execute("UPDATE tasks SET is_done = 1 WHERE id = ?", (task_id,))
            self.load_tasks()

    def delete_task(self):
        selected = self.task_list.currentItem()
        if selected:
            task_id = selected.data(1000)
            with get_connection() as conn:
                conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()
            self.load_tasks()
