from system import get_sys_info
from commands import get_cmd
from json import dump, load
from config import get_config
from tarfile import open as tar_open
from os import path

def terminal():
    sys_info = get_sys_info()
    config = get_config('config.ini')
    startup = config.get("config", "startup", fallback=None)

    with open("log.json", "w")as log_file:
        dump([], log_file)

    if not path.exists(sys_info.fs_path):
        with tar_open(sys_info.fs_path, "w") as fs:
            pass

    if startup:
        with open(startup, "r") as file:
            for line in file:
                args = line.split()
                if not args:
                    continue
                cmd = get_cmd(args[0])
                if cmd:
                    cmd(args)
                    with open("log.json", "r") as log_file:
                        log = load(log_file)
                    log.append(line)
                    with open("log.json", "w") as log_file:
                        dump(log, log_file)

    while True:
        prompt = input(f"{sys_info.hostname}> ")
        args = prompt.split()
        if not args:
            continue
        cmd = get_cmd(args[0])
        if cmd:
            cmd(args)
            with open("log.json", "r") as log_file:
                log = load(log_file)
            log.append(prompt)
            with open("log.json", "w") as log_file:
                dump(log, log_file)
        else:
            print("No such command.")
            

terminal()