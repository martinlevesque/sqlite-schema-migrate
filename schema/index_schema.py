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

    REGEX = r'CREATE\s+(UNIQUE)?\s*INDEX\s+(IF NOT EXISTS)?\s*(\w+\.)?(\w+)\s+ON\s+(\w+)\s*\(((\w+(,\s)?)+)\);'
    TYPE = 'pragma'

    def index_name(self):
        return self.parse().group(4)

    def table_name(self):
        return self.parse().group(5)

    def is_unique(self):
        return str(self.parse().group(1)).upper() == 'UNIQUE'

    def columns(self):
        columns_str = str(self.parse().group(6)).split(',')

        return [column.strip() for column in columns_str if column.strip()]


    def value(self):
        if self.override_value is not None:
            return self.override_value

        self.override_value = self.parse().group(2)

        return self.override_value

    def __str__(self):
        return f"PRAGMA {self.variable_name()} = {self.value()};"
