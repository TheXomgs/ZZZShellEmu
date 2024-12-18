from config import get_config
from dataclasses import dataclass

@dataclass
class SysInfo:
    fs_path: str
    hostname: str
    log_path: str
    startup_path: str
    cwd: str

_sys_info = None

def get_sys_info():
    global _sys_info
    if not _sys_info:
        config = get_config('config.ini')
        _sys_info = SysInfo(
            fs_path=config.get("config", "fs"),
            hostname=config.get("config", "hostname"),
            log_path=config.get("config", "log"),
            startup_path=config.get("config", "startup"),
            cwd="/"
        )
    return _sys_info

def get_cwd():
    sys_info = get_sys_info()
    return sys_info.cwd

def set_cwd_unsafe(new_wd: str):
    global _sys_info
    get_sys_info()
    _sys_info.cwd = new_wd