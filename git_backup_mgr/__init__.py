from mcdreforged.api.all import *
from git import Repo
from git_backup_mgr.config import Configure

repo: Repo


def git_init() -> None:
    global repo
    repo = Repo(Configure.server_path)  # 使用Configure中的服务器目录初始化git


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
