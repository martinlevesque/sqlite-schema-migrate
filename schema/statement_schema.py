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

    REGEX_IF_NOT_EXISTS = r"(?P<if_not_exists>IF NOT EXISTS)"
    REGEX_TERM_NAME = "(\\[(\\w|\\s)+\\])|(\\w+)"
    REGEX_SCHEMA_NAME = rf"(?P<schema_name>({REGEX_TERM_NAME})\.)"
    REGEX_TABLE_NAME = rf"(?P<table_name>({REGEX_TERM_NAME}))"
    REGEX = ""
    TYPE = ""

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

    def schema_name_at(self, expected_index: int | str) -> str:
        schema_test = ""

        if isinstance(expected_index, int):
            schema_txt = self.parse().group(expected_index)
        elif isinstance(expected_index, str):
            schema_txt = self.parsed_variable(expected_index)

        if not schema_txt:
            return ""

        # if ends with a dot, remove it
        if schema_txt and schema_txt.endswith("."):
            schema_txt = schema_txt[:-1]

        return str(schema_txt).strip()

    def table_full_name(self) -> str:
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.table_name()
        )

    def entity_full_name(self) -> str:
        return StatementSchema.schema_entity_full_name(
            self.schema_name(), self.entity_name()
        )

    def schema_name(self) -> str:
        return self.schema_name_at("schema_name")

    def entity_name(self) -> str:
        return self.parsed_variable("entity_name")

    def table_name(self) -> str:
        return self.parsed_variable("table_name")

    def if_not_exists(self) -> str:
        return self.parsed_variable("if_not_exists")

    def remaining(self) -> str:
        return self.parsed_variable("remaining")

    def temp(self) -> str:
        return self.parsed_variable("temp")

    def is_temp(self) -> bool:
        return str(self.temp()).upper() in ["TEMP", "TEMPORARY"]

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

    def parsed_variable(self, variable: str) -> str:
        match = self.parse()

        groupdict = match.groupdict()

        if not groupdict:
            raise Exception(f"Invalid statement: {self.statement}")

        result = groupdict.get(variable)

        if not result:
            return ""

        return result
