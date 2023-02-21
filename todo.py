import sys
from PyQt5.QtCore import Qt, QSettings, QByteArray, QDataStream, QIODevice
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton

class TodoItem:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

class TodoListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.todo_list = []
        self.load_todo_list()

        self.todo_input = QLineEdit()
        self.todo_list_view = QListWidget()
        self.todo_list_view.addItems(self.todo_list)

        add_button = QPushButton("추가")
        add_button.clicked.connect(self.add_todo_item)

        delete_button = QPushButton("완료")
        delete_button.clicked.connect(self.delete_todo_item)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.todo_input)
        input_layout.addWidget(add_button)

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.todo_list_view)
        list_layout.addWidget(delete_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(list_layout)

        self.setLayout(main_layout)

    def add_todo_item(self):
        text = self.todo_input.text()
        if text:
            todo_item = TodoItem(text)
            self.todo_list.append(todo_item)
            self.todo_list_view.addItem(text)
            self.todo_input.setText("")
            self.save_todo_list()

    def delete_todo_item(self):
        current_item = self.todo_list_view.currentItem()
        if current_item:
            current_row = self.todo_list_view.row(current_item)
            self.todo_list_view.takeItem(current_row)
            del self.todo_list[current_row]
            self.save_todo_list()

    def load_todo_list(self):
        settings = QSettings("MyCompany", "MyApp")
        todo_list_bytes = settings.value("todo_list")
        if todo_list_bytes:
            stream = QDataStream(QByteArray(todo_list_bytes), QIODevice.ReadOnly)
            while not stream.atEnd():
                text = stream.readQString()
                todo_item = TodoItem(text)
                self.todo_list.append(todo_item)
                self.todo_list_view.addItem(text)

    def save_todo_list(self):
        settings = QSettings("MyCompany", "MyApp")
        todo_list_bytes = QByteArray()
        stream = QDataStream(todo_list_bytes, QIODevice.WriteOnly)
        for todo_item in self.todo_list:
            stream.writeQString(todo_item.text)
        settings.setValue("todo_list", todo_list_bytes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo_list_widget = TodoListWidget()
    todo_list_widget.show()
    sys.exit(app.exec_())