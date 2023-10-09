# sqlite-schema-migrate

CLI tool allowing to manage and migrate sqlite database schemas,
from a single source schema file.

Example usage:

```
$ python __main__.py -s ./tests/fixtures/schema-samples/categories.sql database.db
```

The source schema file is read line by line, and for each statement, it will ensure that
the database follows the schema. If not, it will execute every missing statement.
To verify that a given statement is already present in the database, it will use a metadata
table in the sqlite database, namely "*_sqlite_schema_migrate*".


## Command line options

```
usage: python __main__.py [-h] [-f] [-s SCHEMA] [--init-db-schema] database
```

Options are described below:

- -h, --help: show the help command message and exit
- -f, --force: force the execution of all statements, even if they are already in the database. Especially, this is useful if a table already exists - it will recreate the table with the new schema and copy the data to the new table.
- -s SCHEMA, --schema SCHEMA: path to the source schema SQL file.
- --init-db-schema: initialize the database metadata table (*_sqlite_schema_migrate*) with the source schema file. This is useful only if you already have a sqlite database and want to start using this tool.
