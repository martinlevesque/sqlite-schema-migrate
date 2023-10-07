from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema
from lib import log
from sqlite_db import Database


@dataclass
class ViewSchema(StatementSchema):
    statement: str
    base_instruction: str
    override_value: Optional[str] = None

    REGEX = rf"CREATE\s+(?P<temp>TEMP|TEMPORARY)?\s*VIEW\s+(?P<if_not_exists>IF NOT EXISTS)?\s*(?P<schema_name>{StatementSchema.REGEX_TERM_NAME}\.)?(?P<view_name>{StatementSchema.REGEX_TERM_NAME})\s*(?P<remaining>.+);"
    TYPE = "create_view"

    def id(self) -> str:
        return f"view-{self.name()}"

    def prepared_input_statement(self):
        # strip newlines
        statement_stripped_comments = Database.strip_comments(self.statement)

        return statement_stripped_comments.replace("\n", " ")

    def view_name(self) -> str:
        return self.parsed_variable("view_name")

    def view_full_name(self) -> str:
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.view_name()
        )

    def name(self) -> str:
        return self.view_full_name()

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
        return f"DROP VIEW IF EXISTS {self.view_full_name()};"

    def __str__(self) -> str:
        result = "CREATE "

        if self.is_temp():
            result += "TEMP "

        result += "VIEW "

        if self.if_not_exists():
            result += "IF NOT EXISTS "

        result += self.view_full_name()

        if self.remaining():
            result += " " + str(self.remaining())

        return f"{result};"
