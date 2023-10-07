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

    REGEX = r"DROP\s+(?P<entity_type>TABLE|INDEX)?\s*(?P<if_exists>IF\s+EXISTS)?\s*(?P<schema_name>\w+\.)?(?P<entity_name>\w+);"
    TYPE = "drop_entity"

    def id(self) -> str:
        return f"drop-{self.entity_type()}-{self.name()}"

    def entity_type(self) -> str:
        return self.parsed_variable("entity_type")

    def name(self) -> str:
        return self.entity_full_name()

    def is_if_exists(self) -> bool:
        return str(self.parsed_variable("if_exists")).upper() == "IF EXISTS"

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
