
from lib import log

TABLE_NAME_SQLITE_SCHEMA_MIGRATE = "_sqlite_schema_migrate"


def schema_migration_table_exists(database):
    return database.table_exists(TABLE_NAME_SQLITE_SCHEMA_MIGRATE)


def ensure_schema_migration_table_exists(database):
    log.debug(f"Ensuring schema migration table exists")

    if not schema_migration_table_exists(database):
        log.info("Creating schema migration table...")
        database.execute(f"CREATE TABLE {TABLE_NAME_SQLITE_SCHEMA_MIGRATE} (name TEXT, applied_at DATETIME);")
    else:
        log.debug("Schema migration table already exists... skipping")
