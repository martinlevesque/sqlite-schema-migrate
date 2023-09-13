from dataclasses import dataclass
from typing import List

from schema.statement_schema import StatementSchema


@dataclass
class ParsedSchema:
    pragmas: dict
    tables: dict
    alter_tables: dict
    data_mutations: dict
    indexes: dict
    drop_entities: dict
    all: List[StatementSchema]

    def __str__(self) -> str:
        result = ""

        for entity in self.all:
            result += f"{entity}\n"

        return result
