cd src
BASE_CMD="python main.py"

rm -f test.db
cat ../tests/fixtures/schema-samples/categories.sql | $BASE_CMD test.db
sqlite3 -line test.db 'PRAGMA default_cache_size;' | grep "cache_size = 500000"

# create table check
echo "## create table check"
sqlite3 -line test.db '.schema categories' | grep "CREATE TABLE categories"

# alter table check
echo "## alter table check"
sqlite3 -line test.db '.schema categories' | grep "description VARCHAR(200)"

# simple --force case
echo "## simple --force case"
sqlite3 test.db 'insert into categories (name, description) values ("cat1", "cat1desc")'
sqlite3 test.db 'select name, description from categories;' | grep 'cat1|cat1desc'

cat ../tests/fixtures/schema-samples/categories_with_new_column.sql | $BASE_CMD --force test.db
sqlite3 test.db 'select name, description, age from categories;' | grep 'cat1|cat1desc|18'

# --schema argument
echo "## --schema argument"
rm -f test.db
$BASE_CMD test.db --schema ../tests/fixtures/schema-samples/categories.sql
sqlite3 -line test.db '.schema categories' | grep "CREATE TABLE categories"

# --init-db-schema argument
echo "## --init-db-schema argument"
rm -f test.db
$BASE_CMD test.db --schema ../tests/fixtures/schema-samples/categories.sql
sqlite3 -line test.db 'drop table _sqlite_schema_migrate;'
$BASE_CMD test.db --schema ../tests/fixtures/schema-samples/categories.sql --init-db-schema
sqlite3 -line test.db 'select * from _sqlite_schema_migrate;' | grep "CREATE TABLE categories"
sqlite3 -line test.db 'select * from _sqlite_schema_migrate;' | grep "ALTER TABLE categories"
