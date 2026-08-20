class EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_name, handler):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(handler)

    def emit(self, event_name, data=None):
        if data is None:
            data = {}

        if event_name not in self._listeners:
            return
        event = {
            "name": event_name,
            "data": data
        }

        for handler in self._listeners[event_name]:
            handler(event)

    def unsubscribe(self, event_name, handler):
        if event_name in self._listeners:
            self._listeners[event_name].remove(handler)

    def clear(self, event_name):
        self._listeners[event_name] = []
