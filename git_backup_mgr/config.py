from typing import List, Dict

from mcdreforged.utils.serializer import Serializable


class Configure(Serializable):
    server_path: str = "./server"
    saves: List[str] = [
        'world'
    ]
    ignored_files: List[str] = [
        'session.lock'
    ]
    saved_world_keywords: List[str] = [
        'Saved the game',  # 1.13+
        'Saved the world',  # 1.12-
    ]

    remote_backup: bool = False  # 远程备份开关
    remote_origin: str = 'example.com'  # 远程Git仓库地址

    timed_backup = True  # 自动备份开关
    backup_interval = 30  # 备份间隔(分钟)默认为30min

    permissions: Dict[str, int] = {
        'init': 2,
        'make': 1,
        'back': 2,
        'confirm': 1,
        'abort': 1,
        'list': 0,
        'remote': 3,
    }
