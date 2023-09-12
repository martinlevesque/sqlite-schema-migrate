import re
from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema
from lib import log
from sqlite_db import Database


# example:
# DROP (TABLE|INDEX) IF EXISTS schema_name.table_name;


@dataclass
class DropEntitySchema(StatementSchema):
    statement: str
    base_instruction: str
    override_value: Optional[str] = None

    REGEX = r"DROP\s+(TABLE|INDEX)?\s*(IF EXISTS)?\s*(\w+\.)?(\w+);"
    TYPE = "drop_entity"

    def id(self) -> str:
        return f"drop-{self.entity_type()}-{self.name()}"

    def schema_name(self) -> str:
        return self.schema_name_at(3)

    def entity_name(self) -> str:
        return self.parse().group(4)

    def entity_full_name(self) -> str:
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.entity_name()
        )

    def entity_type(self) -> str:
        return self.parse().group(1).upper()

    def name(self) -> str:
        return self.entity_full_name()

    def table_name(self) -> str:
        return self.parse().group(5)

    def is_if_exists(self) -> bool:
        return str(self.parse().group(2)).upper() == "IF EXISTS"

    @staticmethod
    def apply_changes(
        current_schema: StatementSchema | None,
        previous_schema: StatementSchema | None,
        database: Database,
        force: bool = False,
    ) -> str:
        state_result = ""

        if current_schema:
            # it is new:
            database.execute(str(current_schema), log_function=log.info)
        elif current_schema is None and previous_schema:
            state_result = "remove"

        return state_result

    def __str__(self) -> str:
        if_exists_txt = "IF EXISTS" if self.is_if_exists() else ""
        return f"DROP {self.entity_type()} {if_exists_txt} {self.entity_full_name()};"
