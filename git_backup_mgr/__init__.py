from mcdreforged.api.all import *
from git import Repo
from git_backup_mgr.config import Configure

repo: Repo


def git_init() -> None:
    global repo
    repo = Repo(Configure.server_path)  # 使用Configure中的服务器目录初始化git
