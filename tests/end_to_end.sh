rm -f test.db
cat tests/fixtures/schema-samples/categories.sql | python main.py test.db
sqlite3 -line test.db 'PRAGMA default_cache_size;' | grep "cache_size = 500000"

# create table check
sqlite3 -line test.db '.schema categories' | grep "CREATE TABLE categories"

# alter table check
sqlite3 -line test.db '.schema categories' | grep "description VARCHAR(200)"
