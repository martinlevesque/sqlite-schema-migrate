import hashlib
import re
from dataclasses import dataclass


@dataclass
class StatementSchema:
    statement: str
    base_instruction: str

    REGEX_TERM_NAME = "(\\w|\\s|\\[|\\])+"

    def id(self):
        return self.name()

    def statement_hash_id(self):
        return hashlib.sha256(str(self).encode("utf-8")).hexdigest()

    def __eq__(self, other):
        return self.id() == other.id()

    def __ne__(self, other):
        return not self.__eq__(other)

    def name(self):
        raise Exception("Not implemented")

    def schema_name_at(self, expected_index):
        schema_txt = self.parse().group(expected_index)

        if not schema_txt:
            return ""

        # if ends with a dot, remove it
        if schema_txt and schema_txt.endswith("."):
            schema_txt = schema_txt[:-1]

        return str(schema_txt).strip()

    @staticmethod
    def schema_entity_full_name(schema_name, entity_name):
        if schema_name:
            return f"{schema_name}.{entity_name}"

        return entity_name

    """
    prepare the input statement for parsing
    """

    def prepared_input_statement(self):
        return self.statement

    def parse(self):
        match = re.search(
            self.__class__.REGEX, self.prepared_input_statement(), re.IGNORECASE
        )

        if not match:
            raise Exception(f"Invalid statement: {self.statement}")

        return match
