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
            # is there a diff between the two?
            if str(current_schema) == str(previous_schema):
                return

            log.debug(f"Table {current_schema.name()} already exists and has changes...")

            if force:
                log.debug("will force...")
                # todo foreign key pragma

                # pragma table_info(tablename);

                database.execute("BEGIN TRANSACTION;", log_function=log.info)
                database.execute(
                    f"ALTER TABLE {current_schema.name()} RENAME TO {current_schema.name()}_old;",
                    log_function=log.info,
                )
                database.execute(str(current_schema), log_function=log.info)
                database.execute(
                    f"INSERT INTO {current_schema.name()} SELECT * FROM {current_schema.name()}_old;",
                    log_function=log.info,
                )
                database.execute(
                    f"DROP TABLE {current_schema.name()}_old;", log_function=log.info
                )
                database.execute("COMMIT;", log_function=log.info)
            else:
                log.debug(f"skipping changes in table {current_schema.name()}")

    def __str__(self):
        return f"CREATE TABLE {self.table_full_name()} {self.specs_following_table()};"
