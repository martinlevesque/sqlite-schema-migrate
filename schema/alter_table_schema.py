import re
from dataclasses import dataclass
from schema.statement_schema import StatementSchema
from lib import log


# doc:
# https://www.sqlite.org/lang_altertable.html

# example:
# ALTER TABLE [schema_name.]index_name ...;


@dataclass
class AlterTableSchema(StatementSchema):
    statement: str
    base_instruction: str

    REGEX = r"ALTER\s+TABLE\s+(\w+\.)?(\w+)\s+.+;"
    TYPE = "alter_table"

    def id(self):
        return f"toto"

    def schema_name(self):
        return self.schema_name_at(1)

    def table_name(self):
        return self.parse().group(2)

    def table_full_name(self):
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.table_name()
        )

    def name(self):
        return self.table_full_name()

    @staticmethod
    def apply_changes(current_schema=None, previous_schema=None, database=None):
        if previous_schema is None and current_schema:
            # it has not been run yet:
            database.execute(str(current_schema), log_function=log.info)

    def destroy_cmd(self):
        return f"DROP INDEX {self.index_full_name()};"

    def __str__(self):
        result = "CREATE "

        if self.is_unique():
            result += "UNIQUE "

        result += "INDEX "

        result += self.index_full_name()

        result += f" ON {self.table_name()} ({', '.join(self.columns())})"

        if self.where_clause():
            result += f" WHERE {self.where_clause()}"

        return f"{result};"
