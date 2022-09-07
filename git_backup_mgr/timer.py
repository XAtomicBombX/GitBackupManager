import time
from threading import Thread, Event

from mcdreforged.plugin.server_interface import PluginServerInterface

from git_backup_mgr import Events, broadcast_msg


class TimedBackup(Thread):
    def __init__(self, server: PluginServerInterface) -> None:
        super().__init__()
        self.daemon = True
        self.name = "GBM Timed Backup"
        self.time_last_backup = time.time()
        self.server = server
        self.is_enabled = False
        self.stop_event = Event()

    def set_enabled(self, value):
        self.is_enabled = value
        self.reset_timer()

    @staticmethod
    def get_interval():
        from git_backup_mgr import config
        return config.backup_interval * 60

    def reset_timer(self):
        self.time_last_backup = time.time()

    def broadcast_next_backup_time(self):
        next_backup_time = time.strftime("%Y/%m/%d %H:%M:%S",
                                         time.localtime(self.time_last_backup + self.get_interval()))
        broadcast_msg(self.server, f"下次自动备份时间:{next_backup_time}")

    def on_backup_created(self):
        broadcast_msg(self.server, "检测到新增备份,重置计时器")
        self.reset_timer()
        self.broadcast_next_backup_time()

    def run(self):
        while True:
            while True:
                if self.stop_event.wait(1):
                    return
                if time.time() - self.time_last_backup > self.get_interval():
                    break
            if self.is_enabled and self.server.is_server_startup():
                self.server.dispatch_event(Events.backup_trig, ())

    def stop(self):
        self.stop_event.set()
