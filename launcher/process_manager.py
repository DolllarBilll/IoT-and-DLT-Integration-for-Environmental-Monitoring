"""
IoT + DLT Integration Project

Process Manager
Handles process detection, start, stop and status.
"""

import subprocess
import psutil
import sys
import os

from launcher.config import (
    PROJECT_ROOT,
    GATEWAY_SCRIPT,
    PUBLISHER_SCRIPT,
    VERIFY_SCRIPT,
    VIEW_DATABASE_SCRIPT,
    DATABASE_SCRIPT,
    DATABASE_FILE,
    MOSQUITTO_COMMAND
)


class ProcessManager:

    def __init__(self):
        self.gateway_process = None
        self.publisher_process = None
        self.verify_process = None
        self.database_process = None
        self.mosquitto_process = None

    def process_exists(self, executable):
        executable = executable.lower()
        for proc in psutil.process_iter(["name"]):
            try:
                name = proc.info["name"]
                if name and name.lower() == executable:
                    return True
            except (psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess):
                pass
        return False

    def find_python_script(self, script_name):
        script_name = script_name.lower()
        for proc in psutil.process_iter(["name", "cmdline"]):
            try:
                name = proc.info["name"]
                if not name or "python" not in name.lower():
                    continue

                cmdline = proc.info["cmdline"]
                if not cmdline:
                    continue

                if script_name in " ".join(cmdline).lower():
                    return proc

            except (psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess):
                pass
        return None

    def mqtt_running(self):
        return self.process_exists("mosquitto.exe")

    def gateway_running(self):
        return self.find_python_script("gateway.py") is not None

    def publisher_running(self):
        return self.find_python_script("publisher.py") is not None

    def verify_running(self):
        return self.find_python_script("verify_integrity.py") is not None

    def database_running(self):
        return self.find_python_script("view_database.py") is not None

    def database_exists(self):
        return os.path.exists(DATABASE_FILE)

    def create_database(self):

        if self.database_exists():
            return False

        if getattr(sys, "frozen", False):
            python_cmd = "python"
        else:
            python_cmd = sys.executable

        result = subprocess.run(
            [python_cmd, str(DATABASE_SCRIPT)],
            cwd=PROJECT_ROOT
        )

        return result.returncode == 0

    def start_gateway(self):
        if self.gateway_running():
            return False

        self.gateway_process = subprocess.Popen(
            ["python", str(GATEWAY_SCRIPT)],
            cwd=PROJECT_ROOT,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        return True

    def start_publisher(self):
        if self.publisher_running():
            return False

        self.publisher_process = subprocess.Popen(
            ["python", str(PUBLISHER_SCRIPT)],
            cwd=PROJECT_ROOT,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        return True

    def start_verify(self):
        if self.verify_running():
            return False

        self.verify_process = subprocess.Popen(
            ["python", str(VERIFY_SCRIPT)],
            cwd=PROJECT_ROOT,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        return True

    def start_database(self):

        if self.database_running():
            return False

        if getattr(sys, "frozen", False):
            python_cmd = "python"
        else:
            python_cmd = sys.executable

        self.database_process = subprocess.Popen(
            [python_cmd, str(VIEW_DATABASE_SCRIPT)],
            cwd=PROJECT_ROOT,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        return True

    def stop_python_script(self, script_name):
        process = self.find_python_script(script_name)
        if process:
            process.terminate()
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()

    def stop_all(self):
        self.stop_python_script("publisher.py")
        self.stop_python_script("gateway.py")
        self.stop_python_script("verify_integrity.py")