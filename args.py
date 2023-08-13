import argparse

parser = argparse.ArgumentParser(
    prog="sqlite-schema-migration",
    description="Migrate an sqlite3 database from a file schema",
)
parser.add_argument(
    "database", metavar="database", type=str, help="the database file to migrate"
)
parser.add_argument(
    "-f",
    "--force",
    action="store_true",
    help="force the origin schema (e.g., if table exists, drop it and recreate, and copy it)",
)

parser.add_argument(
    "-s",
    "--schema",
    help="SQL schema file to migrate to",
)

parsed_args = parser.parse_args()
