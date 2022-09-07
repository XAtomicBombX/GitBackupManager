from mcdreforged.plugin.plugin_event import LiteralEvent


class Events:
    backup_done = LiteralEvent("git_backup_mgr.backup_done")
    backup_trig = LiteralEvent("git_backup_mgr.backup_trig")
    restore_done = LiteralEvent("git_backup_mgr.restore_done")
    restore_trig = LiteralEvent("git_backup_mgr.restore_trig")
