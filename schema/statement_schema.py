import re
from dataclasses import dataclass


@dataclass
class StatementSchema:
    statement: str
    base_instruction: str

    def name(self):
        raise Exception("Not implemented")

    def prepared_input_statement(self):
        return self.statement

    def parse(self):
        match = re.search(
            self.__class__.REGEX, self.prepared_input_statement(), re.IGNORECASE
        )

        if not match:
            raise Exception(f"Invalid statement: {self.statement}")

        return match
