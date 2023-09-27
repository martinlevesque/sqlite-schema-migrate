from __future__ import annotations

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

    REGEX = rf"CREATE\s+TABLE\s+(({StatementSchema.REGEX_TERM_NAME})\.)?({StatementSchema.REGEX_TERM_NAME})\s*(.+);"
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

        return str(self.parse().group(6)).strip()

    def table_full_name(self):
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.table_name()
        )

    def specs_following_table(self):
        return self.parse().group(10)

    def name(self):
        return self.table_full_name()

    @staticmethod
    def apply_changes(
        current_schema: TableSchema,
        previous_schema: TableSchema,
        database: Database,
        force: bool = False,
    ):
        state_result = ""
        print(f"in apply change table.. ")

        if previous_schema is None:
            # does not exist, create it
            print(f"about to create ...")
            database.execute(str(current_schema), log_function=log.info)
            print(f"done create ...")
        elif current_schema is None and previous_schema:
            # it was removed:
            database.execute(previous_schema.destroy_cmd(), log_function=log.info)
            state_result = "remove"
        else:
            # is there a diff between the two?
            if str(current_schema) == str(previous_schema):
                return

            log.debug(
                f"Table {current_schema.name()} already exists and has changes..."
            )

            if force:
                # ensure foreign keys are off
                database.execute(f"PRAGMA foreign_keys = OFF;")

                # database.execute("BEGIN TRANSACTION;", log_function=log.info)

                origin_table_name = f"{current_schema.table_name()}_old"

                replace_statement = f"ALTER TABLE {current_schema.name()} RENAME TO {origin_table_name};"
                replace_statement = TableSchema.clean_statement(replace_statement)
                database.execute(
                    replace_statement,
                    log_function=log.info,
                )

                # create new table with the new schema
                database.execute(str(current_schema), log_function=log.info)

                to_table_name = f"{current_schema.table_name()}"

                origin_columns = database.get_table_column_names(
                    TableSchema.clean_statement(origin_table_name)
                )
                destination_columns = database.get_table_column_names(
                    TableSchema.clean_statement(to_table_name)
                )

                columns_to_copy = list(set(origin_columns) & set(destination_columns))
                columns_to_copy_s = ", ".join(columns_to_copy)

                database.execute(
                    TableSchema.clean_statement(
                        f"INSERT INTO {current_schema.name()} ({columns_to_copy_s}) SELECT {columns_to_copy_s} FROM {current_schema.name()}_old;",
                    ),
                    log_function=log.info,
                )
                database.execute(
                    TableSchema.clean_statement(
                        f"DROP TABLE {current_schema.name()}_old;"
                    ),
                    log_function=log.info,
                )
                # database.execute("COMMIT;", log_function=log.info)
            else:
                log.debug(f"skipping changes in table {current_schema.name()}")

        return state_result

    @staticmethod
    def clean_statement(current_statement):
        return current_statement.replace("[", "").replace("]", "")

    def destroy_cmd(self):
        return f"DROP TABLE IF EXISTS {self.table_full_name()};"

    def __str__(self):
        return f"CREATE TABLE {self.table_full_name()} {self.specs_following_table()};"
