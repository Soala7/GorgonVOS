# runtime/startup.py

from core.logger import Logger


class StartupManager:
    """
    Controls full VOS startup sequence.
    This is the final stage of boot after Kernel initialization.
    """

    def __init__(self, kernel, runtime_manager):
        self.kernel = kernel
        self.runtime = runtime_manager

        self.logger = Logger("Startup")

    # ----------------------------
    # MAIN BOOT SEQUENCE
    # ----------------------------
    def start(self):
        self.logger.info("Starting VOS Runtime Startup Sequence...")

        # Step 1: Validate Kernel services
        self._validate_services()

        # Step 2: Start Runtime
        self.runtime.start()

        # Step 3: Create default session
        self._create_default_session()

        # Step 4: Register default apps
        self._register_default_apps()

        # Step 5: Launch desktop (placeholder for now)
        self._launch_desktop()

        self.logger.info("VOS Startup Complete.")

    # ----------------------------
    # SERVICE VALIDATION
    # ----------------------------
    def _validate_services(self):
        self.logger.info("Validating Kernel services...")

        required = [
            "event_bus",
            "service_manager",
            "logger"
        ]

        for service in required:
            if not self.kernel.service_manager.get(service):
                raise Exception(f"Missing critical service: {service}")

        self.logger.info("All Kernel services validated.")

    # ----------------------------
    # DEFAULT SESSION
    # ----------------------------
    def _create_default_session(self):
        self.logger.info("Creating default session...")

        session_manager = self.runtime.session_manager

        # Default user (for now)
        session_manager.create_session("default_user")

    # ----------------------------
    # DEFAULT APPLICATIONS
    # ----------------------------
    def _register_default_apps(self):
        self.logger.info("Registering default applications...")

        app_manager = self.runtime.app_manager

        # Temporary placeholder apps
        app_manager.register_app("browser", lambda: print("Browser started"))
        app_manager.register_app("calculator", lambda: print("Calculator started"))
        app_manager.register_app("terminal", lambda: print("Terminal started"))
        app_manager.register_app("explorer", lambda: print("File Explorer started"))
        app_manager.register_app("text_editor", lambda: print("Text Editor started"))

    # ----------------------------
    # DESKTOP BOOT
    # ----------------------------
    def _launch_desktop(self):
        self.logger.info("Launching Desktop Environment...")

        # Placeholder until desktop system is built
        self.kernel.service_manager.get("event_bus").emit(
            "desktop:start",
            {"status": "launching"}
        )