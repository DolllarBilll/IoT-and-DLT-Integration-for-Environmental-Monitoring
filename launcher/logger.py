"""
IoT + DLT Integration Project

Launcher Logger
"""

from datetime import datetime


class ActivityLogger:
    """
    Handles activity logging
    for the launcher.
    """

    def __init__(self, textbox):

        self.textbox = textbox

    def log(self, message):
        """
        Writes one message
        to the activity log.
        """

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.textbox.configure(state="normal")

        self.textbox.insert(
            "end",
            f"[{timestamp}] {message}\n"
        )

        self.textbox.see("end")

        self.textbox.configure(state="disabled")

    def clear(self):
        """
        Clears the activity log.
        """

        self.textbox.configure(state="normal")

        self.textbox.delete("1.0", "end")

        self.textbox.configure(state="disabled")