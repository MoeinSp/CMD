from datetime import datetime
class Node:
    def __init__(self , name = None , type = None):
        self.time = datetime.now()
        self.owner = "user"
        self.group = "group"
        self.perms = "755"
        print("Enter Type")
        if type is None:
            print("Enter Type")
            self.type = input()
        if name is None:
            print("Enter Name")
            self.name = input()
        if self.type == "file":
            print("Enter your content.")
            self.Content = input()
            print("Enter Size :")
            self.Size = input()
        if self.type == "directory":
            self.children = []
        self.parent = None

        def resolve_path():

        def mkdir (self ,):

hoom = Node("home","directory")
root = []
root.append(hoom)
root.append(Node())
current_addres = hoom
while True:
    order = input().split()
    if order[0] == "mkdir":
