from mcdreforged.api.all import *
from git import Repo, InvalidGitRepositoryError
from git_backup_mgr.config import Configure

repo: Repo


def git_init() -> None:
    """
    当不存在.git路径时自动init
    :return:None
    """
    global repo
    try:
        repo = Repo(Configure.server_path)
    except InvalidGitRepositoryError:
        repo = Repo.init(Configure.server_path)


def create_backup():
    pass
