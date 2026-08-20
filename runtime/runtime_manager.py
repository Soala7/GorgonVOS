from core.logger import Logger
from core.event_bus import EventBus
from core.services_manager import ServiceManager

class RuntimeManager:
    def __init__(self, kernel):
        self.kernel = kernel
        self.logger = Logger("Runtime")

        self.event_bus: EventBus = self.kernel.service_manager.get("event_bus")
        self.service_manager: ServiceManager = self.kernel.service_manager

        self.process_table = None
        self.session_manager = None
        self.app_manager = None

        self.state = "STOPPED"

    def start(self):
        self.logger.info("Runtime starting...")

        self.state = "STARTING"

        self._init_process_table()
        self._init_session_manager()
        self._init_app_manager()

        self.event_bus.emit("runtime:ready", {})

        self.state = "RUNNING"

        self.logger.info("Runtime fully started.")

    def shutdown(self):
        self.logger.info("Runtime shutting down...")

        self.state = "STOPPING"

        if self.app_manager:
            self.app_manager.shutdown_all()

        if self.session_manager:
            self.session_manager.close_all_sessions()

        if self.process_table:
            self.process_table.clear()

        self.state = "STOPPED"

        self.logger.info("Runtime stopped.")

    def _init_process_table(self):
        from runtime.process_table import ProcessTable
        self.process_table = ProcessTable(self.event_bus)
        self.service_manager.register("process_table", self.process_table)
        self.logger.info("Process Table initialized.")

    def _init_session_manager(self):
        from runtime.session_manager import SessionManager
        self.session_manager = SessionManager(self.event_bus, self.process_table)
        self.service_manager.register("session_manager", self.session_manager)
        self.logger.info("Session Manager initialized.")

    def _init_app_manager(self):
        from runtime.app_manager import AppManager
        self.app_manager = AppManager(self.event_bus, self.process_table)
        self.service_manager.register("app_manager", self.app_manager)
        self.logger.info("Application Manager initialized.")
