class ProcessManager:
    def __init__(self, event_bus=None):
        self.processes = []
        self.event_bus = event_bus

    def create_process(self, name):
        self.processes.append(name)

        if self.event_bus:
            self.event_bus.emit("process_started", {"name": name})

    def kill_process(self, name):
        if name in self.processes:
            self.processes.remove(name)

            if self.event_bus:
                self.event_bus.emit("process_terminated", {"name": name})

    def list_processes(self):
        return self.processes
