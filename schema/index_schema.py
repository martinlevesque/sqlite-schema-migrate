import re
from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema


# doc:
# https://www.sqlite.org/lang_createindex.html

# example:
# CREATE [UNIQUE] INDEX [IF NOT EXISTS] [schema_name.]index_name ON table_name (column_name [, ...]) [WHERE expr];

# todo
# if find drop index, remove it from the schema

@dataclass
class IndexSchema(StatementSchema):
    statement: str
    base_instruction: str
    override_value: Optional[str] = None

    REGEX = r'CREATE\s+(UNIQUE)?\s+(\w+)\s*=\s*(\w+);'
    TYPE = 'pragma'

    def variable_name(self):
        return self.parse().group(1)

    def value(self):
        if self.override_value is not None:
            return self.override_value

        self.override_value = self.parse().group(2)

        return self.override_value

    def __str__(self):
        return f"PRAGMA {self.variable_name()} = {self.value()};"
