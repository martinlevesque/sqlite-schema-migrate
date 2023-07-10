import re
from schema.pragma_schema import PragmaSchema
from schema.parsed_schema import ParsedSchema

# read an input sql schema content and provide a hash representing the schema

STATEMENT_TYPES = {
    "PRAGMA": {
        "name": "pragma",
        "class": PragmaSchema
    }
}


def parse(str_content):
    result = ParsedSchema(
        pragmas={},
        tables={},
        indexes={}
    )

    pattern = re.compile(r'(?i)((CREATE TABLE|ALTER TABLE|PRAGMA).*?;)\s*(--[^\n]*)?\n', re.DOTALL | re.MULTILINE)

    for match in pattern.finditer(f"{str_content}\n"):
        statement = match.group(1)
        base_instruction = match.group(2).upper()

        statement_setup = STATEMENT_TYPES.get(base_instruction, None)

        if statement_setup is None:
            # raise Exception(f"Unknown statement type: {base_instruction}")
            continue
        else:
            schema_item = statement_setup['class'](statement=statement, base_instruction=base_instruction)

            if schema_item.TYPE == 'pragma':
                result.pragmas[schema_item.variable_name()] = schema_item

    return result
