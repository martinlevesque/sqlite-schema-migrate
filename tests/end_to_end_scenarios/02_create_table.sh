set -e

sqlite3 -line test.db '.schema categories' | grep "CREATE TABLE categories"