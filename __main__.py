import sys
import copy
from args import parsed_args
from schema import parser as schema_parser
import state_migrate
from migrate import apply as migrate_apply
import sqlite_db
from lib import log


def main():
    db = sqlite_db.Database(filepath=parsed_args.database)

    db.execute("BEGIN TRANSACTION;", log_function=log.info)

    latest_schema_info = state_migrate.ensure_schema_migration_table_exists(db)

    if parsed_args.schema:
        with open(parsed_args.schema, "r") as f:
            stdin_content = f.read()
    else:
        stdin_content = sys.stdin.read()

    desired_schema = schema_parser.parse(stdin_content)

    if not parsed_args.init_db_schema:
        previous_schema = schema_parser.parse(latest_schema_info.get("schema", {}))

        all_schema = migrate_apply.apply(
            desired_schema, previous_schema, db, parsed_args.force
        )
    else:
        all_schema = desired_schema.all

    resulting_schema = copy.deepcopy(desired_schema)
    resulting_schema.all = all_schema

    # insert the schema into the database
    state_migrate.update_schema_migration_table(db, str(resulting_schema))

    db.execute("COMMIT;", log_function=log.info)


if __name__ == "__main__":
    main()
