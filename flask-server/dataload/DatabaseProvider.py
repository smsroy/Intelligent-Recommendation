import sqlite3
import os

db_file_path = '../db/intellireco1.db'

def __connect_db__():
    """Connect to the specific database."""
    package_dir = os.path.abspath(os.path.dirname(__file__))
    final_path = os.path.join(package_dir, db_file_path)
    connection = sqlite3.connect(final_path)
    connection.row_factory = sqlite3.Row
    return connection


def get_db():
    """
    Open a new database connection.

    If there is none yet for the
    current application context.
    """
    return __connect_db__()

conn = get_db()
if conn is not None:
    print("DBProvider Working")
    conn.close()