import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QToolTip
)
from PySide6.QtGui import QColor, QFont, QCursor
from PySide6.QtCore import Qt

from filesystem import get_command


class FileSystemUI(QWidget):
    """
    Main GUI for Virtual File System
    """

    # =====================
    # INIT
    # =====================
    def __init__(self, root, current):
        super().__init__()

        # filesystem state
        self.root = root
        self.current = current

        # window
        self.setWindowTitle("Virtual File System Manager")
        self.resize(1100, 650)

        # style
        self.apply_style()

        # ui
        self.init_ui()

        # initial render
        self.refresh_tree()
        self.update_path_label()

    # =====================
    # STYLE
    # =====================
    def apply_style(self):
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

    # =====================
    # UI SETUP
    # =====================
    def init_ui(self):
        # ---------- TREE ----------
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setMinimumWidth(260)

        # hover support
        self.tree.setMouseTracking(True)
        self.tree.itemEntered.connect(self.on_tree_hover)

        # hide tooltip when mouse leaves tree
        self.tree.viewport().leaveEvent = self.on_tree_leave

        # ---------- PATH ----------
        self.path_label = QLabel("/")
        self.path_label.setStyleSheet("""
            QLabel {
                color: #60a5fa;
                font-weight: bold;
                padding: 4px 6px;
            }
        """)

        # ---------- OUTPUT ----------
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.append("Welcome\n")

        # ---------- INPUT ----------
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("ls | pwd | cd folder")

        run_btn = QPushButton("Run")

        # ---------- LAYOUTS ----------
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

        # ---------- SIGNALS ----------
        run_btn.clicked.connect(self.handle_command)
        self.input_box.returnPressed.connect(self.handle_command)

    # =====================
    # COMMAND HANDLING
    # =====================
    def handle_command(self):
        cmd = self.input_box.text().strip()

        if not cmd:
            return

        if cmd == "clear":
            self.output.clear()
            self.input_box.clear()
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

    # =====================
    # TREE HOVER
    # =====================
    def on_tree_hover(self, item, column):
        node = item.data(0, Qt.UserRole)
        if not node:
            return

        # permission expected: (owner, group, other)
        perm = node.perms
        perm_text = f"{perm[0]}{perm[1]}{perm[2]}"

        tooltip_text = (
            f"Name: {node.name}\n"
            f"Type: {node.type}\n"
            f"Permissions: {perm_text}"
        )

        QToolTip.showText(
            QCursor.pos(),
            tooltip_text,
            self.tree
        )

    def on_tree_leave(self, event):
        QToolTip.hideText()
        event.accept()

    # =====================
    # PATH LABEL
    # =====================
    def update_path_label(self):
        parts = []
        node = self.current

        while node:
            parts.append(node.name)
            node = node.parent

        # ignore root name
        self.path_label.setText("/" + "/".join(parts[::-1][1:]))

    # =====================
    # TREE BUILD
    # =====================
    def refresh_tree(self):
        self.tree.clear()

        root_item = QTreeWidgetItem([self.root.name])
        root_item.setForeground(0, QColor("#e5e7eb"))
        root_item.setFont(0, QFont("", weight=QFont.Bold))
        root_item.setData(0, Qt.UserRole, self.root)

        self.tree.addTopLevelItem(root_item)
        self.build_tree(self.root, root_item)

        self.tree.expandAll()

    def build_tree(self, node, parent_item):
        for child in node.children:
            item = QTreeWidgetItem([child.name])
            item.setData(0, Qt.UserRole, child)

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
