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


def test_create_table_name_with_special_characters():
    schema = TableSchema(
        statement="CREATE TABLE [what].[Categories]( [CategoryID] INTEGER PRIMARY KEY AUTOINCREMENT, [CategoryName] TEXT, [Description] TEXT, [Picture] BLOB);",
        base_instruction="CREATE TABLE",
    )

    assert schema.schema_name() == "[what]"
    assert schema.table_name() == "[Categories]"
    assert schema.name() == "[what].[Categories]"


def test_create_table_str_happy_path():
    schema = TableSchema(
        statement="CREATE TABLE hello.world ...;",
        base_instruction="CREATE TABLE",
    )

    assert str(schema) == "CREATE TABLE hello.world ...;"


def test_create_table_str_with_override():
    schema = TableSchema(
        statement="CREATE TABLE hello ...;",
        base_instruction="CREATE TABLE",
        override_table_name="world",
    )

    assert str(schema) == "CREATE TABLE world ...;"


def test_create_table_str_with_special_characters():
    schema = TableSchema(
        statement="CREATE TABLE [Categories]( [CategoryID] INTEGER PRIMARY KEY AUTOINCREMENT, [CategoryName] TEXT, [Description] TEXT, [Picture] BLOB);",
        base_instruction="CREATE TABLE",
    )

    assert (
        str(schema)
        == "CREATE TABLE [Categories] ( [CategoryID] INTEGER PRIMARY KEY AUTOINCREMENT, [CategoryName] TEXT, [Description] TEXT, [Picture] BLOB);"
    )


# prepared_input_statement


def test_create_table_prepared_input_statement_happy_path():
    schema = TableSchema(
        statement="CREATE TABLE hello \ntest, -- what\ntest2, -- what2\n...;",
        base_instruction="CREATE TABLE",
    )

    assert (
        schema.prepared_input_statement() == "CREATE TABLE hello  test,  test2,  ...;"
    )
