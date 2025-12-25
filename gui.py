import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QTextEdit,
    QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel
)

from filesystem import get_command


class FileSystemUI(QWidget):
    def __init__(self, root, current):
        super().__init__()

        self.root = root
        self.current = current

        self.setWindowTitle("File System Manager")
        self.resize(900, 600)

        self.setStyleSheet("""
        QWidget {
            background-color: #0f172a;
            color: #e5e7eb;
            font-family: Consolas;
            font-size: 14px;
        }

        QLabel { color: #94a3b8; }

        QTextEdit {
            background-color: #020617;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 10px;
        }

        QLineEdit {
            background-color: #020617;
            border: 1px solid #1e293b;
            border-radius: 8px;
            padding: 8px;
        }

        QLineEdit:focus { border: 1px solid #2563eb; }

        QPushButton {
            background-color: #2563eb;
            border-radius: 8px;
            padding: 8px 18px;
            font-weight: bold;
        }

        QPushButton:hover { background-color: #1d4ed8; }
        QPushButton:pressed { background-color: #1e40af; }
        """)

        self.init_ui()

    def init_ui(self):
        title = QLabel("Virtual File System Manager")

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.append("Welcome to File System Manager\n")

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter command (e.g. ls, pwd, cd folder)")

        run_btn = QPushButton("Run")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box, 1)
        input_layout.addWidget(run_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.output, 1)
        layout.addLayout(input_layout)

        # اتصال‌ها
        run_btn.clicked.connect(self.handle_command)
        self.input_box.returnPressed.connect(self.handle_command)

    def handle_command(self):
        cmd = self.input_box.text().strip()
        if not cmd:
            return

        self.input_box.clear()

        # ⭐ اتصال به منطق پروژه
        self.current, result = get_command(
            cmd,
            self.root,
            self.current
        )

        if result:
            self.output.append(result)
