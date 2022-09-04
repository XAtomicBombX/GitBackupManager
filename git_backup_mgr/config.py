from typing import List, Dict

from mcdreforged.utils.serializer import Serializable


class Configure(Serializable):
    """服务器位置"""
    server_path: str = "./server"
    """存档位置,有多个存档的情况可自行添加"""
    saves: List[str] = [
        'world'
    ]
    """各存档文件夹中忽略的文件"""
    ignored_files: List[str] = [
        'session.lock'
    ]
    saved_world_keywords: List[str] = [
        'Saved the game',  # 1.13+
        'Saved the world',  # 1.12-
    ]

    user_name: str = "ExampleUser"
    user_email: str = "example@example.com"

    remote_backup: bool = False  # 远程备份开关
    remote_origin: str = 'example.com'  # 远程Git仓库地址

    timed_backup: bool = True  # 自动备份开关
    backup_interval: float = 30.0  # 备份间隔(分钟)默认为30min

    permissions: Dict[str, int] = {
        'init': 2,
        'make': 1,
        'back': 2,
        'confirm': 1,
        'abort': 1,
        'list': 0,
        'remote': 3,
    }
