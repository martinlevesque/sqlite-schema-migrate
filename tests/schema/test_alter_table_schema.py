from schema.alter_table_schema import AlterTableSchema


def test_alter_table_schema_name_happy_path():
    schema = AlterTableSchema(
        statement="ALTER TABLE schema_name.table ...;",
        base_instruction="ALTER TABLE",
    )

    assert schema.schema_name() == "schema_name"


def test_alter_table_schema_name_when_no_schema():
    schema = AlterTableSchema(
        statement="ALTER TABLE table ...;",
        base_instruction="ALTER TABLE",
    )

    assert schema.schema_name() == ""


def test_alter_table_table_name_happy_path():
    schema = AlterTableSchema(
        statement="ALTER TABLE schema_name.table ...;",
        base_instruction="ALTER TABLE",
    )

    assert schema.table_name() == "table"


def test_alter_table_table_name_when_no_schema():
    schema = AlterTableSchema(
        statement="ALTER TABLE table ...;",
        base_instruction="ALTER TABLE",
    )

    assert schema.table_name() == "table"


def test_alter_table_table_full_name_happy_path():
    schema = AlterTableSchema(
        statement="ALTER TABLE schema_name.table ...;",
        base_instruction="ALTER TABLE",
    )

    assert schema.table_full_name() == "schema_name.table"


def test_alter_table_table_id_happy_path():
    schema = AlterTableSchema(
        statement="ALTER TABLE schema_name.table ...;",
        base_instruction="ALTER TABLE",
    )

    assert (
        schema.id()
        == "737d0e49c588504f0f6c7ecf959af3fa0f88f5aff78a10b267dc50d59ef32aac"
    )
