import os

import psycopg
from psycopg.rows import dict_row


def connect():
    url = os.environ.get("NAVEBASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set.")
    return psycopg.connect(url, row_factory=dict_row, connect_timeout=10)


def get_conn():
    with connect() as conn:
        yield conn
