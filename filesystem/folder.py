"""
VOS Virtual Filesystem
Folder representation.
"""
class Folder:

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

        self.files = {}
        self.folders = {}

    def add_file(self, name, content=""):
        self.files[name] = content

    def add_folder(self, folder):
        self.folders[folder.name] = folder

    def remove_file(self, name):
        if name in self.files:
            del self.files[name]

    def remove_folder(self, name):
        if name in self.folders:
            del self.folders[name]

    def get_folder(self, name):
        return self.folders.get(name)

    def list_contents(self):
        print("[FOLDER] folders:", self.folders)
        print("[FOLDER] files:", self.files)
        contents = []
        contents.extend(self.folders.keys())
        contents.extend(self.files.keys())
        return contents













        