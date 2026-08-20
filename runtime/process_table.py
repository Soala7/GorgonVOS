

import time
from core.logger import Logger

class Process:
    """
    Represents a single VOS process.
    """

    def __init__(self, pid, name, owner="system", priority="normal", process_type="app", instance=None):
        self.pid = pid
        self.name = name
        self.owner = owner
        self.priority = priority
        self.process_type = process_type
        self.instance = instance

        self.state = "CREATED"
        self.created_at = time.time()
        self.start_time = None
        self.end_time = None

        self.cpu_usage = 0
        self.memory_usage = 0

    def start(self):
        self.state = "RUNNING"
        self.start_time = time.time()

    def suspend(self):
        self.state = "SUSPENDED"

    def resume(self):
        self.state = "RUNNING"

    def terminate(self):
        self.state = "TERMINATED"
        self.end_time = time.time()

class ProcessTable:
    """
    Central registry of all running VOS processes.
    """

    def __init__(self, event_bus=None):
        self.logger = Logger("ProcessTable")
        self.event_bus = event_bus

        self.processes = {}
        self.next_pid = 1

    def create_process(self, name, owner="system", priority="normal", process_type="app", instance=None):
        pid = self.next_pid
        self.next_pid += 1

        process = Process(
            pid=pid,
            name=name,
            owner=owner,
            priority=priority,
            process_type=process_type,
            instance=instance
        )

        self.processes[pid] = process
        process.start()

        self.logger.info(f"Process created: {name} (PID {pid})")

        if self.event_bus:
            self.event_bus.emit("process:created", {
                "pid": pid,
                "name": name
            })

        return process

    def terminate_process(self, pid):
        process = self.processes.get(pid)

        if not process:
            self.logger.error(f"Process {pid} not found")
            return False

        process.terminate()
        self.logger.info(f"Process terminated: {pid}")

        if self.event_bus:
            self.event_bus.emit("process:terminated", {"pid": pid})

        return True

    def suspend_process(self, pid):
        process = self.processes.get(pid)

        if not process:
            return False

        process.suspend()
        self.logger.info(f"Process suspended: {pid}")

        return True

    def resume_process(self, pid):
        process = self.processes.get(pid)

        if not process:
            return False

        process.resume()
        self.logger.info(f"Process resumed: {pid}")

        return True

    def get_process(self, pid):
        return self.processes.get(pid)

    def list_processes(self):
        return list(self.processes.values())

    def clear(self):
        self.logger.info("Clearing all processes...")
        self.processes.clear()
        self.next_pid = 1
