sqlite3 test.db 'insert into categories (name, description) values ("cat1", "cat1desc")'
sqlite3 test.db 'select name, description from categories;' | grep 'cat1|cat1desc'

cat tests/fixtures/schema-samples/categories_with_new_column.sql | $BASE_CMD --force test.db
sqlite3 test.db 'select name, description, age from categories;' | grep 'cat1|cat1desc|18'