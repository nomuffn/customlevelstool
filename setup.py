import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": [], "excludes": ["tkinter"]}

setup(
    name="muffnsCustomLevelsTool",
    version="0.1",
    description="Custom Levels Tool wow",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")],
)