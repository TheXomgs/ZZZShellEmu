from system import get_sys_info
from commands import get_cmd

def terminal():
    sys_info = get_sys_info()

    while True:
        args = input(f"{sys_info.hostname}> ").split()
        cmd = get_cmd(args[0])
        if cmd:
            cmd(args)
        else:
            print("No such command.")

terminal()