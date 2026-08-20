"""
Gorgon OS Shutdown Manager
"""

class ShutdownManager:

    def __init__(self, service_manager):

        self.service_manager = service_manager

    def shutdown(self):

        print("[SYSTEM] Shutdown requested")

        filesystem = (
            self.service_manager.get(
                "filesystem"
            )
        )

        if filesystem:

            filesystem.save()

            print(
                "[SYSTEM] Filesystem saved"
            )

        print(
            "[SYSTEM] Shutdown complete"
        )
