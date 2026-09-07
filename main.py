"""
IoT + DLT Integration Project

Application Entry Point
"""

from launcher.ui import LauncherUI


def main():
    """
    Starts the launcher application.
    """

    app = LauncherUI()
    app.run()


if __name__ == "__main__":
    main()