from datetime import datetime

class Node:
    def __init__(self , name , type_, time = None , content = None):
        if time is None:
            self.time = datetime.now()
        else:
            self.time = time
        self.owner = "user"
        self.group = "group"
        self.perms = "755"
        self.type = type_
        self.name = name
        if self.type == "file":
            self.content = content
            if self.content is not None:
                self.size = len(self.content)
            else :
                self.size = 0
        if self.type == "directory":
            self.children = []
        self.parent = None
    def clone(obj,coppy,parentcopy):
        coppy = Node(obj.name,obj.type,obj.time,obj.content)
        return
    def splite_way(address):
        if "/" not in address:
            return ".", address

        index = address.rfind("/")
        if index == 0:
            parent = "/"
        else:
            parent = address[:index]

        name = address[index + 1:]
        name = name.strip()
        parent = parent.strip()
        return parent, name

    def resolve_path(path,current,root):
        if path.startswith("/"):
            current = root
            parts = path[1:].split("/")
        else:
            parts = path.split("/")
        for i,part in enumerate(parts):
            if part == "..":
                if current.parent is not None:
                    current = current.parent
                    continue
            if part == "." or part == "":
                continue
            address = None
            if current.children is not None:
                for child in current.children:
                    if child.name == part:
                        address = child
                        break
            if address is None:
                return None
            if i != len(parts) - 1 and address.type != "directory":
                return None
            current = address

        return current

    def stat(current,address,root):
            temp = Node.resolve_path(address, current, root)
            if temp is not None:
                if temp.type != "directory":
                    print(f"{temp.type}  {temp.time} Size = {temp.size} ")
                else:
                    print(f"{temp.type}  {temp.time} ")


    def mkdir (root,current,text):
        parent_path , name = Node.splite_way(text)
        temp = Node.resolve_path(parent_path , current, root)
        if temp is None:
            print("Invalid command format")
            return
        if temp.type != "directory":
            print("Error: Not a directory")
            return
        for child in temp.children:
            if child.name == name:
                print("Error: Name already exists")
                return
        new = Node(name, "directory")
        temp.children.append(new)
        new.parent = temp
    def touch(current,order):
        name = None
        time = datetime.now()
        if order[0] == "-t" and len(order) == 4:
            time = None
            date_str = order[1] + " " + order[2]
            try:
                time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Invalid time format")
            if time is None:
                return
            name =order[-1]
        elif len(order) == 1:
            name = order[0]

        for child in current.children:
            if child.name == name:
                print("Error: Name already exists")
                return
        content = input("Enter the content: ")
        new = Node(name, "file",None,content)
        new.parent = current
        current.children.append(new)

    def ls(current,order,root,text):
        temp = current
        if len(order)>=2 and  "/" in order[-1]:
            #ادرس رو درست کن
            temp = Node.resolve_path(order[-1], current, root)
            if temp is None:
                print("Invalid path")
                return
            order = order[:-1]
        count = 0
        if len(order)==1:
            for child in temp.children:
                if not child.name.startswith("."):
                    print(child.name, end="  ")
                    count += 1
            if count > 0:
                print()
        elif order[1] == "-l":
            for child in temp.children:
                if child.type == "file":
                    print(child.size, end=" ")
                print(child.time.strftime("%b %d %H:%M"),end=" ")
                print(child.name)


        elif order[1] == "-a":
            for child in temp.children:
                print(child.name, end="  ")

    def rm1(currrent , filename):
        for child in currrent.children:
            if child.name == filename:
                print("success")
                currrent.children.remove(child)
                return
        print("error")

    def rm2(currrent , name):
        for child in currrent.children:
            if child.name == name:
                if child.type != "directory":
                    currrent.children.remove(child)
                    print("success")
                    return
                elif child.type == "directory":
                    Node.delete_dir(child)
        print("error")

    def delete_dir(dir):
        for child in list(dir.children):
            if child.type == "file":
                dir.children.remove(child)
            elif child.type == "directory":
                Node.delete_dir(child)
                dir.children.remove(child)

    def rmdir(current,dir_name):
        for child in current.children:
            if child.name == dir_name:
                if len(child.children) == 0:
                    print("success")
                    current.children.remove(child)
                    return
        print("error")

    def cd(current, text, root):
        temp = Node.resolve_path(text, current, root)

        if temp is None:
            print("Error: Invalid path")
            return current
        if temp.type != "directory":
            print("Error: Not a directory")
            return current
        return temp

    def pwd(current_address):
        path = []
        if not isinstance(current_address,Node):
            return
        node = current_address
        while node is not None:
            path.append(node.name)
            node = node.parent

        path = path[::-1]
        path= path[1:]
        print("/"+"/".join(path))

    def mv(current, name, new, root):
        old = None
        for child in current.children:
            if child.name == name:
                old = child
                break

        if old is None:
            print(f"{name} does not exist")
            return

        target = new.rstrip("/")

        dest = Node.resolve_path(target, current, root)
        if dest is not None and dest.type == "directory":
            old.parent.children.remove(old)
            old.parent = dest
            dest.children.append(old)
            return

        if "/" in target:
            parent_path, new_name = target.rsplit("/", 1)
            parent = Node.resolve_path(parent_path, current, root)
            if parent is None or parent.type != "directory":
                print("Error: Invalid path")
                return

            for child in parent.children:
                if child.name == new_name:
                    print("Error: Name already exists")
                    return

            old.parent.children.remove(old)
            old.parent = parent
            old.name = new_name
            parent.children.append(old)
            return

        for child in current.children:
            if child.name == target:
                print("Error: Name already exists")
                return

        old.name = target

    def cp(current,src,dst,root):
        src1 = src.rstrip("/")
        source = Node.resolve_path(src1, current, root)
        if source is None:
            print("Error: Invalid path")
            return


        dst1 = dst.rstrip("/")
        dest = Node.resolve_path(dst1, current, root)
        if dst[-1] == "/" and dest is not None and dest.type != "directory":
            print("Error: Not a directory")
            return


        if dest is None:
            # جدا کن والد و فرزند و چک کن اگه والد معتبر بود ...
            # return


            
        if(dest.type == "directory"):
            new_copy = Node.copy(source,dest)
        elif dest.type == "file":
            if(source.type == "directory"):
                print("Error: Not a directory to file")
            elif (dest.type == "file"):
                new_copy = Node.copy(source, dest)
                return


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

