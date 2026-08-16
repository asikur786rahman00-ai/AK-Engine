import os
import platform
import shutil
import sys


class PlatformInfo:

    @property
    def os(self):
        system = platform.system().lower()

        if system == "windows":
            return "windows"

        if system == "darwin":
            return "macos"

        if system == "linux":
            return "linux"

        return system

    @property
    def architecture(self):
        return platform.machine().lower()

    @property
    def python_version(self):
        return platform.python_version()

    @property
    def shell(self):
        if self.os == "windows":
            return os.environ.get("COMSPEC", "cmd.exe")

        return os.environ.get("SHELL", "/bin/sh")

    @property
    def home(self):
        return os.path.expanduser("~")

    def has_command(self, command):
        return shutil.which(command) is not None

    def summary(self):

        return {
            "os": self.os,
            "architecture": self.architecture,
            "python": self.python_version,
            "shell": self.shell,
            "home": self.home,
        }


platform_info = PlatformInfo()
