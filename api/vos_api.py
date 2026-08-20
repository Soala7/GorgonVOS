"""
VOS API

Provides controlled access to kernel services.
"""

class VOSAPI:

    def __init__(self, kernel):
        self._kernel = kernel

    def get_service(self, name):
        """
        Returns a registered kernel service.
        """

        return self._kernel.service_manager.get(name)

    @property
    def filesystem(self):
        return self.get_service("filesystem")

    @property
    def logger(self):
        return self.get_service("logger")

    @property
    def event_bus(self):
        return self.get_service("event_bus")

    @property
    def process_manager(self):
        return self.get_service("process")
