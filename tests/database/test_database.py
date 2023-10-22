import os
import sqlite3
import tempfile
from typing import Generator

import pytest

from src.database.database import create_connection, get_all_rows


@pytest.fixture(scope="session")
def db_path() -> Generator[str, None, None]:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    tmp_name: str = tmp_file.name
    # Creating a valid database
    conn = sqlite3.connect(tmp_name)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE Contact(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        job TEXT,
        email TEXT NOT NULL
    );"""
    )
    cur.execute(
        """
        INSERT INTO Contact VALUES
        (1, "Linda", "Technical Lead", "linda@example.com"),
        (2, "Joe", "Senior Web Developer", "joe@example.com"),
        (3, "Lara", "Project Manager", "lara@example.com"),
        (4, "David", "Data Analyst", "david@example.com"),
        (5, "Jane", "Senior Python Developer", "jane@example.com");
    """
    )
    conn.commit()
    conn.close()
    yield tmp_name
    tmp_file.close()


def test_create_connection_existing_db(db_path: str) -> None:
    con = create_connection(db_path)
    assert isinstance(con, sqlite3.Connection)
    con.close()


def test_create_connection_nonexisting_db() -> None:
    con = create_connection("nonexisting.db")
    assert con is None


def test_show_all(db_path: str) -> None:
    conn = create_connection(db_path)
    assert conn is not None
    assert get_all_rows(conn, "Contact") == [
        (1, "Linda", "Technical Lead", "linda@example.com"),
        (2, "Joe", "Senior Web Developer", "joe@example.com"),
        (3, "Lara", "Project Manager", "lara@example.com"),
        (4, "David", "Data Analyst", "david@example.com"),
        (5, "Jane", "Senior Python Developer", "jane@example.com"),
    ]
