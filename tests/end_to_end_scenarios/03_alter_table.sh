set -e

sqlite3 -line test.db '.schema categories' | grep "description VARCHAR(200)"
