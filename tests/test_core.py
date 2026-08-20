import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.logger import Logger
from core.event_bus import EventBus
from core.services_manager import ServiceManager

def test_core_system():
    print("\n[TEST] Core System Boot Test")

    logger = Logger("Test")
    logger.info("Logger initialized")

    bus = EventBus()

    def handler(data):
        print("[EVENT RECEIVED]", data)

    bus.subscribe("test:event", handler)
    bus.emit("test:event", {"msg": "hello VOS"})

    sm = ServiceManager()
    class DummyService:
        def ping(self):
            return "pong"
    sm.register("dummy", DummyService())
    service = sm.get("dummy")

    assert service.ping() == "pong"

    print("[TEST PASSED] Core systems working correctly")

if __name__ == "__main__":
    test_core_system()
