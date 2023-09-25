from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema
from lib import log
from sqlite_db import Database


@dataclass
class TriggerSchema(StatementSchema):
    statement: str
    base_instruction: str
    override_value: Optional[str] = None

    REGEX = rf"CREATE\s+(TEMP|TEMPORARY)?\s*TRIGGER\s+(IF NOT EXISTS)?\s*({StatementSchema.REGEX_TERM_NAME}\.)?({StatementSchema.REGEX_TERM_NAME})\s*(.+);"
    TYPE = "create_trigger"

    def id(self) -> str:
        return f"trigger-{self.name()}"

    def prepared_input_statement(self):
        # strip newlines
        statement_stripped_comments = Database.strip_comments(self.statement)

        return statement_stripped_comments.replace("\n", " ")

    def if_not_exists(self) -> str | None:
        return self.parse().group(2)

    def schema_name(self) -> str:
        return self.schema_name_at(5)

    def trigger_name(self) -> str:
        return self.parse().group(6)

    def remaining_statement(self) -> str | None:
        return self.parse().group(9)

    def name(self) -> str:
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.trigger_name()
        )

    def table_name(self) -> str:
        return self.parse().group(5)

    def is_temp(self) -> bool:
        return str(self.parse().group(1)).upper() in ["TEMP", "TEMPORARY"]

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
        return f"DROP TRIGGER IF EXISTS {self.name()};"

    def __str__(self) -> str:
        result = "CREATE "

        if self.is_temp():
            result += "TEMP "

        result += "TRIGGER "

        if self.if_not_exists():
            result += "IF NOT EXISTS "

        result += self.name()

        if self.remaining_statement():
            result += " " + str(self.remaining_statement())

        return f"{result};"
