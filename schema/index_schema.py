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

    REGEX = r"CREATE\s+(UNIQUE)?\s*INDEX\s+(IF NOT EXISTS)?\s*(\w+\.)?(\w+)\s+ON\s+(\w+)\s*\(((\w+(,\s?)?)+)\)\s*(WHERE\s+(.*))?;"
    TYPE = "create_index"

    def id(self) -> str:
        return f"index-{self.name()}"

    def if_not_exists(self) -> str | None:
        return self.parse().group(2)

    def schema_name(self) -> str:
        return self.schema_name_at(3)

    def index_name(self) -> str:
        return self.parse().group(4)

    def index_full_name(self) -> str:
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.index_name()
        )

    def name(self) -> str:
        return self.index_full_name()

    def table_name(self) -> str:
        return self.parse().group(5)

    def is_unique(self) -> bool:
        return str(self.parse().group(1)).upper() == "UNIQUE"

    def columns(self) -> list[str]:
        columns_str = str(self.parse().group(6)).split(",")

        return [column.strip() for column in columns_str if column.strip()]

    def where_clause(self) -> str:
        return self.parse().group(10)

    def value(self) -> str:
        if self.override_value is not None:
            return self.override_value

        self.override_value = self.parse().group(2)

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
