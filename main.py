import sys
import datetime
from schema import parser as schema_parser
import state_migrate
from migrate import apply as migrate_apply
import sqlite_db

if __name__ == "__main__":
    db = sqlite_db.Database(filepath=sys.argv[1])

    latest_schema_info = state_migrate.ensure_schema_migration_table_exists(db)

    stdin_content = sys.stdin.read()

    desired_schema = schema_parser.parse(stdin_content)
    previous_schema = schema_parser.parse(latest_schema_info.get("schema", {}))

    new_schema = migrate_apply.apply(
        local_schema=desired_schema, previous_schema=previous_schema, database=db
    )

    # insert the schema into the database
    state_migrate.update_schema_migration_table(db, str(new_schema))
