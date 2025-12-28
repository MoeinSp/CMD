from datetime import datetime

History_c = []


class Node:
    def __init__(self, name, type_, time=None):
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
            self.content = ""
            self.size = len(self.content)
        if self.type == "directory":
            self.children = []
        self.parent = None

    @staticmethod
    def clone(obj, coppy, parent_copy):
        coppy = Node(obj.name, obj.type, obj.time, obj.content)
        return

    @staticmethod
    def split_way(address):
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

    @staticmethod
    def resolve_path(path, current, root):
        if path.startswith("/"):
            current = root
            parts = path[1:].split("/")
        else:
            parts = path.split("/")
        for i, part in enumerate(parts):
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

    @staticmethod
    def stat(current, address, root):
        result = ""
        temp = Node.resolve_path(address, current, root)
        if temp is not None:
            if temp.type != "directory":
                result = f"{temp.type}  {temp.time} Size = {temp.size} "
                return current, result
            else:
                result = f"{temp.type}  {temp.time} "
                return current, result

    @staticmethod
    def mkdir(root, current, text):
        result = ""
        parent_path, name = Node.split_way(text)
        temp = Node.resolve_path(parent_path, current, root)
        if temp is None:
            result = "Invalid command format"
            return current, result
        if temp.type != "directory":
            result = "Error: Not a directory"
            return current, result
        for child in temp.children:
            if child.name == name:
                result = "Error: Name already exists"
                return current, result
        if not Node.has_permission(temp,"w") or not Node.has_permission(current,"x"):
            result = "Error: Permission denied"
            return current, result
        new = Node(name, "directory")
        temp.children.append(new)
        new.parent = temp
        result = "success"
        return current, result

    @staticmethod
    def touch(current, order):
        result = ""
        name = ""
        time = datetime.now()
        if order[0] == "-t" and len(order) == 4:
            time = None
            date_str = order[1] + " " + order[2]
            try:
                time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                result = "Invalid time format"
                return current, result
            if time is None:
                return current, result
            name = order[-1]
        elif len(order) == 1:
            name = order[0]

        for child in current.children:
            if child.name == name:
                result = "Error: Name already exists"
                return current, result
        new = Node(name, "file", None)
        new.parent = current
        current.children.append(new)
        result = "success"
        return current, result

    @staticmethod
    def ls(current, order, root, text):
        result = ""
        temp = current
        if len(order) >= 2 and "/" in order[-1]:
            # ادرس رو درست کن
            temp = Node.resolve_path(order[-1], current, root)
            if temp is None:
                result = "Invalid path"
                return current, result
            order = order[:-1]
        count = 0
        if len(order) == 1:
            for child in temp.children:
                if not child.name.startswith("."):
                    result += child.name + "  "
                    count += 1
            if count > 0:
                result += "\n"
        elif order[1] == "-l":
            for child in temp.children:
                if child.type == "file":
                    result += f"{child.size}  "
                result += f'{child.time.strftime("%b %d %H:%M")}  '
                result += child.name + "\n"


        elif order[1] == "-a":
            for child in temp.children:
                result += child.name + "  "
        return current, result

    @staticmethod
    def rm1(current, filename):

        for child in current.children:
            if child.name == filename:
                result = "success"
                current.children.remove(child)
                return current, result
        result = "error"
        return current, result

    @staticmethod
    def rm2(current, name):
        for child in current.children:
            if child.name == name:
                if child.type != "directory":
                    current.children.remove(child)
                    result = "success"
                    return current, result
                elif child.type == "directory":
                    Node.delete_dir(child)
        result = "error"
        return current, result

    @staticmethod
    def delete_dir(dir):
        for child in list(dir.children):
            if child.type == "file":
                dir.children.remove(child)
            elif child.type == "directory":
                Node.delete_dir(child)
                dir.children.remove(child)

    @staticmethod
    def rmdir(current, dir_name):
        for child in current.children:
            if child.name == dir_name:
                if len(child.children) == 0:
                    result = "success"
                    current.children.remove(child)
                    return current, result
        result = "error"
        return current, result

    @staticmethod
    def cd(current, text, root):
        temp = Node.resolve_path(text, current, root)
        result = ""
        if temp is None:
            result = "Error: Invalid path"
            return current, result
        if temp.type != "directory":
            result = "Error: Not a directory"
            return current, result
        return temp, result

    @staticmethod
    def pwd(current_address):
        result = ""
        path = []
        node = current_address
        while node is not None:
            path.append(node.name)
            node = node.parent

        path = path[::-1]
        path = path[1:]
        result = "/" + "/".join(path)
        return current_address, result

    @staticmethod
    def mv(current, name, new, root):
        result = ""
        old = None
        for child in current.children:
            if child.name == name:
                old = child
                break

        if old is None:
            result = f"{name} does not exist"
            return current, result

        target = new.rstrip("/")

        dest = Node.resolve_path(target, current, root)
        if dest is not None and dest.type == "directory":
            old.parent.children.remove(old)
            old.parent = dest
            dest.children.append(old)
            return current, result

        if "/" in target:
            parent_path, new_name = target.rsplit("/", 1)
            parent = Node.resolve_path(parent_path, current, root)
            if parent is None or parent.type != "directory":
                result = "Error: Invalid path"
                return current, result

            for child in parent.children:
                if child.name == new_name:
                    result = "Error: Name already exists"
                    return current, result

            old.parent.children.remove(old)
            old.parent = parent
            old.name = new_name
            parent.children.append(old)
            result = "success"
            return current, result

        for child in current.children:
            if child.name == target:
                result = "Error: Name already exists"
                return current, result

        old.name = target
        result = "success"
        return current, result

    @staticmethod
    def cat(root, current, path):
        if not path:
            return current, "cat: missing operand"

        target = Node.resolve_path(path, current, root)

        if not target:
            return current, f"cat: {path}: No such file or directory"
        if target.type == "directory":
            return current, f"cat: {path}: Is a directory"

        return current, target.content

    @staticmethod
    def echo(current, root, order):
        if ">" not in order:
            return current, order

        text, path = order.split(">", 1)
        text = text.strip()
        path = path.strip()

        if not path:
            return current, "echo: missing operand"

        target = Node.resolve_path(path, current, root)
        if not target:
            aray = path.split()
            Node.touch(current, aray)
            target = Node.resolve_path(path, current, root)
            if not target:
                return current, f"echo: {path}: No such file or directory"

        if target.type == "directory":
            return current, f"echo: {path}: Is a directory"

        target.content = text
        target.size = len(text)
        return current, "success"

    @staticmethod
    def cp(current, src, dst, root):
        result = ""
        src1 = src.rstrip("/")
        source = Node.resolve_path(src1, current, root)
        if source is None:
            result = "Error: Invalid path"
            return current, result

        dst1 = dst.rstrip("/")
        dest = Node.resolve_path(dst1, current, root)
        if dst[-1] == "/" and dest is not None and dest.type != "directory":
            result = "Error: Not a directory"
            return current, result

        if dest is None:
            return current, result

        if dest.type == "directory":
            new_copy = Node.copy(source, dest)
        elif dest.type == "file":
            if (source.type == "directory"):
                result = "Error: Not a directory to file"
                return current, result
            elif (dest.type == "file"):
                new_copy = Node.copy(source, dest)
                result = "success"
                return current, result

    @staticmethod
    def chmod(root,current,order):
        if len(order) != 2:
            return current, "chmod: missing operand"
        perm, path = order[0], order[1]
        if not perm:
            return current, "chmod: missing operand"
        else:
            if len(perm) != 3:
                return current, "chmod: invalid operand"
            for per in perm:
                if  not per.isdigit() or not 0 <= int(per) <= 7 :
                    return current, "chmod: invalid operand"
        if not path:
            return current, "chmod: missing operand"
        target = Node.resolve_path(path, current, root)
        if not target:
            return current, "chmod: No such file or directory"
        target.perms = perm
        return current, "success"
    @staticmethod
    def has_permission(node, action):
        if node is None or not isinstance(node, Node):
            return False
        perm_digit = int(node.perms[0])

        if action == "r":
            return perm_digit & 4 != 0

        if action == "w":
            return perm_digit & 2 != 0

        if action == "x":
            return perm_digit & 1 != 0
        return "access denied"



def get_command(text, root, current_address):
    result = ""
    global History_c
    History_c.append(text)
    order = text.split()

    if order[0] == "mkdir":
        current_address, result = Node.mkdir(root, current_address, text[6:])
        return current_address, result

    elif order[0] == "touch":
        current_address, result = Node.touch(current_address, order[1:])
        return current_address, result

    elif order[0] == "ls":
        current_address, result = Node.ls(current_address, order, root, text)
        return current_address, result

    elif order[0] == "cd":
        if len(order) != 2:
            result = "Invalid command format"
            return current_address, result
        current_address, result = Node.cd(current_address, text[3:], root)
        return current_address, result

    elif order[0] == "pwd":
        current_address, result = Node.pwd(current_address)
        return current_address, result

    elif order[0] == "stat" and len(order) == 2:
        current_address, result = Node.stat(current_address, order[1], root)
        return current_address, result

    elif order[0] == "rm" and len(order) == 2:
        current_address, result = Node.rm1(current_address, text[3:])
        return current_address, result

    elif order[0] == "rm":
        current_address, result = Node.rm1(current_address, text[7:])
        return current_address, result

    elif order[0] == "rmdir":
        current_address, result = Node.rmdir(current_address, order[1])
        return current_address, result

    elif order[0] == "mv" and len(order) == 3:
        current_address, result = Node.mv(current_address, order[1], order[2], root)
        return current_address, result

    elif order[0] == "cp":
        current_address, result = Node.cp(current_address, order[1], order[2], root)
        return current_address, result

    elif order[0] == "echo":
        current_address, result = Node.echo(current_address, root, text[5:])
        return current_address, result

    elif order[0] == "whoami":
        return current_address, "Moein"

    elif order[0] == "chmod":
        current_address, result = Node.chmod(current_address, root, order[1:])
        return current_address, result

    elif text == "history":
        if not History_c:
            return current_address, "no history"
        for i, item in enumerate(History_c):
            result += f"{i + 1}. {item}\n"
        return current_address, result

    result = "invalid command"
    return current_address, result
