from dataclasses import dataclass
from typing import Optional
from schema.statement_schema import StatementSchema
from lib import log


# example:
# INSERT INTO schema_name.table_name (col1, col2) VALUES (val1, val2);


@dataclass
class DataMutationSchema(StatementSchema):
    statement: str
    base_instruction: str

    REGEX = r"(WITH\s+(RECURSIVE)?.*)?(INSERT\s+(OR\s+(ABORT|FAIL|IGNORE|REPLACE|ROLLBACK))?INTO).+;"
    # REGEX = r"DROP\s+(TABLE|INDEX)?\s*(IF EXISTS)?\s*(\w+\.)?(\w+);"
    TYPE = "data_mutation"

    def id(self):
        return self.statement_hash_id()

    def name(self):
        return self.id()

    @staticmethod
    def apply_changes(
        current_schema=None, previous_schema=None, database=None, force=False
    ):
        state_result = ""

        if current_schema:
            # it is new:
            database.execute(str(current_schema), log_function=log.info)
        elif current_schema is None and previous_schema:
            state_result = "remove"

        return state_result

    def __str__(self):
        return self.statement
