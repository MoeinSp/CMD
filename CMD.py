from filesystem import *
from gui import *



home = Node("home","directory")
root = Node("/","directory")
root.children.append(home)
home.parent = root
current_address = home

app = QApplication(sys.argv)
ui = FileSystemUI(root, current_address)
ui.show()

sys.exit(app.exec())