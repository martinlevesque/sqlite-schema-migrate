import hashlib
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
        return hashlib.sha256(str(self).encode("utf-8")).hexdigest()

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
        else:
            log.debug(f'alter table "{current_schema}" already exists... skipping')

    def __str__(self):
        return self.prepared_input_statement()
