"""
=============================================================
 IoT + DLT Integration Project
 Environmental Monitoring System

 Database Viewer
=============================================================

Displays environmental records stored in the SQLite database.

Navigation:
    ←  Previous Record
    →  Next Record
    Home  First Record
    End   Last Record
    Esc   Exit

Author:
International Hellenic University
Computer and Electronic Systems Engineering
"""

import os
import sqlite3
import msvcrt


# =============================================================
# Configuration
# =============================================================

DATABASE_PATH = "storage/environmental_data.db"
TABLE_NAME = "environment_data"
SCREEN_WIDTH = 80


# =============================================================
# Screen Functions
# =============================================================

def clear_screen():
    """Clears the console window."""
    os.system("cls" if os.name == "nt" else "clear")


def line():
    """Prints a separator line."""
    print("=" * SCREEN_WIDTH)


def small_line():
    """Prints a secondary separator line."""
    print("-" * SCREEN_WIDTH)


def center(text):
    """Prints centered text."""
    print(text.center(SCREEN_WIDTH))


# =============================================================
# Banner
# =============================================================

def show_banner():

    clear_screen()

    line()
    center("IoT + DLT ENVIRONMENTAL DATABASE VIEWER")
    line()

    print()
    print(f"Database : {DATABASE_PATH}")
    print(f"Table    : {TABLE_NAME}")
    print("Mode     : Interactive Viewer")
    print()

    small_line()


# =============================================================
# Keyboard Functions
# =============================================================

KEY_LEFT = "LEFT"
KEY_RIGHT = "RIGHT"
KEY_HOME = "HOME"
KEY_END = "END"
KEY_ESC = "ESC"
KEY_OTHER = "OTHER"


def get_key():
    """
    Waits for a keyboard key and translates
    special Windows keys into readable values.
    """

    key = msvcrt.getch()

    if key == b'\x1b':
        return KEY_ESC

    if key in (b'\x00', b'\xe0'):

        special = msvcrt.getch()

        if special == b'K':
            return KEY_LEFT

        if special == b'M':
            return KEY_RIGHT

        if special == b'G':
            return KEY_HOME

        if special == b'O':
            return KEY_END

    return KEY_OTHER

# =============================================================
# Database Functions
# =============================================================

def connect_database():
    """
    Opens a connection to the SQLite database.
    Returns:
        sqlite3.Connection or None
    """

    if not os.path.exists(DATABASE_PATH):

        show_banner()

        print("ERROR")
        print()
        print("Database file not found.")
        print()
        print(f"Expected location:")
        print(DATABASE_PATH)
        print()

        input("Press ENTER to close...")

        return None

    try:

        connection = sqlite3.connect(DATABASE_PATH)

        return connection

    except sqlite3.Error as error:

        show_banner()

        print("Database connection failed.")
        print()
        print(error)
        print()

        input("Press ENTER to close...")

        return None


# =============================================================
# Load Records
# =============================================================

def load_records(connection):
    """
    Reads every environmental record from the database.
    Returns a list of tuples.
    """

    try:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                cycle_id,
                timestamp,
                temperature,
                humidity,
                air_quality,
                hash,
                transaction_id
            FROM environment_data
            ORDER BY cycle_id ASC
        """)

        records = cursor.fetchall()

        return records

    except sqlite3.Error as error:

        show_banner()

        print("Unable to read the database.")
        print()
        print(error)
        print()

        input("Press ENTER to close...")

        return None

# =============================================================
# Database Information
# =============================================================

def show_empty_database():

    show_banner()

    print("The database does not contain any records.")
    print()
    print("Start the IoT project first to generate")
    print("environmental monitoring cycles.")
    print()

    input("Press ENTER to close...")


def show_summary(total):

    show_banner()

    print("DATABASE SUCCESSFULLY LOADED")
    print()

    small_line()

    print(f"Total Records : {total}")

    small_line()

    print()
    print("Viewer closed successfully.")
    print()

    input("Press ENTER to close...")

# =============================================================
# Record Viewer
# =============================================================

def display_record(record, current_index, total_records):
    """
    Displays one environmental record.
    """

    (
        database_id,
        cycle_id,
        timestamp,
        temperature,
        humidity,
        air_quality,
        hash_value,
        transaction_id
    ) = record

    show_banner()

    print(f"Record {current_index + 1} of {total_records}")

    small_line()

    print(f"Database ID        : {database_id}")
    print(f"Cycle ID           : {cycle_id}")
    print(f"Timestamp          : {timestamp}")
    print(f"Temperature (°C)   : {temperature:.2f}")
    print(f"Humidity (%)       : {humidity:.2f}")
    print(f"Air Quality Index  : {air_quality}")

    small_line()

    print("SHA-256 Hash")
    print()

    if hash_value:
        print(hash_value)
    else:
        print("No hash available.")

    small_line()

    print("Shimmer Transaction ID")
    print()

    if transaction_id:
        print(transaction_id)
    else:
        print("No transaction available.")

    small_line()

    print()

    display_footer(current_index, total_records)


# =============================================================
# Footer
# =============================================================

def display_footer(current_index, total_records):

    print(f"Current Record : {current_index + 1} / {total_records}")

    print()

    print("← Previous    → Next    Home First    End Last    ESC Exit")

# =============================================================
# Interactive Viewer
# =============================================================

def viewer_loop(records):
    """
    Interactive database viewer.

    Navigation:

        LEFT   -> Previous Record
        RIGHT  -> Next Record
        HOME   -> First Record
        END    -> Last Record
        ESC    -> Exit
    """

    current_index = 0

    total_records = len(records)

    while True:

        display_record(
            records[current_index],
            current_index,
            total_records
        )

        key = get_key()

        # -----------------------------------------------------
        # Previous Record
        # -----------------------------------------------------

        if key == KEY_LEFT:

            if current_index > 0:
                current_index -= 1

            continue

        # -----------------------------------------------------
        # Next Record
        # -----------------------------------------------------

        if key == KEY_RIGHT:

            if current_index < total_records - 1:
                current_index += 1

            continue

        # -----------------------------------------------------
        # First Record
        # -----------------------------------------------------

        if key == KEY_HOME:

            current_index = 0

            continue

        # -----------------------------------------------------
        # Last Record
        # -----------------------------------------------------

        if key == KEY_END:

            current_index = total_records - 1

            continue

        # -----------------------------------------------------
        # Exit Viewer
        # -----------------------------------------------------

        if key == KEY_ESC:

            break

        # -----------------------------------------------------
        # Ignore every other key
        # -----------------------------------------------------

        continue

# =============================================================
# Main Program
# =============================================================

def main():

    connection = connect_database()

    if connection is None:
        return

    try:

        records = load_records(connection)

        if records is None:
            return

        if len(records) == 0:

            show_empty_database()

            return

        viewer_loop(records)

        show_summary(len(records))

    finally:

        connection.close()


# =============================================================
# Program Entry Point
# =============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        clear_screen()

        print("Program interrupted by user.")

    except Exception as error:

        clear_screen()

        line()
        center("UNEXPECTED ERROR")
        line()

        print()
        print(error)
        print()

        input("Press ENTER to close...")