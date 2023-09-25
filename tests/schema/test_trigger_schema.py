from schema.trigger_schema import TriggerSchema


def test_create_trigger_str_with_temp():
    schema = TriggerSchema(
        statement="CREATE TEMP TRIGGER hello.world ...;",
        base_instruction="CREATE TRIGGER",
    )

    assert str(schema) == "CREATE TEMP TRIGGER hello.world ...;"


def test_create_trigger_str_happy_path():
    schema = TriggerSchema(
        statement="CREATE TRIGGER hello.world ...;",
        base_instruction="CREATE TRIGGER",
    )

    assert str(schema) == "CREATE TRIGGER hello.world ...;"


def test_create_trigger_name():
    schema = TriggerSchema(
        statement="CREATE TRIGGER hello.world AFTER INSERT test;",
        base_instruction="CREATE TRIGGER",
    )

    assert schema.name() == "hello.world"
