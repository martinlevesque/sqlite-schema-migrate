rm -f test.db
cat ../tests/fixtures/schema-samples/categories.sql | $BASE_CMD test.db
sqlite3 -line test.db 'PRAGMA default_cache_size;' | grep "cache_size = 500000"