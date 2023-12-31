from schema.data_mutation_schema import DataMutationSchema


def test_data_mutation_parse_simple_insert_happy_path():
    schema = DataMutationSchema(
        statement="INSERT INTO table(v1, v2) VALUES (v1, v2);",
        base_instruction="INSERT INTO",
    )

    assert schema.parse()


def test_data_mutation_parse_simple_update_happy_path():
    schema = DataMutationSchema(
        statement="UPDATE categories SET name = 'category-test-4' WHERE id = 3;",
        base_instruction="UPDATE",
    )

    assert schema.parse()


def test_data_mutation_parse_simple_delete_happy_path():
    schema = DataMutationSchema(
        statement="DELETE FROM categories WHERE id = 4;",
        base_instruction="DELETE FROM",
    )

    assert schema.parse()


def test_data_mutation_str_happy_path():
    schema = DataMutationSchema(
        statement="INSERT INTO table(v1, v2) VALUES (v1, v2);",
        base_instruction="INSERT INTO",
    )

    assert str(schema) == "INSERT INTO table(v1, v2) VALUES (v1, v2);"


def test_data_mutation_id_happy_path():
    schema = DataMutationSchema(
        statement="INSERT INTO table(v1, v2) VALUES (v1, v2);",
        base_instruction="INSERT INTO",
    )

    assert (
        schema.id()
        == "2dffe7fe8b64a699d2797e53ca589815e70e8817c85fb07199185df28e53419b"
    )
