"""
VOS Virtual Filesystem

Manages files and folders inside the virtual operating system.
"""
import os

from .folder import Folder
from .storage import FileSystemStorage

class FileSystem:

    def __init__(self, event_bus=None):

        self.event_bus = event_bus

        self.storage = FileSystemStorage()

        base_path = os.path.dirname(
            os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        
        self.save_path = os.path.join(
            base_path,
            "data",
            "VOS.os"
        )

        loaded = self.storage.load(
            self.save_path
        )


        if loaded:

            print("[FILESYSTEM] Restoring saved filesystem")

            self.root = loaded

        else:

            print(
                "[FILESYSTEM] Creating new filesystem"
            )

            self.root = Folder("/")

            self._create_default_structure()


        self.current_directory = self.root
    def _create_default_structure(self):
        """
        Creates the default VOS directory structure.
        """

        self.create_folder("/apps")
        self.create_folder("/home")
        self.create_folder("/system")
        self.create_folder("/temp")
        self.create_folder("/users")

        # Default user
        self.create_folder("/users/guest")

    def get_current_path(self):

        path = []

        current = self.current_directory


        while current.parent is not None:

            path.append(current.name)

            current = current.parent


        return "/" + "/".join(
            reversed(path)
        )
    
    def create_folder(self, path):
        """
        Creates a folder at the given path.
        Supports both absolute and relative paths.
        """

        print(f"[FILESYSTEM] create folder request: {path}")


        if path.startswith("/"):
            current = self.root
        else:
            current = self.current_directory


        parts = self._split_path(path)


        for part in parts:

            if part not in current.folders:

                new_folder = Folder(
                    part,
                    parent=current
                )

                current.add_folder(
                    new_folder
                )

                print(
                    f"[FILESYSTEM] created folder: {part}"
                )


            current = current.folders[part]


        if self.event_bus:
            self.event_bus.emit(
                "folder_created",
                {"path": path}
            )


        return True

    def create_file(self, path, content=""):
        """
        Creates a file in the current directory or specified path.
        """

        print(f"[FILESYSTEM] create file request: {path}")


        parts = self._split_path(path)


        filename = parts.pop()


        if path.startswith("/"):
            current = self.root
        else:
            current = self.current_directory



        # Move into target folder if needed
        for part in parts:

            if part not in current.folders:
                print(
                    "[FILESYSTEM] folder not found:",
                    part
                )
                return False


            current = current.folders[part]



        # Check existing file
        if filename in current.files:

            print(
                "[FILESYSTEM] file already exists"
            )

            return False



        current.add_file(
            filename,
            content
        )


        print(
            f"[FILESYSTEM] created file: {filename}"
        )


        return True

    def change_directory(self, path):
        """
        Changes the current working directory.
        """

        print("[FILESYSTEM] cd request:", path)

        # Parent directory
        if path == "..":

            if self.current_directory.parent is not None:
                self.current_directory = self.current_directory.parent

            return True


        # Root directory
        if path == "/":

            self.current_directory = self.root

            return True


        folder = self._get_folder(
            self._resolve_path(path)
        )

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


    def write_file(self, path, content):

        print("[FILESYSTEM] write file request:", path)

        path = self._resolve_path(path)

        folder_path, filename = self._split_file_path(path)

        folder = self._get_folder(folder_path)

        if folder is None:
            return False

        if filename not in folder.files:
            return False

        folder.files[filename] = content

        return True

    def read_file(self, path):
    
            path = self._resolve_path(path)
    
            folder_path, filename = self._split_file_path(path)
    
            folder = self._get_folder(folder_path)
    
            if folder is None:
                return None
    
            return folder.files.get(filename)

    def delete_file(self, path):

        folder_path, filename = self._split_file_path(path)

        folder = self._get_folder(folder_path)

        if folder and filename in folder.files:

            folder.remove_file(filename)


            if self.event_bus:
                self.event_bus.emit(
                    "file_deleted",
                    {"path": path}
                )

            return True


        return False

    def delete_folder(self, path):

        print(
            "[FILESYSTEM] delete folder request:",
            path
        )


        path = self._resolve_path(path)

        folder_path, folder_name = self._split_file_path(path)


        parent_folder = self._get_folder(
            folder_path
        )


        if parent_folder is None:
            return False


        if folder_name not in parent_folder.folders:
            return False


        folder = parent_folder.folders[folder_name]


        # Prevent deleting non-empty folders
        if folder.files or folder.folders:
            print(
                "[FILESYSTEM] folder not empty"
            )

            return False


        parent_folder.remove_folder(
            folder_name
        )


        print(
            "[FILESYSTEM] deleted folder:",
            folder_name
        )


        return True

    def list_directory(self, path=None):
        """
        Lists contents of a directory.
        """

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

            lines.append(
                f"{prefix}{name}/"
            )

            lines.extend(
                self.get_tree(
                    subfolder,
                    prefix + "    "
                )
            )


        for filename in folder.files:

            lines.append(
                f"{prefix}{filename}"
            )


        return lines

    def move_file(self, source, destination):

        print(
            "[FILESYSTEM] move request:",
            source,
            "->",
            destination
        )


        source = self._resolve_path(source)
        destination = self._resolve_path(destination)


        src_folder_path, filename = self._split_file_path(source)

        src_folder = self._get_folder(
            src_folder_path
        )


        if src_folder is None:
            return False


        if filename not in src_folder.files:
            return False


        content = src_folder.files[filename]


        dst_folder_path, dst_filename = self._split_file_path(destination)

        dst_folder = self._get_folder(
            dst_folder_path
        )


        if dst_folder is None:
            return False


        if dst_filename in dst_folder.files:
            return False


        # remove from old folder
        del src_folder.files[filename]


        # add to new folder
        dst_folder.files[dst_filename] = content


        print(
            "[FILESYSTEM] moved:",
            filename
        )


        return True

    def copy_file(self, source, destination):

        print(
            "[FILESYSTEM] copy request:",
            source,
            "->",
            destination
        )


        source = self._resolve_path(source)
        destination = self._resolve_path(destination)


        src_folder_path, filename = self._split_file_path(source)

        src_folder = self._get_folder(
            src_folder_path
        )


        if src_folder is None:
            return False


        if filename not in src_folder.files:
            return False


        content = src_folder.files[filename]


        dst_folder_path, dst_filename = self._split_file_path(destination)

        dst_folder = self._get_folder(
            dst_folder_path
        )


        if dst_folder is None:
            return False


        if dst_filename in dst_folder.files:
            return False


        dst_folder.files[dst_filename] = content


        print(
            "[FILESYSTEM] copied:",
            filename
        )


        return True

    def _load_or_create(self):

        loaded = self.storage.load(
            self.save_path
        )


        if loaded:

            print(
                "[FILESYSTEM] Restoring saved filesystem"
            )

            self.root = loaded
            self.current_directory = self.root

            return


        print(
            "[FILESYSTEM] Creating new filesystem"
        )


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
    
    def save(self):

        self.storage.save(
            self.root,
            self.save_path
        )