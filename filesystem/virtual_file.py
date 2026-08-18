class VirtualFile:

    def __init__(self, name, content=""):
        self.name = name
        self.content = content

    def read_text(self):
        return self.content

    def write_text(self, new_content):
        self.content = new_content