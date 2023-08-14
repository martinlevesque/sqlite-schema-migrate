from dataclasses import dataclass
from schema.statement_schema import StatementSchema
from sqlite_db import Database
from lib import log


# doc:
# https://www.sqlite.org/lang_createtable.html

# format
# CREATE TABLE schema_name.table_name ;


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
        statement_stripped_comments = Database.strip_comments(self.statement)

        return statement_stripped_comments.replace("\n", " ")

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
                # ensure foreign keys are off
                database.execute(f"PRAGMA foreign_keys = OFF;")

                database.execute("BEGIN TRANSACTION;", log_function=log.info)

                origin_table_name = f"{current_schema.table_name()}_old"

                database.execute(
                    f"ALTER TABLE {current_schema.name()} RENAME TO {origin_table_name};",
                    log_function=log.info,
                )

                # create new table with the new schema
                database.execute(str(current_schema), log_function=log.info)

                to_table_name = f"{current_schema.table_name()}"

                origin_columns = database.get_table_column_names(origin_table_name)
                destination_columns = database.get_table_column_names(to_table_name)

                columns_to_copy = list(set(origin_columns) & set(destination_columns))
                columns_to_copy_s = ", ".join(columns_to_copy)

                database.execute(
                    f"INSERT INTO {current_schema.name()} ({columns_to_copy_s}) SELECT {columns_to_copy_s} FROM {current_schema.name()}_old;",
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
