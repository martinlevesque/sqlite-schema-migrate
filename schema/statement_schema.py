import re
from dataclasses import dataclass


@dataclass
class StatementSchema():
    statement: str
    base_instruction: str

    def parse(self):
        match = re.search(self.__class__.REGEX, self.statement)

        if not match:
            raise Exception(f"Invalid statement: {self.statement}")

        return match
