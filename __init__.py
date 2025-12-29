# python3.11
import importlib.util
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, distribution


class Pip:
    def _ensurePip(self):
        if importlib.util.find_spec("pip") is None:
            subprocess.check_call([sys.executable, "-m", "ensurepip"])

    def testModule(self, package):
        try:
            distribution(package)
            return True
        except PackageNotFoundError:
            return False

    def pipInstall(
        self,
        package,
    ):
        self._ensurePip()
        if not self.testModule(package):
            print(f"安装 {package}…")
            complete = subprocess.run([sys.executable, "-m", "pip", "install", package, "--break-system-packages"], text=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            try:
                complete.check_returncode()
            except subprocess.CalledProcessError:
                print(f"{package} 安装失败")
                return False
        return True


pip = Pip()
requirements = ["httpx", "watchdog", "jsonschema", "uvicorn", "uvloop", "httptools", "websockets", "watchfiles", "fastapi", "apscheduler", "loguru", "pycryptodome", "sortedcontainers"]
for pkg in requirements:
    if not pip.testModule(pkg):
        pip.pipInstall(pkg)

import python  # noqa: E402, F401
