from subprocess import Popen, CREATE_NEW_CONSOLE

def main():
    proc = Popen("python terminal.py", creationflags=CREATE_NEW_CONSOLE)
    proc.wait()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass