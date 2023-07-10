from dataclasses import dataclass


@dataclass
class ParsedSchema:
    pragmas: dict
    tables: dict
    indexes: dict

    def __str__(self):
        result = ""

        for pragma in self.pragmas.values():
            result += f"{pragma}\n"

        return result
