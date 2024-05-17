import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["tkinter", "mysql.connector", "os"], "include_files": []}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="GUI_IPAM",
    version="0.1",
    description="GUI IP Address Management application",
    options={"build_exe": build_exe_options},
    executables=[Executable("GUI IPAM.py", base=base)]
)
