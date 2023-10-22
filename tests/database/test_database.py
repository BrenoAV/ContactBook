import os
import sqlite3
import tempfile
from typing import Generator

import pytest

from src.database.database import (
    add_record,
    create_connection,
    create_table_schema,
    delete_all_records,
    delete_record,
    get_all_columns,
    get_all_rows,
    get_one_row,
    update_record,
)


@pytest.fixture(scope="session")
def db_path() -> Generator[str, None, None]:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    tmp_name: str = tmp_file.name
    # Creating a valid database
    conn = sqlite3.connect(tmp_name)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE Contact(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        job TEXT,
        email TEXT NOT NULL
    );"""
    )
    cur.execute(
        """
        INSERT INTO Contact (name, job, email) VALUES
        ("Linda", "Technical Lead", "linda@example.com"),
        ("Joe", "Senior Web Developer", "joe@example.com"),
        ("Lara", "Project Manager", "lara@example.com"),
        ("David", "Data Analyst", "david@example.com"),
        ("Jane", "Senior Python Developer", "jane@example.com")
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


def test_create_table_schema() -> None:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_name = tmp_file.name
    conn = create_connection(db_name)
    assert conn is not None
    create_table_schema(
        conn,
        table_name="Contact",
        sql_columns="""id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            job TEXT,
            email TEXT NOT NULL""",
    )
    res = conn.execute(f"""PRAGMA table_info(Contact)""")
    columns_pragma = res.fetchall()
    assert columns_pragma[0][1] == "id"
    assert columns_pragma[0][2] == "INTEGER"
    assert columns_pragma[1][1] == "name"
    assert columns_pragma[1][2] == "TEXT"
    assert columns_pragma[2][1] == "job"
    assert columns_pragma[2][2] == "TEXT"
    assert columns_pragma[3][1] == "email"
    assert columns_pragma[3][2] == "TEXT"
    os.remove(db_name)


def test_get_all_columns(db_path: str) -> None:
    conn = create_connection(db_path)
    assert conn is not None
    assert get_all_columns(conn, "Contact") == ["id", "name", "job", "email"]


def test_get_all_rows(db_path: str) -> None:
    conn = create_connection(db_path)
    assert conn is not None
    assert get_all_rows(conn, "Contact") == [
        (1, "Linda", "Technical Lead", "linda@example.com"),
        (2, "Joe", "Senior Web Developer", "joe@example.com"),
        (3, "Lara", "Project Manager", "lara@example.com"),
        (4, "David", "Data Analyst", "david@example.com"),
        (5, "Jane", "Senior Python Developer", "jane@example.com"),
    ]


def test_get_one_row_valid_id(db_path: str) -> None:
    conn = create_connection(db_path)
    assert conn is not None
    assert get_one_row(conn, table_name="Contact", row=3) == (
        3,
        "Lara",
        "Project Manager",
        "lara@example.com",
    )


def test_get_one_row_invalid_id(db_path: str) -> None:
    conn = create_connection(db_path)
    assert conn is not None
    assert get_one_row(conn, table_name="Contact", row=1000) is None


def test_add_record_valid(db_path: str) -> None:
    conn = create_connection(db_path)
    assert conn is not None
    add_record(
        conn,
        table_name="Contact",
        columns=["name", "job", "email"],
        values=["Breno", "ML Engineer", "breno@example.com"],
    )
    assert get_all_rows(conn, "Contact") == [
        (1, "Linda", "Technical Lead", "linda@example.com"),
        (2, "Joe", "Senior Web Developer", "joe@example.com"),
        (3, "Lara", "Project Manager", "lara@example.com"),
        (4, "David", "Data Analyst", "david@example.com"),
        (5, "Jane", "Senior Python Developer", "jane@example.com"),
        (6, "Breno", "ML Engineer", "breno@example.com"),
    ]


def test_update_record_valid(db_path: str) -> None:
    conn = create_connection(db_path)
    assert conn is not None
    update_record(conn, "Contact", row=2, column="name", new_value="John")
    update_record(conn, "Contact", row=2, column="job", new_value="None")
    update_record(conn, "Contact", row=2, column="email", new_value="john@example.com")
    assert get_one_row(conn, "Contact", row=2) == (
        2,
        "John",
        "None",
        "john@example.com",
    )


def test_delete_record_valid(db_path: str) -> None:
    conn = create_connection(db_path)
    assert conn is not None
    delete_record(conn, "Contact", row=2)
    res = get_one_row(conn, "Contact", row=2)
    assert res is None


def test_delete_all_records(db_path: str) -> None:
    conn = create_connection(db_path)
    assert conn is not None
    delete_all_records(conn, "Contact")
    res = get_all_rows(conn, "Contact")
    assert res == []
