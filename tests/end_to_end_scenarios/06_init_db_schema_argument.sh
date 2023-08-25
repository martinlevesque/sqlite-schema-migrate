rm -f test.db
$BASE_CMD test.db --schema tests/fixtures/schema-samples/categories.sql
sqlite3 -line test.db 'drop table _sqlite_schema_migrate;'
$BASE_CMD test.db --schema tests/fixtures/schema-samples/categories.sql --init-db-schema
sqlite3 -line test.db 'select * from _sqlite_schema_migrate;' | grep "CREATE TABLE categories"
sqlite3 -line test.db 'select * from _sqlite_schema_migrate;' | grep "ALTER TABLE categories"