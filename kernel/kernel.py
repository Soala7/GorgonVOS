from core.services_manager import ServiceManager
from core.logger import Logger
from core.event_bus import EventBus
from resources.resource_manager import ResourceManager
from filesystem.filesystem import FileSystem
from bridge.vos_api import vos_api
from process.manager import ProcessManager
from kernel.shutdown_manager import ShutdownManager

class Kernel:
    def __init__(self):
        self.service_manager = ServiceManager()
        self.event_bus = EventBus()
        self.resources = ResourceManager()


    def boot(self):
        logger = Logger("Kernel")

        # Register core services first
        self.service_manager.register("logger", logger)
        self.service_manager.register("event_bus", self.event_bus)

        logger.info("Boot sequence starting...")

        # Register subsystems (event-aware)
        self._register_core_services()

        # Setup event listeners
        self._setup_event_system()

        logger.info("Kernel boot complete.")

    def _register_core_services(self):

        sm = self.service_manager
        logger = sm.get("logger")


        filesystem = FileSystem(
            self.event_bus
        )

        process_manager = ProcessManager(
            self.event_bus
        )


        sm.register(
            "filesystem",
            filesystem
        )


        sm.register(
            "process",
            process_manager
        )


        vos_api.register_filesystem(
            filesystem
        )


        sm.register(
            "vos_api",
            vos_api
        )


        logger.info(
            "Core services registered."
        )

        shutdown_manager = ShutdownManager(
            sm
        )


        sm.register(
            "shutdown",
            shutdown_manager
        )

    def shutdown(self):

        logger = self.service_manager.get("logger")

        logger.info("Shutdown requested")

        filesystem = self.service_manager.get("filesystem")

        if filesystem:
            filesystem.save()
            print("[SYSTEM] Filesystem saved")

        logger.info("Shutdown complete")

    def _setup_event_system(self):
        bus = self.event_bus
        logger = self.service_manager.get("logger")

        def on_file_created(event):
            logger.info(f"File created: {event['data']['path']}")

        def on_file_deleted(event):
            logger.warning(f"File deleted: {event['data']['path']}")

        def on_process_started(event):
            logger.info(f"Process started: {event['data']['name']}")

        def on_process_terminated(event):
            logger.warning(f"Process terminated: {event['data']['name']}")

        bus.subscribe("file_created", on_file_created)
        bus.subscribe("file_deleted", on_file_deleted)
        bus.subscribe("process_started", on_process_started)
        bus.subscribe("process_terminated", on_process_terminated)
