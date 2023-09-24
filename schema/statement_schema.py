from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Match

from sqlite_db import Database


@dataclass
class StatementSchema:
    statement: str
    base_instruction: str

    REGEX_TERM_NAME = "(\\w|\\s|\\[|\\])+"
    REGEX = ""

    def id(self) -> str:
        return self.name()

    def statement_hash_id(self) -> str:
        return hashlib.sha256(str(self).encode("utf-8")).hexdigest()

    def __eq__(self, other: StatementSchema) -> bool:
        return self.id() == other.id()

    def __ne__(self, other: StatementSchema) -> bool:
        return not self.__eq__(other)

    def name(self) -> str:
        raise Exception("Not implemented")

    @staticmethod
    def apply_changes(
        current_schema: StatementSchema | None,
        previous_schema: StatementSchema | None,
        database: Database,
        force: bool = False,
    ):
        pass

    def schema_name_at(self, expected_index: int) -> str:
        schema_txt = self.parse().group(expected_index)

        if not schema_txt:
            return ""

        # if ends with a dot, remove it
        if schema_txt and schema_txt.endswith("."):
            schema_txt = schema_txt[:-1]

        return str(schema_txt).strip()

    def destroy_cmd(self) -> str:
        return ""

    @staticmethod
    def schema_entity_full_name(schema_name: str, entity_name: str) -> str:
        if schema_name:
            return f"{schema_name}.{entity_name}"

        return entity_name

    """
    prepare the input statement for parsing
    """

    def prepared_input_statement(self) -> str:
        return self.statement

    def parse(self) -> Match[str]:
        match = re.search(
            self.__class__.REGEX, self.prepared_input_statement(), re.IGNORECASE
        )

        if not match:
            raise Exception(f"Invalid statement: {self.statement}")

        return match
