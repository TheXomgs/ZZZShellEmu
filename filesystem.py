from typing import List
from tarfile import open as tar_open
from tarfile import TarFile, TarInfo
from io import BytesIO

class FileSystem:
    def __init__(self, fs_path):
        self.fs_path = fs_path
    
    def normalize_path(path: str):
        return path.removeprefix("/").removesuffix("/")
    
    def is_dir(self, path: str):
        if path == "/":
            return True
        path = FileSystem.normalize_path(path)
        with tar_open(self.fs_path, "r") as fs:
            if path in fs.getnames() and fs.getmember(path).isdir():
                return True
        return False
    
    def is_file(self, path: str):
        if path == "/":
            return False
        path = FileSystem.normalize_path(path)
        with tar_open(self.fs_path, "r") as fs:
            if path in fs.getnames() and fs.getmember(path).isfile():
                return True
        return False

    def dir_content(self, path):
        content: List[TarInfo] = []
        if not self.is_dir(path):
            return None
        path = FileSystem.normalize_path(path)
        with tar_open(self.fs_path, "r") as fs:
            for member in fs.getmembers():
                if member.name.startswith(path) and member.name != path and member.name.count("/") <= path.count("/") + (1 if path else 0):
                    content.append(member)
        
        return content
    
    def rm_dir(self, path: str):
        if not self.is_dir(path):
            return None
        tmp = BytesIO()
        path = FileSystem.normalize_path(path)
        with tar_open(self.fs_path, "r") as fs:
            with tar_open(fileobj=tmp, mode="w") as new_fs:
                for member in fs.getmembers():
                    if not member.name.startswith(path):
                        new_fs.addfile(member, fs.extractfile(member))
        with open(self.fs_path, mode="wb") as file:
            file.write(tmp.getvalue())
    
    def open(self, path: str):
        class FileDescriptor(object):
            def __init__(self, zip_path, file_path):
                self.zip_path = zip_path
                self.file_path = file_path
            def __enter__(self):
                self.file_path = FileSystem.normalize_path(self.file_path)
                self.fs = TarFile(self.zip_path, mode="r")
                member = self.fs.getmember(self.file_path)
                self.file = self.fs.extractfile(member)
                return self.file
            def __exit__(self, type, value, traceback):
                self.file.close()
                self.fs.close()

        return FileDescriptor(self.fs_path, path)
    
    