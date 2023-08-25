rm -f test.db
$BASE_CMD test.db --schema tests/fixtures/schema-samples/categories.sql
$BASE_CMD test.db --schema tests/fixtures/schema-samples/categories_removing_drop_entity_test.sql

sqlite3 -line test.db 'select * from _sqlite_schema_migrate;' | grep "DROP INDEX IF EXISTS myindex_test"

if [ $? -eq 0 ]; then
    echo "## when removing a drop entity index, _sqlite_schema_migrate: NOK"
    exit 1
fi