import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QTextEdit,
    QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel
)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("File System Manager")
window.resize(900, 600)

# ===== STYLE =====
window.setStyleSheet("""
QWidget {
    background-color: #0f172a;
    color: #e5e7eb;
    font-family: Consolas;
    font-size: 14px;
}

QLabel {
    color: #94a3b8;
}

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

QLineEdit:focus {
    border: 1px solid #2563eb;
}

QPushButton {
    background-color: #2563eb;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}
""")

# ===== HEADER =====
title = QLabel("Virtual File System Manager")

# ===== OUTPUT (Terminal Area) =====
output = QTextEdit()
output.setReadOnly(True)
output.setMinimumHeight(420)   # 👈 ارتفاع خروجی
output.append("Welcome to File System Manager\n")

# ===== INPUT AREA =====
input_box = QLineEdit()
input_box.setPlaceholderText("Enter command (e.g. ls, pwd, cd folder)")
input_box.setMinimumHeight(38)  # 👈 ارتفاع ورودی

run_btn = QPushButton("Run")
run_btn.setFixedHeight(38)      # 👈 ارتفاع دکمه

# ===== INPUT LAYOUT =====
input_layout = QHBoxLayout()
input_layout.addWidget(input_box, 1)  # 👈 ورودی کش بیاد
input_layout.addWidget(run_btn)

# ===== MAIN LAYOUT =====
layout = QVBoxLayout()
layout.setSpacing(12)
layout.addWidget(title)
layout.addWidget(output, 1)     # 👈 خروجی کل فضا رو بگیره
layout.addLayout(input_layout)

window.setLayout(layout)

# ===== LOGIC HOOK (نمونه اتصال) =====
def handle_command():
    cmd = input_box.text().strip()
    if not cmd:
        return

    input_box.clear()

    # 🔽 اینجا منطق خودت رو صدا بزن
    # result = run_command(cmd)
    result = f"Executed: {cmd}"  # موقت

    output.append(f"> {cmd}")
    output.append(result)
    output.append("")  # خط خالی

run_btn.clicked.connect(handle_command)
input_box.returnPressed.connect(handle_command)

window.show()
app.exec()
