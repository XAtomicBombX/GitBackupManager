import time
from threading import Thread

from mcdreforged.plugin.server_interface import PluginServerInterface

from git_backup_mgr import Events


class TimedBackup(Thread):
    def __init__(self, server: PluginServerInterface) -> None:
        super().__init__()
        self.daemon = True
        self.name = "GBM Timed Backup"
        self.time_last_backup = time.time()
        self.server = server
        self.is_enabled = False

    def get_interval(self):
        from git_backup_mgr import config
        return config.backup_interval * 60

    def auto_backup(self):
        while True:
            while True:
                if time.time() - self.time_last_backup > self.get_interval():
                    break
            if self.is_enabled and self.server.is_server_startup():
                self.server.dispatch_event(Events.backup_trig, ())

