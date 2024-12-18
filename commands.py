from system import get_sys_info, set_cwd_unsafe
from filesystem import FileSystem

def cmd_exit(args):
    exit(0)

def cmd_ls(args):
    sys = get_sys_info()
    fs = FileSystem(sys.fs_path)

    if len(args) > 1:
        path = args[1]
    else:
        path = sys.cwd

    if fs.is_dir(path):
        for item in fs.dir_content(path):
            print(item.name.rsplit("/", 1)[-1] + ("/" if item.isdir() else ""))
    else:
        print("No such directory!")

def cmd_cd(args):
    sys = get_sys_info()
    fs = FileSystem(sys.fs_path)

    if len(args) > 1:
        path = args[1]
    else:
        return
    
    if not path.startswith("/"):
        path = FileSystem.normalize_path(f'{sys.cwd}/{path}')
    
    if fs.is_dir(path):
        set_cwd_unsafe(f'/{FileSystem.normalize_path(path)}')
    else:
        print("No such directory!")

def cmd_uname(args):
    sys = get_sys_info()
    print(f'ZZZUnixEmu v0.1 on {sys.hostname}')

def cmd_pwd(args):
    sys = get_sys_info()

    print(sys.cwd)

def cmd_rev(args):
    sys = get_sys_info()
    fs = FileSystem(sys.fs_path)

    if len(args) > 1:
        path = args[1]
    else:
        return
    
    if not path.startswith("/"):
        path = FileSystem.normalize_path(f'{sys.cwd}/{path}')
    
    if fs.is_file(path):
        with fs.open(path) as file:
            for line in file:
                print("".join(map(chr, line[::-1])))
    else:
        print("No such file!")

def cmd_rmdir(args):
    sys = get_sys_info()
    fs = FileSystem(sys.fs_path)

    if len(args) > 1:
        path = args[1]
    else:
        return
    
    if not path.startswith("/"):
        path = FileSystem.normalize_path(f'{sys.cwd}/{path}')
    
    if fs.is_dir(path):
        fs.rm_dir(path)
    else:
        print("No such directory!")

def get_cmd(cmd_name):
    obj = globals().get(f"cmd_{cmd_name}")
    if callable(obj):
        return obj
    return None