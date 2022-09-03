from mcdreforged.api.all import *
from git import Repo, InvalidGitRepositoryError
from git_backup_mgr.config import Configure

repo: Repo
git: Repo.git
remote: Repo.remote
config: Configure
CONFIG_FILE_NAME: str = "GitBackupManager.json"


class Events:
    backup_done = LiteralEvent("git_backup_manager.backup_done")
    backup_trig = LiteralEvent("git_backup_manager.backup_trig")
    restore_done = LiteralEvent("git_backup_manager.restore_done")
    restore_trig = LiteralEvent("git_backup_manager.restore_trig")


def load_config(server: PluginServerInterface):
    global config
    server.load_config_simple(file_name=CONFIG_FILE_NAME, default_config=Configure, target_class=Configure)


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
    global git
    git = repo.git
    if config.remote_backup:
        git.remote('add', 'origin', config.remote_origin)
        global remote
        remote = repo.remote()


@new_thread("GBM Backup Thread")
def create_backup(server: ServerInterface, comment) -> None:
    server.say("[GBM]正在备份...")
    for worlds in config.saves:
        git.add(worlds)
    while True:
        break
    git.commit('-m', comment)
    server.say("[GBM]备份完成!")
    if config.remote_backup:
        server.say("[GBM]正在上传...")
        try:
            git.push('master')
        except Exception:
            server.say(f"[GBM]发生错误!错误为:{Exception}")
            server.say("[GBM]请根据控制台日志排除错误原因!")
        else:
            server.say("[GBM]上传完成!")


"""此自动备份函数已弃用,新自动备份参见timer.py"""


# def auto_create_backup(custom_time=0, default_time=1800, state=True) -> None:
#     """git add and git commit"""
#     create_backup()
#     if custom_time == 0:
#         sleep(default_time)
#     else:
#         sleep(custom_time)
#     auto_create_backup()
#
#
# def timer(time: int) -> None:
#     """
#     当执行这个函数时，该线程暂停time秒
#     :param time:
#     :return: None
#     """
#     sleep(time)


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
            Literal("init").runs(git_init)
        ).
        then(
            Literal("make").
            then(
                GreedyText("comment").runs(lambda src, ctx: create_backup(src.get_server(), ctx["comment"]))
            )
        ).
        then(
            Literal("back").
            then(
                Text("version")
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
                    QuotableText("address")
                )
            )
        ).
        then(
            Literal("timed").
            then(
                Literal("enable")
            ).
            then(
                Literal("disable")
            ).
            then(
                Literal("overlay").
                then(Integer("overlay"))
            )
        )
    )
