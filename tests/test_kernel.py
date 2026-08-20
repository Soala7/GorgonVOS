import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kernel.kernel import Kernel

def test_kernel():
    kernel = Kernel()
    kernel.boot()

    sm = kernel.service_manager

    assert sm.exists("logger")
    assert sm.exists("event_bus")
    assert sm.exists("filesystem")
    assert sm.exists("process")

    print("✓ Kernel test passed")

if __name__ == "__main__":
    test_kernel()
