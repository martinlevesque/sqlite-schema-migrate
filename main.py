import sys
from schema import parser as schema_parser
from migrate import apply as migrate_apply
import sqlite_db

if __name__ == '__main__':
    db = sqlite_db.Database(filepath=sys.argv[1])
    print(f"db = {db}")
    stdin_content = sys.stdin.read()

    desired_schema = schema_parser.parse(stdin_content)
    print(f"Desired schema: {desired_schema}")

    remote_schema = None  # todo

    migrate_apply.apply(local_schema=desired_schema, remote_schema=remote_schema, database=db)

    # remote_db_schema =
