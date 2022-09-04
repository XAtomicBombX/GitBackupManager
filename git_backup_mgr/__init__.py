import time

from mcdreforged.api.all import *
from git import Repo, InvalidGitRepositoryError
from git_backup_mgr.config import Configure

repo: Repo
git: Repo.git
remote: Repo.remote
config: Configure
CONFIG_FILE_NAME: str = "GitBackupManager.json"
game_saved: bool = False
plugin_unloaded: bool = False


class Events:
    backup_done = LiteralEvent("git_backup_mgr.backup_done")
    backup_trig = LiteralEvent("git_backup_mgr.backup_trig")
    restore_done = LiteralEvent("git_backup_mgr.restore_done")
    restore_trig = LiteralEvent("git_backup_mgr.restore_trig")


def load_config(server: PluginServerInterface):
    global config
    config = server.load_config_simple(file_name=CONFIG_FILE_NAME, target_class=Configure)


def print_msg(source: CommandSource, msg, prefix='[GBM]'):
    msg = RTextList(prefix, msg)
    if source.is_player:
        source.get_server().say(msg)
    else:
        source.reply(msg)


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
    git.config("user.name", f'"{config.user_name}"')
    git.config("user.email", f'"{config.user_email}"')
    if config.remote_backup:
        git.remote('add', 'origin', config.remote_origin)
        global remote
        remote = repo.remote()
    with open((config.server_path+'/.gitignore'), 'w+') as f:
        for i in config.saves:
            for j in config.ignored_files:
                f.write(f"{i}/{j}\n")


@new_thread("GBM Backup Thread")
def create_backup(source: CommandSource, comment='无') -> None:
    try:
        print_msg(source, "[GBM]正在备份...")
        source.get_server().execute("save-off")
        source.get_server().execute("save-all flush")
        while True:
            time.sleep(0.01)
            if game_saved:
                break
            if plugin_unloaded:
                print_msg(source, "插件被卸载,备份取消")
                return
        for worlds in config.saves:
            git.add(worlds)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        comment = f"{t} 备注:{comment}"
        git.commit('-m', comment)
        print_msg(source, "备份完成!")
        if config.remote_backup:
            print_msg(source, "正在上传...")
            git.push('master')
            print_msg(source, "上传完成!")
    except Exception as e:
        print_msg(source, f"发生错误!错误为:{e}")
        print_msg(source, "请根据控制台日志排除错误原因!")
    else:
        pass  # 此处应发出事件Events.backup_done WIP
    finally:
        source.get_server().execute("save-on")


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
            Literal("make").runs(lambda src: create_backup(src)).
            then(
                GreedyText("comment").runs(lambda src, ctx: create_backup(src, ctx["comment"]))
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


def on_load(server: ServerInterface, prev):
    load_config(server.as_plugin_server_interface())
    git_init()
    register_command(server.as_plugin_server_interface())
