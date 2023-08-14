rm -f test.db
cat tests/fixtures/schema-samples/categories.sql | python main.py test.db
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

cat tests/fixtures/schema-samples/categories_with_new_column.sql | python main.py --force test.db
sqlite3 test.db 'select name, description, age from categories;' | grep 'cat1|cat1desc|18'
