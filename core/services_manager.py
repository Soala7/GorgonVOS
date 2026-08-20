class ServiceManager:
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services[name]

    def exists(self, name):
        return name in self._services

    def unregister(self, name):
        del self._services[name]

    def list_services(self):
        return list(self._services.keys())
