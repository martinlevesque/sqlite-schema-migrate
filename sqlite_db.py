import sqlite3
from dataclasses import dataclass
from lib import log


# communicate with the sqlite database


@dataclass
class Database:
    filepath: str

    def __post_init__(self):
        self.conn = sqlite3.connect(self.filepath)
        log.debug(f"Connected to {self.filepath}")

    def first(self, query):
        return self.conn.execute(query).fetchone()

    def first_column(self, query):
        row = self.first(query)

        if row is None:
            return None

        return row[0]

    def execute(self, query, args=None, log_function=None):
        if log_function:
            log_function(f"Executing: {query} with args: {args}")

        if args is None:
            return self.conn.execute(query)

        return self.conn.execute(query, args)

    def commit(self):
        return self.conn.commit()

    def table_exists(self, table_name):
        return (
            self.first_column(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
            )
            is not None
        )

    def close(self):
        self.conn.close()
