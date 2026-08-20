import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.services_manager import ServiceManager

def test_service_manager():
    sm = ServiceManager()

    sm.register("logger", "LoggerObject")

    assert sm.exists("logger")
    assert sm.get("logger") == "LoggerObject"

    print("✓ ServiceManager test passed")

if __name__ == "__main__":
    test_service_manager()
