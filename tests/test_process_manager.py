import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.event_bus import EventBus
from process.manager import ProcessManager

def test_process_manager():
    bus = EventBus()
    pm = ProcessManager(bus)

    pm.create_process("chrome")

    assert "chrome" in pm.list_processes()

    pm.kill_process("chrome")

    assert "chrome" not in pm.list_processes()

    print("✓ ProcessManager test passed")

if __name__ == "__main__":
    test_process_manager()
