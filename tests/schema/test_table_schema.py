from schema.table_schema import TableSchema


def test_create_table_table_name_happy_path():
    schema = TableSchema(
        statement="CREATE TABLE hello ...;",
        base_instruction="CREATE TABLE",
    )

    assert schema.table_name() == "hello"


def test_create_table_table_name_with_override():
    schema = TableSchema(
        statement="CREATE TABLE hello ...;",
        base_instruction="CREATE TABLE",
        override_table_name="world",
    )

    assert schema.table_name() == "world"


def test_create_table_str_happy_path():
    schema = TableSchema(
        statement="CREATE TABLE hello ...;",
        base_instruction="CREATE TABLE",
    )

    assert str(schema) == "CREATE TABLE hello ...;"


def test_create_table_str_with_override():
    schema = TableSchema(
        statement="CREATE TABLE hello ...;",
        base_instruction="CREATE TABLE",
        override_table_name="world",
    )

    assert str(schema) == "CREATE TABLE world ...;"
