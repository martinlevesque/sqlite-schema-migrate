rm -f test.db
$BASE_CMD test.db --schema ../tests/fixtures/schema-samples/categories.sql
sqlite3 -line test.db '.schema categories' | grep "CREATE TABLE categories"