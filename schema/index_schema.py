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

    REGEX = r"CREATE\s+(UNIQUE)?\s*INDEX\s+(IF NOT EXISTS)?\s*(\w+\.)?(\w+)\s+ON\s+(\w+)\s*\(((\w+(,\s)?)+)\)\s*(WHERE\s+.*)?;"
    TYPE = "create_index"

    def schema_name(self):
        schema_txt = self.parse().group(3)

        if not schema_txt:
            return ""

        # if ends with a dot, remove it
        if schema_txt and schema_txt.endswith("."):
            schema_txt = schema_txt[:-1]

        return schema_txt

    def index_name(self):
        return self.parse().group(4)

    def index_full_name(self):
        schema_name = self.schema_name()

        if schema_name:
            return f"{schema_name}.{self.index_name()}"

        return self.index_name()

    def table_name(self):
        return self.parse().group(5)

    def is_unique(self):
        return str(self.parse().group(1)).upper() == "UNIQUE"

    def columns(self):
        columns_str = str(self.parse().group(6)).split(",")

        return [column.strip() for column in columns_str if column.strip()]

    def where_clause(self):
        return self.parse().group(9)

    def value(self):
        if self.override_value is not None:
            return self.override_value

        self.override_value = self.parse().group(2)

        return self.override_value

    def __str__(self):
        return f"PRAGMA {self.variable_name()} = {self.value()};"
