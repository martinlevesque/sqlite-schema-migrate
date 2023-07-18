import re
from schema.parsed_schema import ParsedSchema
from schema.pragma_schema import PragmaSchema
from schema.index_schema import IndexSchema

# read an input sql schema content and provide a hash representing the schema

STATEMENT_TYPES = {
    "PRAGMA": {"name": "pragma", "class": PragmaSchema},
    "CREATE INDEX": {"name": "index", "class": IndexSchema},
    "CREATE UNIQUE INDEX": {"name": "index", "class": IndexSchema},
}


def parse(str_content):
    result = ParsedSchema(pragmas={}, tables={}, indexes={})

    pattern = re.compile(
        r"(?i)((CREATE TABLE|ALTER TABLE|CREATE INDEX|CREATE UNIQUE INDEX|PRAGMA).*?;)\s*(--[^\n]*)?\n",
        re.DOTALL | re.MULTILINE,
    )

    for match in pattern.finditer(f"{str_content}\n"):
        statement = match.group(1)
        base_instruction = match.group(2).upper()

        statement_setup = STATEMENT_TYPES.get(base_instruction, None)

        if statement_setup is None:
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

    return result
