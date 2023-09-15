from schema.view_schema import ViewSchema


def test_create_view_str_happy_path():
    schema = ViewSchema(
        statement="CREATE TEMP VIEW hello.world ...;",
        base_instruction="CREATE VIEW",
    )

    assert str(schema) == "CREATE TEMP VIEW hello.world ...;"
