import sqlite3

print(f"sqlite version: {sqlite3.version}")

# todo, parse chunks:
# PRAGMA|CREATE TABLE|DROP TABLE|ALTER TABLE|CREATE INDEX|DROP INDEX ... ; (line ends with ;)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('PyCharm')

