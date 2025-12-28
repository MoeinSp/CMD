import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel,
    QTreeWidget, QTreeWidgetItem
)
from PySide6.QtGui import QColor, QFont

from filesystem import get_command


class FileSystemUI(QWidget):
    def __init__(self, root, current):
        super().__init__()

        self.root = root
        self.current = current

        self.setWindowTitle("Virtual File System Manager")
        self.resize(1100, 650)

        # ===== STYLE =====
        self.setStyleSheet("""
        QWidget {
            background-color: #0b1020;
            color: #d1d5db;
            font-family: Consolas;
            font-size: 14px;
        }

        QLabel {
            color: #9ca3af;
        }

        QTextEdit {
            background-color: #020617;
            border: 1px solid #1f2937;
            border-radius: 8px;
            padding: 10px;
        }

        QLineEdit {
            background-color: #020617;
            border: 1px solid #1f2937;
            border-radius: 8px;
            padding: 8px;
        }

        QLineEdit:focus {
            border: 1px solid #3b82f6;
        }

        QPushButton {
            background-color: #1f2937;
            border-radius: 8px;
            padding: 8px 18px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #374151;
        }

        QPushButton:pressed {
            background-color: #111827;
        }
        """)

        self.init_ui()
        self.refresh_tree()
        self.update_path_label()

    # ---------- UI ----------
    def init_ui(self):
        title = QLabel("Virtual File System Manager")

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setMinimumWidth(260)

        self.path_label = QLabel("/")
        self.path_label.setStyleSheet("""
            QLabel {
                color: #60a5fa;
                font-weight: bold;
                padding: 4px 6px;
            }
        """)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.append("Welcome\n")

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("ls | pwd | cd folder")

        run_btn = QPushButton("Run")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box, 1)
        input_layout.addWidget(run_btn)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.path_label)
        right_layout.addWidget(self.output, 1)
        right_layout.addLayout(input_layout)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.tree, 1)
        main_layout.addLayout(right_layout, 3)

        run_btn.clicked.connect(self.handle_command)
        self.input_box.returnPressed.connect(self.handle_command)

    # ---------- LOGIC ----------
    def handle_command(self):
        cmd = self.input_box.text().strip()
        if cmd == "clear":
            self.output.clear()
            return
        if not cmd:
            return

        self.input_box.clear()

        self.current, result = get_command(
            cmd,
            self.root,
            self.current
        )

        if result:
            self.output.append(result)

        self.refresh_tree()
        self.update_path_label()

    # ---------- PATH ----------
    def update_path_label(self):
        parts = []
        node = self.current
        while node:
            parts.append(node.name)
            node = node.parent
        self.path_label.setText("/" + "/".join(parts[::-1][1:]))

    # ---------- TREE ----------
    def get_children(self, node):
        return node.children

    def refresh_tree(self):
        self.tree.clear()

        root_item = QTreeWidgetItem([self.root.name])
        root_item.setForeground(0, QColor("#e5e7eb"))
        root_item.setFont(0, QFont("", weight=QFont.Bold))

        self.tree.addTopLevelItem(root_item)
        self.build_tree(self.root, root_item)

        self.tree.expandAll()

    def build_tree(self, node, parent_item):
        for child in self.get_children(node):
            item = QTreeWidgetItem([child.name])

            if child.type == "directory":
                item.setForeground(0, QColor("#cbd5e1"))
            else:
                item.setForeground(0, QColor("#9ca3af"))

            if child is self.current:
                item.setForeground(0, QColor("#60a5fa"))
                font = QFont()
                font.setBold(True)
                item.setFont(0, font)

            parent_item.addChild(item)

            if child.type == "directory":
                self.build_tree(child, item)

