import sys
import os


# Add VOS root directory to Python path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from filesystem.filesystem import FileSystem
from filesystem.storage import FileSystemStorage


fs = FileSystem()

fs.create_file(
    "/hello.txt",
    "Hello from saved VOS"
)


storage = FileSystemStorage()


storage.save(
    fs.root,
    "test.os"
)


loaded_root = storage.load(
    "test.os"
)


print(
    loaded_root.files
)

fs.create_file(
    "/saved.txt",
    "Persistence works"
)

fs.save()
