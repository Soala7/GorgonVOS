import pygame

from filesystem.filesystem import FileSystem
from apps.explorer.explorer_window import ExplorerWindow
from desktop.ui.window.window_manager import WindowManager

pygame.init()

print("========== EXPLORER → EDITOR TEST ==========")

fs = FileSystem()

documents = fs.get_special_folder("explorer/documents")

documents.files["editor_test.txt"] = "Hello from VOS!"

print("Documents files:", documents.files)

window_manager = WindowManager()
explorer = ExplorerWindow(window_manager)

explorer.current_folder = documents

items = explorer._get_folder_items(documents)

test_file = None

for item in items:
    if getattr(item, "name", "") == "editor_test.txt":
        test_file = item
        break

print("Found file:", test_file is not None)

if test_file is not None:
    print("File name:", test_file.name)
    print("File content:", test_file.content)

    explorer.open_item(test_file)

print("============================================")

pygame.quit()
