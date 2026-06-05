import os

import mysql.connector


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "milk_tea_group_db"),
    "charset": os.getenv("DB_CHARSET", "utf8mb4"),
    "autocommit": False,
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def _close(cursor=None, connection=None):
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()


def fetch_one(sql, params=None):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        return cursor.fetchone()
    finally:
        _close(cursor, connection)


def fetch_all(sql, params=None):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        return cursor.fetchall()
    finally:
        _close(cursor, connection)


def execute_write(sql, params=None):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, params or ())
        connection.commit()
        return cursor.lastrowid
    except Exception:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        _close(cursor, connection)
