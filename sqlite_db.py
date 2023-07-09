
import sqlite3
from dataclasses import dataclass


# communicate with the sqlite database

@dataclass
class Database:
    filepath: str

    def __post_init__(self):
        self.conn = sqlite3.connect(self.filepath)
        print(f"Connected to {self.filepath}")

    def first(self, query):
        return self.conn.execute(query).fetchone()

    def first_column(self, query):
        row = self.first(query)

        if row is None:
            return None

        return row[0]

    #def __post


def close(db_conn):
    db_conn.close()
