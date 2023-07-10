import re
from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema


# example:
# PRAGMA journal_mode = MEMORY;

@dataclass
class PragmaSchema(StatementSchema):
    statement: str
    base_instruction: str
    force_value: Optional[str] = None

    REGEX = r'PRAGMA\s+(\w+)\s*=\s*(\w+);'
    TYPE = 'pragma'

    def variable_name(self):
        return self.parse().group(1)

    def value(self):
        if self.force_value is not None:
            return self.force_value

        self.force_value = self.parse().group(2)

        return self.force_value

    def __str__(self):
        return f"PRAGMA {self.variable_name()} = {self.value()};"
