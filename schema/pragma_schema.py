import re
from dataclasses import dataclass
from schema.statement_schema import StatementSchema


# example:
# PRAGMA journal_mode = MEMORY;

@dataclass
class PragmaSchema(StatementSchema):
    statement: str
    base_instruction: str

    REGEX = r'PRAGMA\s+(\w+)\s*=\s*(\w+);'
    TYPE = 'pragma'

    def variable_name(self):
        return self.parse().group(1)

    def value(self):
        return self.parse().group(2)
