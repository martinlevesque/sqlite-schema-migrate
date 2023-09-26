set -e

rm -f test.db
cat tests/fixtures/schema-samples/categories.sql | $BASE_CMD test.db
sqlite3 -line test.db 'PRAGMA default_cache_size;' | grep "cache_size = 500000"
sqlite3 -line test.db 'select name from categories where name = "category-test-1"' | grep "category-test-1"
sqlite3 -line test.db 'select name from categories where name = "category-test-1"' | grep "category-test-1" | wc -l | grep "1"
sqlite3 -line test.db 'select name from categories where name = "category-test-2"' | grep "category-test-2"
sqlite3 -line test.db 'select name from categories where name = "category-test-2"' | grep "category-test-2" | wc -l | grep "1"
sqlite3 -line test.db 'select name from categories where id = 3' | grep "category-test-4" | wc -l | grep "1"

sqlite3 -line test.db 'select name from categories where id = 4' | grep "category-test-5" | wc -l | grep "0"

# check that the trigger worked
current_year=`date +%Y`
sqlite3 -line test.db 'select last_update from categories where id = 3' | grep "$current_year"

