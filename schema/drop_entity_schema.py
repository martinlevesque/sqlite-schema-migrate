import re
from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema
from lib import log


# example:
# DROP (TABLE|INDEX) IF EXISTS schema_name.table_name;


@dataclass
class DropEntitySchema(StatementSchema):
    statement: str
    base_instruction: str
    override_value: Optional[str] = None

    REGEX = r"DROP\s+(TABLE|INDEX)?\s*(IF EXISTS)?\s*(\w+\.)?(\w+);"
    TYPE = "drop_entity"

    def schema_name(self):
        schema_txt = self.parse().group(3)

        if not schema_txt:
            return ""

        # todo refactor/reuse
        # if ends with a dot, remove it
        if schema_txt and schema_txt.endswith("."):
            schema_txt = schema_txt[:-1]

        return schema_txt

    def entity_name(self):
        return self.parse().group(4)

    def entity_full_name(self):
        schema_name = self.schema_name()

        if schema_name:
            return f"{schema_name}.{self.entity_name()}"

        return self.entity_name()

    def entity_type(self):
        return self.parse().group(1).upper()

    def name(self):
        return self.entity_full_name()

    def table_name(self):
        return self.parse().group(5)

    def is_if_exists(self):
        return str(self.parse().group(2)).upper() == "IF EXISTS"

    @staticmethod
    def apply_changes(current_schema=None, previous_schema=None, database=None):
        if current_schema:
            # it is new:
            database.execute(str(current_schema), log_function=log.info)

    def __str__(self):
        if_exists_txt = "IF EXISTS" if self.is_if_exists() else ""
        return f"DROP {self.entity_type()} {if_exists_txt} {self.entity_full_name()};"
