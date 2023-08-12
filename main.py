import sys
import copy
from args import parsed_args
from schema import parser as schema_parser
import state_migrate
from migrate import apply as migrate_apply
import sqlite_db

if __name__ == "__main__":
    db = sqlite_db.Database(filepath=parsed_args.database)

    latest_schema_info = state_migrate.ensure_schema_migration_table_exists(db)

    stdin_content = sys.stdin.read()

    desired_schema = schema_parser.parse(stdin_content)
    previous_schema = schema_parser.parse(latest_schema_info.get("schema", {}))

    all_schema = migrate_apply.apply(
        local_parsed_schema=desired_schema,
        previous_parsed_schema=previous_schema,
        database=db,
    )
    resulting_schema = copy.deepcopy(desired_schema)
    resulting_schema.all = all_schema

    # insert the schema into the database
    state_migrate.update_schema_migration_table(db, str(resulting_schema))
