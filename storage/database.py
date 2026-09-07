"""
IoT + DLT Integration Project

SQLite Database Management
Environmental Data Storage
"""

import sqlite3


DB_NAME = "storage/environmental_data.db"


def initialize_database():
    """
    Creates the SQLite database and the
    environmental data table if they do not exist.
    """

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    # Create the environmental data table
    # if it does not already exist.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS environment_data (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            cycle_id INTEGER NOT NULL,

            timestamp TEXT NOT NULL,

            temperature REAL NOT NULL,

            humidity REAL NOT NULL,

            air_quality INTEGER NOT NULL,

            hash TEXT,

            transaction_id TEXT

        )
        """
    )

    connection.commit()
    connection.close()

    print("Database initialized.")


def insert_cycle(cycle):
    """
    Stores one complete environmental
    measurement cycle in the database.
    """

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    # Store a complete environmental
    # measurement cycle in the database.
    cursor.execute(
        """
        INSERT INTO environment_data (

            cycle_id,
            timestamp,
            temperature,
            humidity,
            air_quality,
            hash,
            transaction_id

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            cycle["cycle_id"],
            cycle["timestamp"],
            cycle["temperature"],
            cycle["humidity"],
            cycle["air_quality"],
            cycle["hash"],
            cycle["transaction_id"]
        )
    )

    connection.commit()
    connection.close()


def get_last_cycle_id():
    """
    Returns the latest stored cycle ID.
    If the database is empty, returns 0.
    """

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()
    
    # Retrieve the highest stored cycle ID.
    cursor.execute(
        """
        SELECT MAX(cycle_id)
        FROM environment_data
        """
    )

    result = cursor.fetchone()

    connection.close()

    if result[0] is None:
        return 0

    return result[0]


if __name__ == "__main__":

    # Create the database when this file
    # is executed directly.
    initialize_database()