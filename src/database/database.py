import logging
import sqlite3
from pathlib import Path
from typing import Any, Optional


def create_connection(database_path: str) -> sqlite3.Connection:
    database_path_obj = Path(database_path)
    con = sqlite3.connect(database_path_obj)
    logging.info("Connection created to the database %s.", database_path_obj)
    return con


def create_table_schema(
    conn: sqlite3.Connection, table_name: str, sql_columns: str
) -> None:
    conn.execute(
        f"""CREATE TABLE IF NOT EXISTS {table_name}(
        {sql_columns}
    );"""
    )
    conn.commit()


def get_all_columns(conn: sqlite3.Connection, table_name: str) -> list[Any]:
    res = conn.execute(f"""PRAGMA table_info({table_name})""")
    columns_pragma = res.fetchall()
    acc_column_name = []
    for column_pragma in columns_pragma:
        acc_column_name.append(column_pragma[1])
    return acc_column_name


def get_all_rows(conn: sqlite3.Connection, table_name: str) -> list[list[Any]]:
    res = conn.execute(f"SELECT * FROM {table_name}")
    return res.fetchall()


def get_one_row(conn: sqlite3.Connection, table_name: str, row: int) -> Optional[list]:
    res = conn.execute(f"SELECT * FROM {table_name} WHERE id={row}")
    return res.fetchone()


def add_record(
    conn: sqlite3.Connection, table_name: str, columns: list[str], values: list[Any]
) -> None:
    conn.execute(
        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES (?, ?, ?)", values
    )
    conn.commit()


def update_record(
    conn: sqlite3.Connection, table_name: str, row: int, column: str, new_value: Any
) -> None:
    conn.execute(
        f"""
        UPDATE {table_name}
        SET {column}='{new_value}'
        WHERE id={row}
        """
    )
    conn.commit()


def delete_record(conn: sqlite3.Connection, table_name: str, row: int) -> None:
    conn.execute(
        f"""
        DELETE FROM {table_name} WHERE id={row}
        """
    )
    conn.commit()


def delete_all_records(conn: sqlite3.Connection, table_name: str) -> None:
    conn.execute(
        f"""
            DELETE FROM {table_name}
        """
    )
    conn.commit()
