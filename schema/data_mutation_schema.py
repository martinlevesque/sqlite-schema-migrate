from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema
from lib import log
from sqlite_db import Database


# example:
# INSERT INTO schema_name.table_name (col1, col2) VALUES (val1, val2);


@dataclass
class DataMutationSchema(StatementSchema):
    statement: str
    base_instruction: str

    REGEX_OR = "(OR\\s+(ABORT|FAIL|IGNORE|REPLACE|ROLLBACK))?"
    REGEX_INSERT_CASE = f"INSERT\\s+{REGEX_OR}INTO"
    REGEX_UPDATE_CASE = f"UPDATE\\s+{REGEX_OR}\\s*\\w+\\s+SET\\s*\\w+"
    REGEX_DELETE_CASE = f"DELETE\\s+FROM\\s*\\w+\\s+WHERE\\s*\\.*"
    REGEX = rf"(WITH\s+(RECURSIVE)?.*)?({REGEX_INSERT_CASE})|({REGEX_UPDATE_CASE})|({REGEX_DELETE_CASE}).+;"
    TYPE = "data_mutation"

    def id(self) -> str:
        return self.statement_hash_id()

    def name(self) -> str:
        return self.id()

    @staticmethod
    def apply_changes(
        current_schema: StatementSchema | None,
        previous_schema: StatementSchema | None,
        database: Database,
        force: bool = False,
    ) -> str:
        state_result = ""

        if previous_schema is None and current_schema:
            # has not been run yet
            database.execute(str(current_schema), log_function=log.info)
        elif current_schema is None and previous_schema:
            state_result = "remove"

        return state_result

    def __str__(self) -> str:
        return self.statement
