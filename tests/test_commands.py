from unittest.mock import patch, MagicMock
from commands import cmd_ls, cmd_cd, cmd_uname, cmd_rev, cmd_rmdir
from collections import namedtuple

DirEntry = namedtuple("DirEntry", ["name", "isdir"])

@patch("commands.get_sys_info")
@patch("commands.FileSystem")
def test_cmd_ls_no_args(MockFileSystem, mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home", fs_path="/fs")
    mock_fs = MockFileSystem.return_value
    mock_fs.dir_content.return_value = [
        DirEntry(name="home/file1.txt", isdir=MagicMock(return_value=False)),
        DirEntry(name="home/dir1", isdir=MagicMock(return_value=True)),
    ]

    with patch("builtins.print") as mock_print:
        cmd_ls([])
        mock_fs.dir_content.assert_called_with("/home")
        mock_print.assert_any_call("file1.txt")
        mock_print.assert_any_call("dir1/")


@patch("commands.get_sys_info")
@patch("commands.FileSystem")
def test_cmd_ls_with_path(MockFileSystem, mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(fs_path="/fs")
    mock_fs = MockFileSystem.return_value
    mock_fs.dir_content.return_value = [
        DirEntry(name="/other/file2.txt", isdir=MagicMock(return_value=False)),
    ]

    with patch("builtins.print") as mock_print:
        cmd_ls(["ls", "/other"])
        mock_fs.dir_content.assert_called_with("/other")
        mock_print.assert_any_call("file2.txt")


@patch("commands.get_sys_info")
@patch("commands.FileSystem")
def test_cmd_ls_no_such_dir(MockFileSystem, mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(fs_path="/fs")
    mock_fs = MockFileSystem.return_value
    mock_fs.dir_content.return_value = []
    mock_fs.is_dir.return_value = False

    with patch("builtins.print") as mock_print:
        cmd_ls(["ls", "/invalid"])
        mock_print.assert_any_call("No such directory!")


@patch("commands.get_sys_info")
@patch("commands.FileSystem")
def test_cmd_cd_valid(MockFileSystem, mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home", fs_path="/fs")
    MockFileSystem.normalize_path.return_value = "home/subdir"
    mock_fs = MockFileSystem.return_value
    mock_fs.is_dir.return_value = True

    with patch("commands.set_cwd_unsafe") as mock_set_cwd:
        cmd_cd(["cd", "subdir"])
        mock_fs.is_dir.assert_called_with("home/subdir")
        mock_set_cwd.assert_called_with("/home/subdir")


@patch("commands.get_sys_info")
@patch("commands.FileSystem")
def test_cmd_cd_invalid(MockFileSystem, mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home", fs_path="/fs")
    MockFileSystem.normalize_path.return_value = "home/invalid_dir"
    mock_fs = MockFileSystem.return_value
    mock_fs.is_dir.return_value = False

    with patch("builtins.print") as mock_print:
        cmd_cd(["cd", "invalid_dir"])
        mock_fs.is_dir.assert_called_with("home/invalid_dir")
        mock_print.assert_called_with("No such directory!")


@patch("commands.get_sys_info")
def test_cmd_cd_no_args(mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home")

    with patch("commands.set_cwd_unsafe") as mock_set_cwd:
        cmd_cd(["cd"])
        mock_set_cwd.assert_not_called()

@patch("commands.get_sys_info")
def test_cmd_uname_basic(mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(hostname="test-host")

    with patch("builtins.print") as mock_print:
        cmd_uname([])
        mock_print.assert_called_with("ZZZUnixEmu v0.1 on test-host")


@patch("commands.get_sys_info")
def test_cmd_uname_no_hostname(mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(hostname="")

    with patch("builtins.print") as mock_print:
        cmd_uname([])
        mock_print.assert_called_with("ZZZUnixEmu v0.1 on ")


@patch("commands.get_sys_info")
def test_cmd_uname_custom_message(mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(hostname="custom-host")

    with patch("builtins.print") as mock_print:
        cmd_uname([])
        mock_print.assert_called_with("ZZZUnixEmu v0.1 on custom-host")

@patch("commands.get_sys_info")
@patch("commands.FileSystem")
def test_cmd_rev_file(MockFileSystem, mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home", fs_path="/fs")
    mock_fs = MockFileSystem.return_value
    mock_fs.is_file.return_value = True

    mock_file = MagicMock()
    mock_file.__iter__.return_value = [b"abc", b"123"]
    mock_fs.open.return_value.__enter__.return_value = mock_file

    with patch("builtins.print") as mock_print:
        cmd_rev(["rev", "file.txt"])
        mock_print.assert_any_call("cba")
        mock_print.assert_any_call("321")


@patch("commands.get_sys_info")
@patch("commands.FileSystem")
def test_cmd_rev_no_file(MockFileSystem, mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home", fs_path="/fs")
    mock_fs = MockFileSystem.return_value
    mock_fs.is_file.return_value = False

    with patch("builtins.print") as mock_print:
        cmd_rev(["rev", "invalid.txt"])
        mock_print.assert_called_with("No such file!")


@patch("commands.get_sys_info")
def test_cmd_rev_no_args(mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home")

    with patch("builtins.print") as mock_print:
        cmd_rev([])
        mock_print.assert_not_called()

@patch("commands.get_sys_info")
@patch("commands.FileSystem")
def test_cmd_rmdir_valid(MockFileSystem, mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home", fs_path="/fs")

    mock_fs = MockFileSystem.return_value
    mock_fs.is_dir.return_value = True
    MockFileSystem.normalize_path.return_value = "normalized/path"
    cmd_rmdir(["cmd_rmdir", "test_dir"])
    mock_fs.rm_dir.assert_called_once_with("normalized/path")


@patch("commands.get_sys_info")
@patch("commands.FileSystem")
def test_cmd_rmdir_invalid(MockFileSystem, mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home", fs_path="/fs")
    mock_fs = MockFileSystem.return_value
    mock_fs.is_dir.return_value = False

    with patch("builtins.print") as mock_print:
        cmd_rmdir(["rmdir", "invalid_dir"])
        mock_print.assert_called_with("No such directory!")


@patch("commands.get_sys_info")
def test_cmd_rmdir_no_args(mock_get_sys_info):
    mock_get_sys_info.return_value = MagicMock(cwd="/home")

    with patch("builtins.print") as mock_print:
        cmd_rmdir([])
        mock_print.assert_not_called()
