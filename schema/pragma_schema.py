from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema
from lib import log
from sqlite_db import Database


# example:
# PRAGMA journal_mode = MEMORY;


@dataclass
class PragmaSchema(StatementSchema):
    statement: str
    base_instruction: str
    override_value: Optional[str] = None

    REGEX = r"PRAGMA\s+(\w+)\s*=\s*(\w+);"
    TYPE = "pragma"

    def id(self) -> str:
        return f"pragma-{self.name()}"

    def name(self) -> str:
        return self.variable_name()

    def variable_name(self) -> str:
        return str(self.parse().group(1)).lower()

    def value(self) -> str:
        if self.override_value is not None:
            return self.override_value

        self.override_value = self.parse().group(2)

        return self.override_value

    @staticmethod
    def apply_changes(
        current_schema: PragmaSchema,
        previous_schema: PragmaSchema | None,
        database: Database,
        force: bool = False,
    ):
        desired_value = current_schema.value()

        if previous_schema is None or previous_schema.value() != desired_value:
            current_schema.override_value = desired_value
            database.execute(str(current_schema), log_function=log.info)

            mutated_value = database.first_column(f"PRAGMA {current_schema.name()};")
            current_schema.override_value = mutated_value

    def __str__(self):
        return f"PRAGMA {self.variable_name()} = {self.value()};"
