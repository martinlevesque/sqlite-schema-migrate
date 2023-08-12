import re
from dataclasses import dataclass
from schema.statement_schema import StatementSchema
from lib import log


# doc:
# https://www.sqlite.org/lang_createtable.html

# format
# CREATE TABLE schema_name.table_name ;

# todo to support diff create table
# - option full table copy
# - if not option full table copy, then:
#   - support column diff


@dataclass
class TableSchema(StatementSchema):
    statement: str
    base_instruction: str
    override_table_name: str = ""

    REGEX = r"CREATE\s+TABLE\s+(\w+\.)?(\w+)\s+(.+);"
    TYPE = "create_table"

    def id(self):
        return f"table-{self.name()}"

    def prepared_input_statement(self):
        # strip newlines
        return self.statement.replace("\n", " ")

    def schema_name(self):
        return self.schema_name_at(1)

    def table_name(self):
        if self.override_table_name:
            return self.override_table_name

        return self.parse().group(2)

    def table_full_name(self):
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.table_name()
        )

    def specs_following_table(self):
        return self.parse().group(3)

    def name(self):
        return self.table_full_name()

    @staticmethod
    def apply_changes(
        current_schema=None, previous_schema=None, database=None, force=False
    ):
        if previous_schema is None:
            # does not exist, create it
            database.execute(str(current_schema), log_function=log.info)
        else:
            log.debug(f"table {current_schema.name()} already exists...")

            if force:
                log.debug(f"should FORCEEEEEEEEEEEEEE")

    def __str__(self):
        return f"CREATE TABLE {self.table_full_name()} {self.specs_following_table()};"
