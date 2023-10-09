from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema
from lib import log
from sqlite_db import Database


# doc:
# https://www.sqlite.org/lang_createindex.html

# example:
# CREATE [UNIQUE] INDEX [IF NOT EXISTS] [schema_name.]index_name ON table_name (column_name [, ...]) [WHERE expr];


@dataclass
class IndexSchema(StatementSchema):
    statement: str
    base_instruction: str
    override_value: Optional[str] = None

    REGEX = (
        rf"CREATE\s+(?P<unique>UNIQUE)?\s*INDEX\s+{StatementSchema.REGEX_IF_NOT_EXISTS}"
        rf"?\s*{StatementSchema.REGEX_SCHEMA_NAME}?(?P<index_name>\w+)"
        rf"\s+ON\s+(?P<table_name>\w+)\s*\((?P<columns>(\w+(,\s?)?)+)\)\s*(WHERE\s+(?P<where_clause>.*))?;"
    )
    TYPE = "create_index"

    def id(self) -> str:
        return f"index-{self.name()}"

    def index_name(self) -> str:
        return self.parsed_variable("index_name")

    def index_full_name(self) -> str:
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.index_name()
        )

    def name(self) -> str:
        return self.index_full_name()

    def is_unique(self) -> bool:
        return str(self.parsed_variable("unique")).upper() == "UNIQUE"

    def columns(self) -> list[str]:
        columns_str = str(self.parsed_variable("columns")).split(",")

        return [column.strip() for column in columns_str if column.strip()]

    def where_clause(self) -> str:
        return self.parsed_variable("where_clause")

    def value(self) -> str:
        if self.override_value is not None:
            return self.override_value

        self.override_value = self.if_not_exists()

        return self.override_value

    @staticmethod
    def apply_changes(
        current_schema: StatementSchema | None,
        previous_schema: StatementSchema | None,
        database: Database,
        force: bool = False,
    ) -> str:
        state_result = ""

        if previous_schema is None and current_schema:
            # it is new:
            database.execute(str(current_schema), log_function=log.info)
            state_result = "create"
        elif current_schema is None and previous_schema:
            # it was removed:
            database.execute(previous_schema.destroy_cmd(), log_function=log.info)
            state_result = "remove"
        elif (
            current_schema
            and previous_schema
            and str(current_schema) != str(previous_schema)
        ):
            # recreate it
            database.execute(previous_schema.destroy_cmd(), log_function=log.info)
            database.execute(str(current_schema), log_function=log.info)
            state_result = "update"

        return state_result

    def destroy_cmd(self) -> str:
        return f"DROP INDEX IF EXISTS {self.index_full_name()};"

    def __str__(self) -> str:
        result = "CREATE "

        if self.is_unique():
            result += "UNIQUE "

        result += "INDEX "

        if self.if_not_exists():
            result += "IF NOT EXISTS "

        result += self.index_full_name()

        result += f" ON {self.table_name()} ({', '.join(self.columns())})"

        if self.where_clause():
            result += f" WHERE {self.where_clause()}"

        return f"{result};"
