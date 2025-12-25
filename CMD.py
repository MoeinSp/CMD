from filesystem import *




home = Node("home","directory")
root = Node("/","directory")
root.children.append(home)
home.parent = root
current_address = home

while True:
    Node.pwd(current_address)
    text = input().strip()
    if not text:
        continue
    order = text.split()
    if order[0] == "mkdir":
        Node.mkdir(root , current_address ,text[6:])
    elif order[0] == "touch":
        Node.touch(current_address,order[1:])
    elif order[0] == "ls":
        Node.ls(current_address,order,root,text)
    elif order[0] == "cd":
        if len(order)!=2:
            print("Invalid command format")
            continue
        current_address = Node.cd(current_address,text[3:],root)
    elif order == "pwd":
        Node.pwd(current_address)
    elif order[0] == "stat" and len(order)==2:
        Node.stat(current_address,order[1],root)
    elif order[0] == "rm" and len(order)==2:
        Node.rm1(current_address,text[3:])
    elif order[0] == "rm":
        Node.rm1(current_address,text[7:])
    elif order[0] == "rmdir":
        Node.rmdir(current_address,order[1])
    elif order[0] == "mv" and len(order)==3:
        Node.mv(current_address,order[1],order[2],root)
    elif order[0] == "cp":
        Node.cp(current_address,text[3:])

