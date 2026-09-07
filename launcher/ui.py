"""
IoT + DLT Integration Project

Launcher User Interface
"""

import os
import sys
import webbrowser
import time
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import sqlite3
import paho.mqtt.client as mqtt

from launcher.config import (
    APPLICATION_TITLE,
    STATUS_REFRESH,
    PROJECT_ROOT,
    SHIMMER_EXPLORER,
    DATABASE_FILE,
)

from launcher.logger import ActivityLogger
from launcher.process_manager import ProcessManager

# ==========================
# UI LAYOUT
# ==========================

WINDOW_WIDTH = 750
WINDOW_HEIGHT = 780

OUTER_MARGIN = 5
CARD_GAP = 5

CARD_RADIUS = 12
CARD_BORDER = 1

TITLE_PAD_X = 16
TITLE_PAD_Y = 16

BUTTON_HEIGHT = 36
BUTTON_PAD_X = 15
BUTTON_PAD_Y = 5

def resource_path(relative_path):
    """Return absolute path to resource (works for development and PyInstaller)."""

    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base_path, relative_path)

def load_icon(filename):

    return ctk.CTkImage(
        light_image=Image.open(
            resource_path(f"assets/icons/Buttons/{filename}")
        ),
        dark_image=Image.open(
            resource_path(f"assets/icons/Buttons/{filename}")
        ),
        size=(20, 20)
    )

class LauncherUI:

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.process_manager = ProcessManager()

        self.gateway_ready = False

        self.status_client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        self.status_client.on_connect = self.on_status_connect
        self.status_client.on_message = self.on_status_message

        self.window = ctk.CTk()
        icon_path = resource_path("assets/iot_dlt.ico")

        # Windows title bar & taskbar
        self.window.iconbitmap(icon_path)

        # Tkinter keeps a reference to the image
        icon = ImageTk.PhotoImage(Image.open(icon_path))
        self.window.iconphoto(True, icon)
        self.window._icon = icon
        self.window.title(APPLICATION_TITLE)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=0)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.resizable(False, False)
        self.last_update = "Never"
        self.status_icons = {
        
            "mqtt": ctk.CTkImage(
                Image.open(resource_path("assets/icons/status/mqtt.png")),
                size=(40, 40)
            ),

            "gateway": ctk.CTkImage(
                Image.open(resource_path("assets/icons/status/gateway.png")),
                size=(40, 40)
            ),

            "publisher": ctk.CTkImage(
                Image.open(resource_path("assets/icons/status/publisher.png")),
                size=(40, 40)
            ),

            "database": ctk.CTkImage(
                Image.open(resource_path("assets/icons/status/database.png")),
                size=(40, 40)
            ),

            "dlt": ctk.CTkImage(
                Image.open(resource_path("assets/icons/status/DLT.png")),
                size=(40, 40)
            )
        }
        self.create_widgets()
        self.log_message("Application started.")
        self.log_message("Database check completed.")
        self.log_message("Launcher ready.")
        self.update_status()
        self.update_quick_info()
        
    def create_widgets(self):

        self.create_main_layout()

        self.create_controls()

        self.create_status()

        self.create_quick_info()

        self.create_log()

        self.create_footer()

    # ==========================
    # LAYOUT
    # ==========================

    def create_main_layout(self):

        # ==========================
        # Main Container
        # ==========================

        self.main_frame = ctk.CTkFrame(
            self.window,
            fg_color="transparent"
        )

        self.main_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=OUTER_MARGIN,
            pady=OUTER_MARGIN
        )

        # Two columns
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        # ==========================
        # LEFT COLUMN
        # ==========================

        self.left_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.left_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=CARD_GAP,
            pady=CARD_GAP
        )

        self.left_frame.grid_columnconfigure(0, weight=1)

        # Ίδιες αναλογίες με πριν
        self.left_frame.grid_rowconfigure(0, weight=55)
        self.left_frame.grid_rowconfigure(1, weight=45)

        # Project Controls
        self.left_top_frame = ctk.CTkFrame(
            self.left_frame,
            fg_color="transparent"
        )

        self.left_top_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=(0, 10)
        )

        # Activity Log
        self.left_bottom_frame = ctk.CTkFrame(
            self.left_frame,
            fg_color="transparent"
        )

        self.left_bottom_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        # ==========================
        # RIGHT COLUMN
        # ==========================

        self.right_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.right_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=CARD_GAP,
            pady=CARD_GAP
        )

        self.right_frame.grid_columnconfigure(0, weight=1)

        # Διαφορετικές αναλογίες
        self.right_frame.grid_rowconfigure(0, weight=60)
        self.right_frame.grid_rowconfigure(1, weight=30)

        # System Status
        self.right_top_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color="transparent"
        )

        self.right_top_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=(0, 10)
        )

        # Quick Info
        self.right_bottom_frame = ctk.CTkFrame(
            self.right_frame,
            fg_color="transparent"
        )

        self.right_bottom_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    # ==========================
    # CONTROLS
    # ==========================

    def create_controls(self):

        self.controls_frame = ctk.CTkFrame(
            self.left_top_frame,
            fg_color="#323232",
            corner_radius=CARD_RADIUS,
            border_width=CARD_BORDER,
            border_color="#4A4A4A"
        )

        self.controls_frame.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )

        title = ctk.CTkLabel(
            self.controls_frame,
            text="PROJECT CONTROLS",
            font=("Segoe UI", 18),
            text_color="#7CFC00"
        )

        title.pack(anchor="w", padx=15, pady=(15, 10))

        # -----------------------------
        # ΛΙΣΤΑ ΚΟΥΜΠΙΩΝ
        # -----------------------------

        self.buttons_frame = ctk.CTkFrame(
            self.controls_frame,
            fg_color="transparent"
        )

        self.buttons_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.buttons_frame.grid_columnconfigure(0, weight=1)

        buttons = [
            ("Start Project",
            "player-play.png",
            self.start_project,
            "#1E7D32",
            "#2E8B57"),

            ("Verify Integrity",
            "shield-check.png",
            self.verify_integrity,
            "#1565C0",
            "#1976D2"),

            ("View Database",
            "chart-area-line.png",
            self.view_database,
            "#5E35B1",
            "#673AB7"),

            ("Create Database",
            "database.png",
            self.create_database,
            "#C77700",
            "#D68910"),

            ("Open Shimmer Explorer",
            "world.png",
            self.open_explorer,
            "#006D7A",
            "#00838F"),

            ("Open Project Folder",
            "folder-open.png",
            self.open_project_folder,
            "#0D47A1",
            "#1565C0"),

            ("Stop Project",
            "player-stop.png",
            self.stop_project,
            "#C62828",
            "#D32F2F"),

            ("About",
            "info-circle.png",
            self.about,
            "#3B434B",
            "#4A535C")
        ]

        # -----------------------------
        # ΔΗΜΙΟΥΡΓΙΑ ΚΟΥΜΠΙΩΝ
        # -----------------------------

        for i, (text, icon_file, command, color, hover) in enumerate(buttons):

            icon = load_icon(icon_file)

            button = ctk.CTkButton(
                self.buttons_frame,

                text=text,
                image=icon,

                compound="left",
                anchor="w",

                command=command,

                height=BUTTON_HEIGHT,

                corner_radius=10,

                font=("Segoe UI", 15),

                fg_color=color,

                hover_color=hover
            )

            button.grid(
                row=i,
                column=0,
                sticky="ew",
                pady=BUTTON_PAD_Y
            )

    # ==========================
    # STATUS
    # ==========================

    def create_status(self):
        # 1. Δημιουργία του frame
        self.status_frame = ctk.CTkFrame(
            self.right_top_frame,
            fg_color="#323232",
            corner_radius=12,
            border_width=1,
            border_color="#4A4A4A"
        )

        self.status_frame.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )

        # 2. Τίτλος
        title = ctk.CTkLabel(
            self.status_frame,
            text="SYSTEM STATUS",
            font=("Segoe UI", 18),
            text_color="#7CFC00"
        )

        title.pack(anchor="w", padx=TITLE_PAD_X, pady=(TITLE_PAD_Y, 10))

        self.status_cards_frame = ctk.CTkFrame(
            self.status_frame,
            fg_color="transparent"
        )

        self.status_cards_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 10)
        )

        self.status_cards_frame.grid_columnconfigure(0, weight=1)

        # μία γραμμή για κάθε card
        for row in range(5):
            self.status_cards_frame.grid_rowconfigure(row, weight=1)

        # 3. Δημιουργία Labels
        self.mqtt_card = self.create_status_card(
            self.status_icons["mqtt"],
            "Mosquitto Broker",
            "localhost:1883",
            "RUNNING",
            "#43A047"
        )

        self.gateway_card = self.create_status_card(
            self.status_icons["gateway"],
            "Gateway",
            "Subscriber",
            "STOPPED",
            "#B0BEC5"
        )

        self.publisher_card = self.create_status_card(
            self.status_icons["publisher"],
            "Publisher",
            "Sensors Simulator",
            "STOPPED",
            "#B0BEC5"
        )

        self.database_card = self.create_status_card(
            self.status_icons["database"],
            "Database",
            "SQLite",
            "READY",
            "#42A5F5"
        )

        self.dlt_card = self.create_status_card(
            self.status_icons["dlt"],
            "DLT (Shimmer)",
            "IOTA Shimmer Network",
            "READY",
            "#42A5F5"
        )

    def create_status_card(
            self,
            icon_image,
            title,
            subtitle,
            state,
            color
    ):

        card = ctk.CTkFrame(
            self.status_cards_frame,
            fg_color="#242424",
            corner_radius=10,
            border_width=1,
            border_color="#505050"
        )

        row = len(self.status_cards_frame.grid_slaves(column=0))

        card.grid(
            row=row,
            column=0,
            sticky="nsew",
            pady=5
        )

        # -------------------------
        # GRID
        # -------------------------

        card.grid_columnconfigure(0, weight=0)
        card.grid_columnconfigure(1, weight=1)
        card.grid_columnconfigure(2, weight=0)

        card.grid_rowconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        # -------------------------
        # ICON
        # -------------------------

        icon_label = ctk.CTkLabel(
            card,
            image=icon_image,
            text=""
        )

        icon_label.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=15,
            pady=10,
            sticky="ns"
        )

        # -------------------------
        # TITLE
        # -------------------------

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 15)
        )

        title_label.grid(
            row=0,
            column=1,
            sticky="sw",
            pady=(8, 0)
        )

        # -------------------------
        # SUBTITLE
        # -------------------------

        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=("Segoe UI", 11),
            text_color="#BDBDBD"
        )

        subtitle_label.grid(
            row=1,
            column=1,
            sticky="nw",
            pady=(0, 8)
        )

        # -------------------------
        # STATUS
        # -------------------------

        status_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        status_frame.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(10, 15),
            sticky="e"
        )

        state_label = ctk.CTkLabel(
            status_frame,
            text=state,
            font=("Segoe UI", 13),
            text_color=color
        )

        state_label.pack(
            side="left"
        )

        dot_label = ctk.CTkLabel(
            status_frame,
            text="●",
            font=("Segoe UI", 15),
            text_color=color
        )

        dot_label.pack(
            side="left",
            padx=(5, 0)
        )

        return {
            "card": card,
            "state": state_label,
            "dot": dot_label
        }
    
    # ==========================
    # QUICK INFO
    # ==========================

    def create_quick_info(self):

        # ==========================
        # Create Frame
        # ==========================

        self.quick_info_frame = ctk.CTkFrame(
            self.right_bottom_frame,
            fg_color="#323232",
            corner_radius=12,
            border_width=1,
            border_color="#4A4A4A"
        )

        self.quick_info_frame.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )

        # ==========================
        # Create Title
        # ==========================

        title = ctk.CTkLabel(
            self.quick_info_frame,
            text="QUICK INFO",
            font=("Segoe UI", 18),
            text_color="#7CFC00"
        )

        title.pack(
            anchor="w",
            padx=15,
            pady=(15, 12)
        )

        # ==========================
        # Quick Info Card
        # ==========================

        self.quick_info_card = ctk.CTkFrame(
            self.quick_info_frame,
            fg_color="#1F1F1F",
            corner_radius=10,
            border_width=1,
            border_color="#4A4A4A"
        )

        self.quick_info_card.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        # ==========================
        # Info Container
        # ==========================

        info_frame = ctk.CTkFrame(
            self.quick_info_card,
            fg_color="transparent"
        )

        info_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=15
        )

        # ==========================
        # Grid Configuration
        # ==========================

        info_frame.grid_columnconfigure(0, weight=0)
        info_frame.grid_columnconfigure(1, weight=1)

        # ==========================
        # Database File
        # ==========================

        db_label = ctk.CTkLabel(
            info_frame,
            text="Database File:",
            font=("Segoe UI", 14),
            anchor="w"
        )

        self.database_value = ctk.CTkLabel(
            info_frame,
            text="environmental_data.db",
            font=("Segoe UI", 14),
            anchor="w"
        )

        db_label.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 12)
        )

        self.database_value.grid(
            row=0,
            column=1,
            sticky="w",
            padx=(35, 0),
            pady=(0, 12)
        )

        # ==========================
        # Total Records
        # ==========================

        records_label = ctk.CTkLabel(
            info_frame,
            text="Total Records:",
            font=("Segoe UI", 14),
            anchor="w"
        )

        self.records_value = ctk.CTkLabel(
            info_frame,
            text="0",
            font=("Segoe UI", 14),
            anchor="w"
        )

        records_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(0, 12)
        )

        self.records_value.grid(
            row=1,
            column=1,
            sticky="w",
            padx=(35, 0),
            pady=(0, 12)
        )

        # ==========================
        # Last Update
        # ==========================

        update_label = ctk.CTkLabel(
            info_frame,
            text="Last Update:",
            font=("Segoe UI", 14),
            anchor="w"
        )

        self.last_update_value = ctk.CTkLabel(
            info_frame,
            text="Never",
            font=("Segoe UI", 14),
            anchor="w"
        )

        update_label.grid(
            row=2,
            column=0,
            sticky="w"
        )

        self.last_update_value.grid(
            row=2,
            column=1,
            sticky="w",
            padx=(35, 0)
        )

    def get_database_filename(self):

        if DATABASE_FILE.exists():
            return DATABASE_FILE.name

        return "Not Found"

    def get_total_records(self):

        if not DATABASE_FILE.exists():
            return "0"

        try:

            conn = sqlite3.connect(DATABASE_FILE)

            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM environment_data")

            count = cursor.fetchone()[0]

            conn.close()

            return str(count)

        except Exception:
            return "0"
    
    def update_quick_info(self):

        self.database_value.configure(
            text=self.get_database_filename()
        )

        self.records_value.configure(
            text=self.get_total_records()
        )

        self.last_update_value.configure(
            text=self.last_update
        )

    def refresh_last_update(self):

        self.last_update = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.update_quick_info()

    # ==========================
    # LOG
    # ==========================

    def create_log(self):

        # ==========================
        # Create Frame
        # ==========================

        self.log_frame = ctk.CTkFrame(
            self.left_bottom_frame,
            fg_color="#323232",
            corner_radius=12,
            border_width=1,
            border_color="#4A4A4A"
        )

        self.log_frame.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )

        # ==========================
        # Grid Configuration
        # ==========================

        self.log_frame.grid_rowconfigure(0, weight=0)   # Title
        self.log_frame.grid_rowconfigure(1, weight=1)   # Textbox

        self.log_frame.grid_columnconfigure(0, weight=1)

        # ==========================
        # Title
        # ==========================

        title = ctk.CTkLabel(
            self.log_frame,
            text="ACTIVITY LOG",
            font=("Segoe UI", 18),
            text_color="#7CFC00"
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 10)
        )

        # ==========================
        # Textbox
        # ==========================

        self.log_textbox = ctk.CTkTextbox(
            self.log_frame,
            font=("Consolas", 13),
            wrap="word"
        )

        self.log_textbox.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        # ==========================
        # Welcome Message
        # ==========================

        self.log_textbox.insert(
            "end",
            "====================================\n"
        )

        self.log_textbox.insert(
            "end",
            " IoT + DLT Integration Launcher\n"
        )

        self.log_textbox.insert(
            "end",
            "====================================\n\n"
        )

        self.log_textbox.insert(
            "end",
            "[SYSTEM] Launcher initialized.\n"
        )

        self.log_textbox.insert(
            "end",
            "[SYSTEM] Waiting for user...\n"
        )

        self.log_textbox.tag_config("INFO", foreground="#4FC3F7")
        self.log_textbox.tag_config("SUCCESS", foreground="#00E676")
        self.log_textbox.tag_config("WARNING", foreground="#FFD54F")
        self.log_textbox.tag_config("ERROR", foreground="#FF5252")

        self.log_textbox.configure(state="disabled")

    def create_footer(self):

        self.footer = ctk.CTkFrame(
            self.window,
            height=38,
            corner_radius=0,
            fg_color="#2B2B2B"
        )

        self.footer.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        self.footer.grid_columnconfigure(0, weight=1)
        self.footer.grid_columnconfigure(1, weight=0)

        # -------------------------
        # Left
        # -------------------------

        self.footer_status = ctk.CTkLabel(
            self.footer,
            text="●  System Not Ready",
            font=("Segoe UI", 15),
            text_color="#D32F2F"
        )

        self.footer_status.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=8
        )

        # -------------------------
        # Right
        # -------------------------

        footer_info = ctk.CTkLabel(
            self.footer,
            text="|   © 2026",
            font=("Segoe UI", 15)
        )

        footer_info.grid(
            row=0,
            column=1,
            sticky="e",
            padx=15
        )

    def update_footer_status(self):

        mqtt_ok = self.process_manager.mqtt_running()
        database_ok = self.process_manager.database_exists()

        if mqtt_ok and database_ok:

            self.footer_status.configure(
                text="●  All Systems Ready",
                text_color="#43A047"
            )

        else:

            self.footer_status.configure(
                text="●  System Not Ready",
                text_color="#D32F2F"
            )

    def log_message(self, message, level="INFO"):

        current_time = datetime.now().strftime("%H:%M:%S")

        self.log_textbox.configure(state="normal")

        line = f"[{current_time}] [{level}] {message}\n"

        self.log_textbox.insert(
            "end",
            line,
            level
        )

        self.log_textbox.see("end")

        self.log_textbox.configure(state="disabled")

    def on_status_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties=None
    ):

        if reason_code == 0:
            client.subscribe("gateway/status")


    def on_status_message(
        self,
        client,
        userdata,
        msg
    ):

        if msg.topic == "gateway/status":

            status = msg.payload.decode()

            if status == "READY":

                self.gateway_ready = True

                self.log_message(
                    "Gateway is ready.",
                    "SUCCESS"
                )

                if self.process_manager.start_publisher():

                    self.log_message(
                        "Publisher started.",
                        "SUCCESS"
                    )

                else:

                    self.log_message(
                        "Publisher already running.",
                        "INFO"
                    )

                self.refresh_last_update()

    def start_project(self):

        # ==========================
        # Database check
        # ==========================

        if not self.process_manager.database_exists():

            messagebox.showerror(
                "Database",
                "Δεν υπάρχει βάση δεδομένων.\n\n"
                "Πατήστε πρώτα 'Create Database'."
            )

            self.log_message(
                "Start cancelled. Database not found.",
                "ERROR"
            )

            return

        # ==========================
        # Reset Gateway status
        # ==========================

        self.gateway_ready = False

        # ==========================
        # Connect status client
        # ==========================

        try:

            self.status_client.connect(
                "localhost",
                1883,
                60
            )

            self.status_client.loop_start()

        except Exception as e:

            self.log_message(
                f"Gateway status listener failed: {e}",
                "ERROR"
            )

            return

        # ==========================
        # Start Gateway
        # ==========================

        if self.process_manager.start_gateway():

            self.log_message(
                "Gateway started. Waiting for Gateway to become ready...",
                "SUCCESS"
            )

        else:

            self.log_message(
                "Gateway already running.",
                "INFO"
            )

        # ==========================
        # Publisher is NOT started here
        # ==========================
        #
        # Publisher will be started
        # automatically when the Gateway
        # sends:
        #
        # gateway/status -> READY

        self.refresh_last_update()

    def stop_project(self):

        if (
            not self.process_manager.gateway_running()
            and not self.process_manager.publisher_running()
        ):

            messagebox.showwarning(
                "Project",
                "Project is not running."
            )

            self.log_message(
                "Stop cancelled. Project is not running.",
                "WARNING"
            )

            return

        self.process_manager.stop_all()

        self.status_client.loop_stop()

        if self.status_client.is_connected():
            self.status_client.disconnect()

        self.gateway_ready = False

        self.log_message(
            "Project stopped.",
            "SUCCESS"
        )

        self.refresh_last_update()

    def verify_integrity(self):

        if not self.process_manager.database_exists():

            messagebox.showwarning(
                "Database",
                "Δεν υπάρχει βάση δεδομένων.\n\n"
                "Δημιουργήστε πρώτα μία από το κουμπί 'Create Database'."
            )

            self.log_message(
                "Integrity verification cancelled. Database not found.",
                "ERROR"
                )

            return

        if self.process_manager.start_verify():
            self.log_message(
                "Integrity verification started.",
                "SUCCESS"
            )
        else:
            self.log_message(
                "Integrity verification already running.",
                "INFO"
            )

        self.refresh_last_update()

    def view_database(self):

        if self.process_manager.start_database():
            self.log_message(
                "Database Viewer started.",
                "SUCCESS"
            )
        else:
            self.log_message(
                "Database Viewer already running.",
                "INFO"
            )

        self.refresh_last_update()

    def create_database(self):

        if self.process_manager.database_exists():

            messagebox.showinfo(
                "Database",
                "Υπάρχει ήδη βάση δεδομένων."
            )

            self.log_message(
                "Database already exists.",
                "WARNING"
            )

            return

        success = self.process_manager.create_database()

        if success:

            messagebox.showinfo(
                "Database",
                "Δημιουργήθηκε νέα βάση δεδομένων."
            )

            self.log_message(
                "Database created.",
                "SUCCESS"
            )

        else:

            messagebox.showerror(
                "Database",
                "Αποτυχία δημιουργίας βάσης δεδομένων."
            )

            self.log_message(
                "Database creation failed.",
                "ERROR"
            )

        self.refresh_last_update()

    def open_explorer(self):
        webbrowser.open(SHIMMER_EXPLORER)
        self.log_message(
            "Opened Shimmer Explorer.",
            "SUCCESS"
        )

    def open_project_folder(self):
        os.startfile(Path(PROJECT_ROOT).resolve())
        self.log_message(
            "Opened project folder.",
            "SUCCESS"
        )

    def update_status(self):

        # MQTT
        if self.process_manager.mqtt_running():

            self.mqtt_card["state"].configure(
                text="RUNNING",
                text_color="#43A047"
            )

            self.mqtt_card["dot"].configure(
                text_color="#43A047"
            )

        else:

            self.mqtt_card["state"].configure(
                text="STOPPED",
                text_color="#D32F2F"
            )

            self.mqtt_card["dot"].configure(
                text_color="#D32F2F"
            )

        # Gateway
        if self.process_manager.gateway_running():

            self.gateway_card["state"].configure(
                text="RUNNING",
                text_color="#43A047"
            )

            self.gateway_card["dot"].configure(
                text_color="#43A047"
            )

        else:

            self.gateway_card["state"].configure(
                text="STOPPED",
                text_color="#D32F2F"
            )

            self.gateway_card["dot"].configure(
                text_color="#D32F2F"
            )

        # Publisher
        if self.process_manager.publisher_running():

            self.publisher_card["state"].configure(
                text="RUNNING",
                text_color="#43A047"
            )

            self.publisher_card["dot"].configure(
                text_color="#43A047"
            )

        else:

            self.publisher_card["state"].configure(
                text="STOPPED",
                text_color="#D32F2F"
            )

            self.publisher_card["dot"].configure(
                text_color="#D32F2F"
            )

        # Database
        if self.process_manager.database_exists():

            self.database_card["state"].configure(
                text="READY",
                text_color="#42A5F5"
            )

            self.database_card["dot"].configure(
                text_color="#42A5F5"
            )

        else:

            self.database_card["state"].configure(
                text="NOT READY",
                text_color="#D32F2F"
            )

            self.database_card["dot"].configure(
                text_color="#D32F2F"
            )

        # Footer
        self.update_footer_status()

        self.window.after(
            STATUS_REFRESH,
            self.update_status
        )

    def about(self):

        self.about_window = ctk.CTkToplevel(self.window)

        icon_path = resource_path("assets/iot_dlt.ico")
        
        # Windows title bar & taskbar
        self.about_window.iconbitmap(icon_path)

        # Tkinter keeps a reference to the image
        about_icon = ImageTk.PhotoImage(Image.open(icon_path))
        self.about_window.iconphoto(True, about_icon)
        self.about_window._icon = about_icon

        self.about_window.title("About")

        self.about_window.geometry("750x900")

        self.about_window.resizable(False, False)

        self.about_window.transient(self.window)

        self.about_window.grab_set()

        self.about_window.focus()

        self.about_image = ctk.CTkImage(
            light_image=Image.open(
                resource_path("assets/About.png")
            ),
            dark_image=Image.open(
                resource_path("assets/About.png")
            ),
            size=(750, 900)
        )

        self.about_label = ctk.CTkLabel(
            self.about_window,
            image=self.about_image,
            text=""
        )

        self.about_label.pack(
            fill="both",
            expand=True
        )
        
    def run(self):
        self.window.mainloop()