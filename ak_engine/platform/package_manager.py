import shutil
import subprocess

from .system import PlatformInfo


class PackageManager:

    def __init__(self):
        self.platform = PlatformInfo()

    def detect(self):
        system = self.platform.os

        if system == "windows":
            if shutil.which("winget"):
                return "winget"
            if shutil.which("choco"):
                return "choco"

        elif system == "macos":
            if shutil.which("brew"):
                return "brew"

        elif system == "linux":
            if shutil.which("apt"):
                return "apt"
            if shutil.which("dnf"):
                return "dnf"
            if shutil.which("pacman"):
                return "pacman"
            if shutil.which("apk"):
                return "apk"

        return None

    def is_available(self):
        return self.detect() is not None

    def install_command(self, package):
        manager = self.detect()

        if manager == "winget":
            return ["winget", "install", package]

        if manager == "choco":
            return ["choco", "install", package, "-y"]

        if manager == "brew":
            return ["brew", "install", package]

        if manager == "apt":
            return ["apt", "install", "-y", package]

        if manager == "dnf":
            return ["dnf", "install", "-y", package]

        if manager == "pacman":
            return ["pacman", "-S", "--noconfirm", package]

        if manager == "apk":
            return ["apk", "add", package]

        raise RuntimeError(
            f"No supported system package manager found on {self.platform.os}"
        )

    def install(self, package):
        command = self.install_command(package)

        print(f"[PackageManager] Using: {command[0]}")
        print(f"[PackageManager] Installing: {package}")

        return subprocess.run(
            command,
            check=False,
            text=True
        )
