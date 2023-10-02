import hashlib
from dataclasses import dataclass
from schema.statement_schema import StatementSchema
from lib import log
from sqlite_db import Database


# doc:
# https://www.sqlite.org/lang_altertable.html

# example:
# ALTER TABLE [schema_name.]index_name ...;


@dataclass
class AlterTableSchema(StatementSchema):
    statement: str
    base_instruction: str

    REGEX = r"ALTER\s+TABLE\s+(\w+\.)?(?P<table_name>\w+)\s+.+;"
    TYPE = "alter_table"

    def id(self) -> str:
        return self.statement_hash_id()

    def schema_name(self) -> str:
        return self.schema_name_at(1)

    def table_name(self) -> str:
        return str(self.parsed_variable("table_name"))

    def table_full_name(self) -> str:
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.table_name()
        )

    def name(self) -> str:
        return self.table_full_name()

    @staticmethod
    def apply_changes(
        current_schema: StatementSchema | None,
        previous_schema: StatementSchema | None,
        database: Database,
        force: bool = False,
    ) -> str:
        state_result = ""

        if previous_schema is None and current_schema:
            # it has not been run yet:
            database.execute(str(current_schema), log_function=log.info)
        elif current_schema is None and previous_schema:
            state_result = "remove"
        else:
            if current_schema:
                log.debug(f'alter table "{current_schema}" already exists... skipping')

        return state_result

    def __str__(self) -> str:
        return self.prepared_input_statement()
