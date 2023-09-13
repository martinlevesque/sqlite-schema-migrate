import re

from schema.data_mutation_schema import DataMutationSchema
from schema.parsed_schema import ParsedSchema
from schema.pragma_schema import PragmaSchema
from schema.index_schema import IndexSchema
from schema.drop_entity_schema import DropEntitySchema
from schema.table_schema import TableSchema
from schema.alter_table_schema import AlterTableSchema

# read an input sql schema content and provide a hash representing the schema

STATEMENT_TYPES = {
    "PRAGMA": {"name": "pragma", "class": PragmaSchema},
    "CREATE INDEX": {"name": "index", "class": IndexSchema},
    "CREATE UNIQUE INDEX": {"name": "index", "class": IndexSchema},
    "DROP INDEX": {"name": "index", "class": DropEntitySchema},
    "CREATE TABLE": {"name": "table", "class": TableSchema},
    "ALTER TABLE": {"name": "table", "class": AlterTableSchema},
    "INSERT": {"name": "insert", "class": DataMutationSchema},
    "WITH": {"name": "insert", "class": DataMutationSchema},
    "REPLACE": {"name": "insert", "class": DataMutationSchema},
    "UPDATE": {"name": "update", "class": DataMutationSchema},
    "DELETE FROM": {"name": "update", "class": DataMutationSchema},
}


def parse(str_content) -> ParsedSchema:
    result = ParsedSchema(
        pragmas={},
        tables={},
        alter_tables={},
        data_mutations={},
        indexes={},
        drop_entities={},
        all=[],
    )

    pattern = re.compile(
        r"""(?i)((CREATE TABLE|ALTER TABLE|CREATE INDEX|CREATE UNIQUE INDEX|DROP INDEX|PRAGMA|WITH|INSERT|REPLACE|UPDATE|DELETE FROM).*?;)\s*(--[^\n]*)?\n""",
        re.DOTALL | re.MULTILINE,
    )

    for match in pattern.finditer(f"{str_content}\n"):
        statement = match.group(1)
        base_instruction = match.group(2).upper()

        statement_setup = STATEMENT_TYPES.get(base_instruction, None)

        if statement_setup is None:
            print(f"unknown statement type!!!")
            # raise Exception(f"Unknown statement type: {base_instruction}")
            continue
        else:
            schema_item = statement_setup["class"](
                statement=statement, base_instruction=base_instruction
            )
            if schema_item.TYPE == "pragma":
                result.pragmas[schema_item.name()] = schema_item
            elif schema_item.TYPE == "create_index":
                result.indexes[schema_item.name()] = schema_item
            elif schema_item.TYPE == "drop_entity":
                result.drop_entities[schema_item.name()] = schema_item
            elif schema_item.TYPE == "create_table":
                result.tables[schema_item.name()] = schema_item
            elif schema_item.TYPE == "alter_table":
                result.alter_tables[schema_item.name()] = schema_item
            elif schema_item.TYPE == "data_mutation":
                result.data_mutations[schema_item.name()] = schema_item
            else:
                raise Exception(f"Unknown schema item type: {schema_item.TYPE}")

            # append to all as an ordered list
            result.all.append(schema_item)

    return result
