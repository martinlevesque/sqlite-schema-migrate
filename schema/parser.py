import re

from schema.data_mutation_schema import DataMutationSchema
from schema.parsed_schema import ParsedSchema
from schema.pragma_schema import PragmaSchema
from schema.index_schema import IndexSchema
from schema.drop_entity_schema import DropEntitySchema
from schema.table_schema import TableSchema
from schema.alter_table_schema import AlterTableSchema
from schema.view_schema import ViewSchema
from schema.trigger_schema import TriggerSchema

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
    "CREATE VIEW": {"name": "update", "class": ViewSchema},
    "CREATE TEMP VIEW": {"name": "update", "class": ViewSchema},
    "CREATE TEMPORARY VIEW": {"name": "update", "class": ViewSchema},
    "CREATE TRIGGER": {"name": "update", "class": TriggerSchema},
    "CREATE TEMP TRIGGER": {"name": "update", "class": TriggerSchema},
    "CREATE TEMPORARY TRIGGER": {"name": "update", "class": TriggerSchema},
}


def parse(str_content: str) -> ParsedSchema:
    result = ParsedSchema(
        pragmas={},
        tables={},
        alter_tables={},
        data_mutations={},
        indexes={},
        drop_entities={},
        views={},
        triggers={},
        all=[],
    )

    stripped_str_content = ""

    if str_content:
        stripped_str_content = strip_single_line_comments(
            strip_multiline_comments(str_content)
        )

    pattern = re.compile(
        r"""(((CREATE TABLE|ALTER TABLE|CREATE INDEX|CREATE UNIQUE INDEX|CREATE VIEW|"""
        r"""CREATE TEMP VIEW|CREATE TEMPORARY VIEW|DROP INDEX|PRAGMA|WITH|INSERT|REPLACE|"""
        r"""UPDATE|DELETE FROM)|((CREATE TRIGGER|CREATE TEMP TRIGGER|CREATE TEMPORARY TRIGGER).+?\s+BEGIN.+?\s+END\s*)).*?;)\s*(--[^\n]*)?\n""",
        re.DOTALL | re.IGNORECASE | re.MULTILINE,
    )

    for match in pattern.finditer(f"{stripped_str_content}\n"):
        statement = match.group(1)
        base_instruction = (match.group(5) or match.group(2)).upper()

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
            elif schema_item.TYPE == "create_view":
                result.views[schema_item.name()] = schema_item
            elif schema_item.TYPE == "create_trigger":
                result.triggers[schema_item.name()] = schema_item
            elif schema_item.TYPE == "data_mutation":
                result.data_mutations[schema_item.name()] = schema_item
            else:
                raise Exception(f"Unknown schema item type: {schema_item.TYPE}")

            # append to all as an ordered list
            result.all.append(schema_item)

    return result


# multiline comments in sql are anything between
# /* and */
# also make sure that it takes into account quotes
# if /* is within "/*" it should be skipped
# same thing with single quotes ('/*')
def strip_multiline_comments(s):
    result = ""
    in_quotes = False
    quote_char = None
    i = 0

    while i < len(s):
        # If we encounter a quote character and we are not inside quotes
        if s[i] in ['"', "'"] and not in_quotes:
            in_quotes = True
            quote_char = s[i]
            result += s[i]
        # If we encounter the same quote character and we are inside quotes
        elif s[i] == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
            result += s[i]
        # If we encounter /* and we are not inside quotes
        elif s[i : i + 2] == "/*" and not in_quotes:
            # Skip to the end of the comment
            while i < len(s) and s[i : i + 2] != "*/":
                i += 1
            i += 2
            continue
        # In all other cases, just add the character to the result
        else:
            result += s[i]
        i += 1

    return result


def strip_single_line_comments(s):
    result = ""
    in_quotes = False
    quote_char = None
    i = 0

    while i < len(s):
        # If we encounter a quote character and we are not inside quotes
        if s[i] in ['"', "'"] and not in_quotes:
            in_quotes = True
            quote_char = s[i]
            result += s[i]
        # If we encounter the same quote character and we are inside quotes
        elif s[i] == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
            result += s[i]
        # If we encounter -- and we are not inside quotes
        elif s[i : i + 2] == "--" and not in_quotes:
            # Skip to the end of the line
            while i < len(s) and s[i] != "\n":
                i += 1
            continue
        # In all other cases, just add the character to the result
        else:
            result += s[i]
        i += 1

    return result
