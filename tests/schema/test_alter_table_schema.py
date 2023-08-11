from schema.alter_table_schema import AlterTableSchema


def test_alter_table_schema_name_happy_path():
    index = AlterTableSchema(
        statement="ALTER TABLE schema_name.table ...;",
        base_instruction="ALTER TABLE",
    )

    assert index.schema_name() == "schema_name"


def test_alter_table_schema_name_when_no_schema():
    index = AlterTableSchema(
        statement="ALTER TABLE table ...;",
        base_instruction="ALTER TABLE",
    )

    assert index.schema_name() == ""


def test_alter_table_table_name_happy_path():
    index = AlterTableSchema(
        statement="ALTER TABLE schema_name.table ...;",
        base_instruction="ALTER TABLE",
    )

    assert index.table_name() == "table"


def test_alter_table_table_name_when_no_schema():
    index = AlterTableSchema(
        statement="ALTER TABLE table ...;",
        base_instruction="ALTER TABLE",
    )

    assert index.table_name() == "table"


def test_alter_table_table_full_name_happy_path():
    index = AlterTableSchema(
        statement="ALTER TABLE schema_name.table ...;",
        base_instruction="ALTER TABLE",
    )

    assert index.table_full_name() == "schema_name.table"
