import argparse

parser = argparse.ArgumentParser(
    prog='sqlite-schema-migration', description='Migrate an sqlite3 database from a file schema')
parser.add_argument('database', metavar='database', type=str,
                    help='the database file to migrate')
parser.add_argument('-f', '--force', action='store_true')

parsed_args = parser.parse_args()
