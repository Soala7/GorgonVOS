"""
VOS Virtual Filesystem

Manages files and folders inside the virtual operating system.
"""
import os

from .folder import Folder
from .storage import FileSystemStorage
from .disk import VirtualDisk

class FileSystem:
    def __init__(self, event_bus=None):
        self.event_bus = event_bus
        self.disk = VirtualDisk()
        self.storage = FileSystemStorage(self.disk)

        base_path = os.path.dirname(
            os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        self.save_path = os.path.join(base_path,"data","VOS.os")
        loaded = self.storage.load(self.save_path)
        if loaded:
            self.root = loaded
        else:
            self.root = Folder("/")
            self._create_default_structure()
        self.current_directory = self.root

    def _default_directories(self):
        directories = ["apps","home","system", "temp", "users"]
        for dir in directories:
            dirs = "/" + dir
            self.create_folder(dirs)

    def _default_user_directories(self):
        user_directory = ["Documents", "Downloads", "Pictures", "Videos", "Music", "Storage", "Trash"]
        for users in user_directory:
            user_dirs = "/users/guest/" + users
            self.create_folder(user_dirs)

    def _create_default_structure(self):
        self._default_user_directories()
        self._default_directories()

    def get_current_path(self):
        path = []
        current = self.current_directory
        while current.parent is not None:
            path.append(current.name)
            current = current.parent
        return "/" + "/".join(reversed(path))

    def create_folder(self, path):

        if path.startswith("/"):
            current = self.root
        else:
            current = self.current_directory

        parts = self._split_path(path)
        for part in parts:
            if part not in current.folders:
                new_folder = Folder(part,parent=current)
                current.add_folder(new_folder)
                print(f"[FILESYSTEM] created folder: {part}")
            current = current.folders[part]

        if self.event_bus:
            self.event_bus.emit("folder_created",{"path": path})

        return True

    def create_file(self, path, content=""):

        print(f"[FILESYSTEM] create file request: {path}")
        parts = self._split_path(path)
        filename = parts.pop()

        if path.startswith("/"):
            current = self.root
        else:
            current = self.current_directory

        for part in parts:
            if part not in current.folders:
                print("[FILESYSTEM] folder not found:",part)
                return False

            current = current.folders[part]

        if filename in current.files:
            print("[FILESYSTEM] file already exists")
            return False
        current.add_file(filename)
        self.disk.create_file(path, content)
        print(f"[FILESYSTEM] created file: {filename}")
        return True

    def change_directory(self, path):

        print("[FILESYSTEM] cd request:", path)

        if path == "..":
            if self.current_directory.parent is not None:
                self.current_directory = self.current_directory.parent

            return True

        if path == "/":
            self.current_directory = self.root
            return True

        folder = self._get_folder(self._resolve_path(path))
        print("[FILESYSTEM] found folder:", folder)
        if folder is None:
            return False

        self.current_directory = folder
        return True

    def _resolve_path(self, path):
        if path.startswith("/"):
            return path
        current = self.get_current_path()
        if current == "/":
            return "/" + path

        return current + "/" + path

    def read_file(self, path):
        path = self._resolve_path(path)
        if path not in self.disk.file_table:
            return None
        data = self.disk.read_file(path)
        return data

    def delete_file(self, path):
        path = self._resolve_path(path)
        folder_path, filename = self._split_file_path(path)
        folder = self._get_folder(folder_path)
        if folder is None:
            return False
        if filename not in folder.files:
            return False
        if path not in self.disk.file_table:
            return False
        if not self.disk.delete_file(path):
            return False
        folder.remove_file(filename)
        if self.event_bus:
            self.event_bus.emit("file_deleted",{"path": path})
        return True

    def delete_folder(self, path):
        print("[FILESYSTEM] delete folder request:",path)
        path = self._resolve_path(path)
        folder_path, folder_name = self._split_file_path(path)
        parent_folder = self._get_folder(folder_path)
        if parent_folder is None:
            return False
        if folder_name not in parent_folder.folders:
            return False
        folder = parent_folder.folders[folder_name]

        if folder.files or folder.folders:
            print("[FILESYSTEM] folder not empty")
            return False

        parent_folder.remove_folder(folder_name)
        print("[FILESYSTEM] deleted folder:",folder_name)
        return True

    def list_directory(self, path=None):

        if path is None or path == "":
            return self.current_directory.list_contents()
        folder = self._get_folder(path)
        if folder:
            return folder.list_contents()
        return None

    def get_tree(self, folder=None, prefix=""):
        if folder is None:
            folder = self.root
        lines = []
        for name, subfolder in folder.folders.items():
            lines.append(f"{prefix}{name}/")
            lines.extend(self.get_tree(subfolder,prefix + "    "))
        for filename in folder.files:
            lines.append(f"{prefix}{filename}")
        return lines

    def move_file(self, source, destination):
        print("[FILESYSTEM] move request:",source,"->",destination)

        source = self._resolve_path(source)
        destination = self._resolve_path(destination)
        src_folder_path, filename = self._split_file_path(source)
        src_folder = self._get_folder(src_folder_path)

        if src_folder is None:
            return False

        if filename not in src_folder.files:
            return False

        content = self.disk.read_file(source)
        dst_folder_path, dst_filename = self._split_file_path(destination)
        dst_folder = self._get_folder(dst_folder_path)

        if dst_folder is None:
            return False

        if dst_filename in dst_folder.files:
            return False
        self.disk.delete_file(source)
        self.disk.create_file(destination, content)
        del src_folder.files[filename]
        dst_folder.files[dst_filename] = content
        print("[FILESYSTEM] moved:",filename)
        return True

    def rename_file(self, source, destination):
        print("[FILESYSTEM] rename request:", source, "->", destination)
        source = self._resolve_path(source)

        if "/" not in destination:
            src_folder_path, filename = self._split_file_path(source)
            destination = (
                src_folder_path
                + ("/" if src_folder_path != "/" else "")
                + destination
            )
        else:
            destination = self._resolve_path(destination)

        src_folder_path, filename = self._split_file_path(source)
        src_folder = self._get_folder(src_folder_path)

        if src_folder is None or filename not in src_folder.files:
            return False

        dst_folder_path, dst_filename = self._split_file_path(destination)
        dst_folder = self._get_folder(dst_folder_path)

        if dst_folder is None:
            return False

        if dst_filename in dst_folder.files:
            return False

        content = self.disk.read_file(source)

        self.disk.delete_file(source)
        self.disk.create_file(destination, content)

        src_folder.remove_file(filename)
        dst_folder.add_file(dst_filename, content)

        if self.event_bus:
            self.event_bus.emit(
                "file_renamed",
                {
                    "old_path": source,
                    "new_path": destination
                }
            )

        print("[FILESYSTEM] renamed:", filename, "->", dst_filename)
        return True

    def copy_file(self, source, destination):
        print("[FILESYSTEM] copy request:",source,"->",destination)

        source = self._resolve_path(source)
        destination = self._resolve_path(destination)
        src_folder_path, filename = self._split_file_path(source)
        src_folder = self._get_folder(src_folder_path)
        if src_folder is None:
            return False
        if filename not in src_folder.files:
            return False
        content = self.disk.read_file(source)
        dst_folder_path, dst_filename = self._split_file_path(destination)
        dst_folder = self._get_folder(dst_folder_path)
        if dst_folder is None:
            return False
        if dst_filename in dst_folder.files:
            return False
        self.disk.create_file(destination, content)
        dst_folder.files[dst_filename] = content
        print("[FILESYSTEM] copied:",filename)
        return True

    def _load_or_create(self):
        loaded = self.storage.load(self.save_path)
        if loaded:
            print("[FILESYSTEM] Restoring saved filesystem")
            self.root = loaded
            self.current_directory = self.root
            return
        print("[FILESYSTEM] Creating new filesystem")
        self.root = Folder("/")
        self.current_directory = self.root
        self._create_default_structure()
        self.save()

    def _split_path(self, path):
        return [
            part
            for part in path.split("/")
            if part
        ]

    def _split_file_path(self, path):
        parts = self._split_path(path)
        filename = parts.pop()
        folder_path = "/" + "/".join(parts)
        return folder_path, filename

    def _get_folder(self, path):
        if path == "/":
            return self.root
        parts = self._split_path(path)
        current = self.root
        for part in parts:
            if part not in current.folders:
                return None
            current = current.folders[part]
        return current

    def get_special_folder(self, key):

        mapping = {
            "explorer/documents": "/users/guest/Documents",
            "explorer/downloads": "/users/guest/Downloads",
            "explorer/photo": "/users/guest/Pictures",
            "explorer/videos": "/users/guest/Videos",
            "explorer/musics": "/users/guest/Music",
            "explorer/storages": "/users/guest",
            "explorer/trashs": "/users/guest/Trash",
            "explorer/computer": "/",
        }
        path = mapping.get(key)
        if path is None:
            return None
        return self._get_folder(path)
    def save(self):self.storage.save(self.root,self.save_path)
