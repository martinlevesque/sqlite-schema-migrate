
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

    pattern = re.compile(r'(?i)((CREATE TABLE|ALTER TABLE|PRAGMA).*?;)\s*(--[^\n]*)?\n', re.DOTALL | re.MULTILINE)

    for match in pattern.finditer(f"{str_content}\n"):
        line = match.group(1)
        base_instruction = match.group(2).upper()
        print('current match:')
        print(f"line = =={line}==")
        print(f"base_instruction = =={base_instruction}==")

    return result
