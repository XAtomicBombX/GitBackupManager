from time import sleep

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
        print("[GBM]正在初始化.git文件夹...")
        repo = Repo.init(Configure.server_path)
        print("[GBM]初始化完成")


def create_backup():
    pass


def creat_backup() -> None:
    pass


def auto_creat_backup(custom_time=0, default_time=1800, state=True) -> None:
    """git add and git commit"""
    creat_backup()
    if custom_time == 0:
        sleep(default_time)
    else:
        sleep(custom_time)
    auto_creat_backup()


def timer(time: int) -> None:
    """
    当执行这个函数时，该线程暂停time秒
    :param time:
    :return: None
    """
    sleep(time)


def register_command(server: PluginServerInterface) -> None:
    """
    实现以下命令:
    !!gb-init
        -make [comment: str]
        -back [id: str]
        -confirm
        -about
        -list
        -remote
            -enable
            -disable
            -address [address: str]
    :return:None
    """
    server.register_command(
        Literal("!!gb").
        then(
            Literal("init")
        ).
        then(
            Literal("make").
            then(
                GreedyText("comment")
            )
        ).
        then(
            Literal("back").
            then(
                Integer("id")
            )
        ).
        then(
            Literal("confirm")
        ).
        then(
            Literal("about")
        ).
        then(
            Literal("list")
        ).
        then(
            Literal("remote").
            then(
                Literal("enable")
            ).
            then(
                Literal("disable")
            ).
            then(
                Literal("address").
                then(
                    GreedyText("address")
                )
            )
        )
    )
