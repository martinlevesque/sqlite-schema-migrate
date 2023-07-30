from schema.drop_entity_schema import DropEntitySchema


def test_drop_entity_schema_entity_name_happy_path():
    index = DropEntitySchema(
        statement="DROP INDEX IF EXISTS schema_name.index_name;",
        base_instruction="DROP INDEX",
    )

    assert index.entity_name() == "index_name"


def test_drop_entity_schema_entity_full_name_happy_path():
    index = DropEntitySchema(
        statement="DROP INDEX IF EXISTS schema_name.index_name;",
        base_instruction="DROP INDEX",
    )

    assert index.entity_full_name() == "schema_name.index_name"


def test_drop_entity_schema_entity_type_happy_path():
    index = DropEntitySchema(
        statement="DROP INDEX IF EXISTS schema_name.index_name;",
        base_instruction="DROP INDEX",
    )

    assert index.entity_type() == "INDEX"


def test_drop_entity_schema_str_happy_path():
    schema = DropEntitySchema(
        statement="DROP INDEX IF EXISTS schema_name.index_name;",
        base_instruction="DROP INDEX",
    )

    assert str(schema) == "DROP INDEX IF EXISTS schema_name.index_name;"
