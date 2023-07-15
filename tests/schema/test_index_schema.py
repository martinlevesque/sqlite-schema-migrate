from schema.index_schema import IndexSchema


def test_index_schema_variable_name_happy_path():
    index = IndexSchema(statement="CREATE INDEX index_name ON table_name (column_name);",
                        base_instruction="CREATE INDEX")

    assert index.index_name() == "index_name"


def test_index_schema_is_unique_happy_path():
    index = IndexSchema(statement="CREATE UNIQUE INDEX index_name ON table_name (column_name);",
                        base_instruction="CREATE INDEX")

    assert index.is_unique() is True


def test_index_schema_table_name_happy_path():
    index = IndexSchema(statement="CREATE INDEX index_name ON table_name (column_name);",
                        base_instruction="CREATE INDEX")

    assert index.table_name() == "table_name"


def test_index_schema_columns_happy_path():
    index = IndexSchema(statement="CREATE INDEX index_name ON table_name (column_name1, column_name2, );",
                        base_instruction="CREATE INDEX")

    assert index.columns() == ["column_name1", "column_name2"]
