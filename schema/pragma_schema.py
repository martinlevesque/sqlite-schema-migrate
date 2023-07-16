from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema


# example:
# PRAGMA journal_mode = MEMORY;


@dataclass
class PragmaSchema(StatementSchema):
    statement: str
    base_instruction: str
    override_value: Optional[str] = None

    REGEX = r"PRAGMA\s+(\w+)\s*=\s*(\w+);"
    TYPE = "pragma"

    def variable_name(self):
        return str(self.parse().group(1)).lower()

    def value(self):
        if self.override_value is not None:
            return self.override_value

        self.override_value = self.parse().group(2)

        return self.override_value

    def __str__(self):
        return f"PRAGMA {self.variable_name()} = {self.value()};"
