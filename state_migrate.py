import datetime
from lib import log

TABLE_NAME_SQLITE_SCHEMA_MIGRATE = "_sqlite_schema_migrate"


def schema_migration_table_exists(database):
    return database.table_exists(TABLE_NAME_SQLITE_SCHEMA_MIGRATE)


def ensure_schema_migration_table_exists(database):
    log.debug(f"Ensuring schema migration table exists")

    if not schema_migration_table_exists(database):
        log.info("Creating schema migration table...")
        database.execute(
            f"CREATE TABLE {TABLE_NAME_SQLITE_SCHEMA_MIGRATE} (schema TEXT, applied_at DATETIME);"
        )
    else:
        log.debug("Schema migration table already exists... skipping")

    # get latest schema
    latest_schema = database.first(
        f"SELECT schema, applied_at, rowid FROM {TABLE_NAME_SQLITE_SCHEMA_MIGRATE} ORDER BY applied_at DESC LIMIT 1;"
    )

    result = {"schema": None, "applied_at": None}

    if not latest_schema:
        return result

    return {
        "schema": latest_schema[0],
        "applied_at": latest_schema[1],
    }


def update_schema_migration_table(database, schema):
    log.debug("Updating schema migration table with schema")

    first_item = database.first(
        f"SELECT schema, rowid FROM {TABLE_NAME_SQLITE_SCHEMA_MIGRATE} ORDER BY applied_at DESC LIMIT 1;"
    )

    if first_item is None:
        database.execute(
            f"INSERT INTO {TABLE_NAME_SQLITE_SCHEMA_MIGRATE} (schema, applied_at) VALUES (?, ?);",
            (schema, datetime.datetime.now()),
        )
        database.commit()
    else:

        log.debug("Schema migration already exists... updating")
        database.execute(
            f"UPDATE {TABLE_NAME_SQLITE_SCHEMA_MIGRATE} SET schema = ?, applied_at = ? WHERE rowid = ?;",
            (schema, datetime.datetime.now(), first_item[1]),
        )
        database.commit()
