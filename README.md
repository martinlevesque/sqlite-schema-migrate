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

## Example usage

Say you have the following schema file (schema.sql) with one table and 3 rows:

```sql
CREATE TABLE categories (
    id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL default(';'),
    parent_category_id INTEGER NULL,
    last_update TIMESTAMP NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(parent_category_id) REFERENCES categories(id),
    UNIQUE (name)
);

INSERT INTO categories (id, name) VALUES (1, 'category-test-1');
INSERT INTO categories (id, name) VALUES (2, 'category-test-2');
INSERT INTO categories (id, name) VALUES (3, 'category-test-3');
```

Create the initial database file with:

```
$ python __main__.py -s schema.sql database.db
```


Now what if you would like to add a new column "new_column" in this table, just update the schema file to:

```sql
CREATE TABLE categories (
    id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL default(';'),
    parent_category_id INTEGER NULL,
    last_update TIMESTAMP NULL,
    new_column VARCHAR(200) NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(parent_category_id) REFERENCES categories(id),
    UNIQUE (name)
);

INSERT INTO categories (id, name) VALUES (1, 'category-test-1');
INSERT INTO categories (id, name) VALUES (2, 'category-test-2');
INSERT INTO categories (id, name) VALUES (3, 'category-test-3');
```

and rerun the command with --force flag, so that it recreates the table and copy the data:


```
$ python __main__.py -s schema.sql --force database.db
```

The output of this command will be the following:

```
DEBUG: Connected to database.db
DEBUG: Ensuring schema migration table exists
DEBUG: Schema migration table already exists... skipping
INFO: Executing: BEGIN TRANSACTION;
DEBUG: Table categories already exists and has changes...
INFO: Executing: ALTER TABLE categories RENAME TO categories_old;
INFO: Executing: CREATE TABLE categories (  id INTEGER NOT NULL,    name VARCHAR(200) NOT NULL default(';'),    parent_category_id INTEGER NULL,    last_update TIMESTAMP NULL,     new_column INTEGER NULL,    PRIMARY KEY (id),   FOREIGN KEY(parent_category_id) REFERENCES categories(id),  UNIQUE (name) );
INFO: Executing: INSERT INTO categories (parent_category_id, name, id, last_update) SELECT parent_category_id, name, id, last_update FROM categories_old;
INFO: Executing: DROP TABLE categories_old;
INFO: Executing: COMMIT;
DEBUG: Updating schema migration table with schema
DEBUG: Schema migration already exists... updating
```


