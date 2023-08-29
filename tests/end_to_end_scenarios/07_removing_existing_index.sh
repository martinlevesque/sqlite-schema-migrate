
rm -f test.db
$BASE_CMD test.db --schema tests/fixtures/schema-samples/categories.sql
$BASE_CMD test.db --schema tests/fixtures/schema-samples/categories_removing_index_myindex_test.sql
sqlite3 -line test.db '.schema'
sqlite3 -line test.db '.schema' | grep "CREATE INDEX myindex_test"

if [ $? -eq 0 ]; then
    echo "## when removing an existing index, .schema: NOK"
    exit 1
fi

sqlite3 -line test.db 'select * from _sqlite_schema_migrate;' | grep "CREATE INDEX myindex_test"

if [ $? -eq 0 ]; then
    echo "## when removing an existing index, _sqlite_schema_migrate: NOK"
    exit 1
fi