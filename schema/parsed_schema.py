from dataclasses import dataclass


@dataclass
class ParsedSchema:
    pragmas: dict
    tables: dict
    alter_tables: dict
    data_mutations: dict
    indexes: dict
    drop_entities: dict
    all: list

    def __str__(self):
        result = ""

        for entity in self.all:
            result += f"{entity}\n"

        return result
