from schema.pragma_schema import PragmaSchema


def test_pragma_schema_variable_name_happy_path():
    pragma = PragmaSchema(statement="PRAGMA journal_mode = MEMORY;", base_instruction="PRAGMA")

    assert pragma.variable_name() == "journal_mode"


def test_pragma_schema_case_insensitive():
    pragma = PragmaSchema(statement="pragma journal_mode = MEMORY;", base_instruction="PRAGMA")

    assert pragma.variable_name() == "journal_mode"


def test_pragma_schema_variable_should_be_downcased():
    pragma = PragmaSchema(statement="PRAGMA journal_MODE = MEMORY;", base_instruction="PRAGMA")

    assert pragma.variable_name() == "journal_mode"


def test_pragma_schema_value_happy_path():
    pragma = PragmaSchema(statement="PRAGMA journal_mode = MEMORY;", base_instruction="PRAGMA")

    assert pragma.value() == "MEMORY"


def test_pragma_schema_value_with_override():
    pragma = PragmaSchema(statement="PRAGMA journal_mode = MEMORY;", base_instruction="PRAGMA")
    pragma.override_value = "WAL"

    assert pragma.value() == "WAL"
