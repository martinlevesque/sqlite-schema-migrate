from dataclasses import dataclass


@dataclass
class ParsedSchema:
    pragmas: dict
    tables: dict
    indexes: dict

    def __str__(self):
        result = ""

        db_entities = list(self.pragmas.values()) + list(self.tables.values()) + list(self.indexes.values())

        for entity in db_entities:
            result += f"{entity}\n"

        return result
