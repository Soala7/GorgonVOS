import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.event_bus import EventBus
from filesystem.filesystem import FileSystem

def test_filesystem():
    bus = EventBus()
    fs = FileSystem(bus)

    fs.create_file("/hello.txt", "Hello VOS")

    assert fs.read_file("/hello.txt") == "Hello VOS"

    fs.delete_file("/hello.txt")

    assert fs.read_file("/hello.txt") is None

    print("✓ FileSystem test passed")
if __name__ == "__main__":
    test_filesystem()
