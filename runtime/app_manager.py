

from core.logger import Logger

class App:
    """
    Represents a registered application in VOS.
    """

    def __init__(self, name, entry_point, app_type="native"):
        self.name = name
        self.entry_point = entry_point
        self.app_type = app_type

        self.is_running = False
        self.process = None

class AppManager:
    """
    Manages all applications inside VOS.
    Responsible for registering and launching apps.
    """

    def __init__(self, event_bus, process_table, session_manager=None):
        self.logger = Logger("AppManager")

        self.event_bus = event_bus
        self.process_table = process_table
        self.session_manager = session_manager

        self.apps = {}
        self.running_apps = {}

    def register_app(self, name, entry_point, app_type="native"):
        if name in self.apps:
            self.logger.warning(f"App already registered: {name}")
            return

        app = App(name, entry_point, app_type)
        self.apps[name] = app

        self.logger.info(f"App registered: {name}")

        if self.event_bus:
            self.event_bus.emit("app:registered", {"name": name})

    def launch_app(self, name, *args, **kwargs):
        app = self.apps.get(name)

        if not app:
            self.logger.error(f"App not found: {name}")
            return None

        self.logger.info(f"Launching app: {name}")

        process = self.process_table.create_process(
            name=name,
            process_type="app",
            instance=app
        )

        app.is_running = True
        app.process = process

        self.running_apps[process.pid] = app

        if self.session_manager and self.session_manager.active_session:
            self.session_manager.active_session.add_process(process.pid)

        try:
            if callable(app.entry_point):
                app.entry_point(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"App crashed: {name} -> {e}")
            process.terminate()

        if self.event_bus:
            self.event_bus.emit("app:launched", {
                "name": name,
                "pid": process.pid
            })

        return process

    def close_app(self, pid):
        app = self.running_apps.get(pid)

        if not app:
            self.logger.error(f"No running app with PID: {pid}")
            return False

        self.logger.info(f"Closing app: {app.name}")

        app.is_running = False

        self.process_table.terminate_process(pid)

        if self.session_manager and self.session_manager.active_session:
            self.session_manager.active_session.remove_process(pid)

        del self.running_apps[pid]

        if self.event_bus:
            self.event_bus.emit("app:closed", {
                "pid": pid,
                "name": app.name
            })

        return True

    def list_apps(self):
        return list(self.apps.keys())

    def list_running_apps(self):
        return {
            pid: app.name for pid, app in self.running_apps.items()
        }
