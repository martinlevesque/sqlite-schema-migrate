rm -f test.db
$BASE_CMD test.db --schema ../tests/fixtures/schema-samples/categories.sql
$BASE_CMD test.db --schema ../tests/fixtures/schema-samples/categories_removing_alter_table_test.sql

sqlite3 -line test.db 'select * from _sqlite_schema_migrate;' | grep "ALTER TABLE categories ADD COLUMN description"

if [ $? -eq 0 ]; then
    echo "## when removing an alter table, _sqlite_schema_migrate: NOK"
    exit 1
fi