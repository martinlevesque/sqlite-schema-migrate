from dataclasses import dataclass


@dataclass
class ParsedSchema:
    pragmas: dict
    tables: dict
    indexes: dict

    def __str__(self):
        result = ""

        for entity in list(self.pragmas.values()) + list(self.indexes.values()):
            result += f"{entity}\n"

        return result
