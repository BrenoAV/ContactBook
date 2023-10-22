import logging
import sqlite3
from pathlib import Path
from typing import Optional


def create_connection(database_path: str) -> Optional[sqlite3.Connection]:
    database_path_obj = Path(database_path)
    if database_path_obj.exists():
        con = sqlite3.connect(database_path_obj)
        logging.info("Connection created with the file %s.", database_path_obj)
        return con
    return None


def get_all_rows(
    conn: sqlite3.Connection, table_name: str
) -> list[tuple[int, str, str, str]]:
    res = conn.execute("SELECT * FROM %s" % table_name)
    return res.fetchall()
