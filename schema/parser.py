
import re

# read an input sql schema content and provide a hash representing the schema

def parse(str_content):
    result = {
        "pragmas": {},
        "tables": {},
        # "views": {},
        # "triggers": {},
        "indexes": {}
    }

    pattern = re.compile(r'(?i)(CREATE TABLE|ALTER TABLE|PRAGMA).*?;', re.DOTALL)

    for match in pattern.finditer(str_content):
        print('current match:')
        print(match.group())

    return result
