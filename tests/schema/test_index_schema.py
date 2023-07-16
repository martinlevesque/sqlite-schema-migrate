from schema.index_schema import IndexSchema


def test_index_schema_index_name_happy_path():
    index = IndexSchema(
        statement="CREATE INDEX index_name ON table_name (column_name);",
        base_instruction="CREATE INDEX",
    )

    assert index.index_name() == "index_name"


def test_index_schema_schema_name_present():
    index = IndexSchema(
        statement="CREATE INDEX my_schema.index_name ON table_name (column_name);",
        base_instruction="CREATE INDEX",
    )

    assert index.schema_name() == "my_schema"


def test_index_schema_index_full_name_without_schema():
    index = IndexSchema(
        statement="CREATE INDEX index_name ON table_name (column_name);",
        base_instruction="CREATE INDEX",
    )

    assert index.index_full_name() == "index_name"


def test_index_schema_index_full_name_with_schema():
    index = IndexSchema(
        statement="CREATE INDEX hello.index_name ON table_name (column_name);",
        base_instruction="CREATE INDEX",
    )

    assert index.index_full_name() == "hello.index_name"


def test_index_schema_is_unique_happy_path():
    index = IndexSchema(
        statement="CREATE UNIQUE INDEX index_name ON table_name (column_name);",
        base_instruction="CREATE INDEX",
    )

    assert index.is_unique() is True


def test_index_schema_table_name_happy_path():
    index = IndexSchema(
        statement="CREATE INDEX index_name ON table_name (column_name);",
        base_instruction="CREATE INDEX",
    )

    assert index.table_name() == "table_name"


def test_index_schema_columns_happy_path():
    index = IndexSchema(
        statement="CREATE INDEX index_name ON table_name (column_name1, column_name2, );",
        base_instruction="CREATE INDEX",
    )

    assert index.columns() == ["column_name1", "column_name2"]


def test_index_schema_with_where_clause():
    index = IndexSchema(
        statement="""CREATE INDEX index_name ON table_name (column_name1)
                        WHERE col1 = 'test' and col2 = 'test2';""",
        base_instruction="CREATE INDEX",
    )

    assert index.where_clause() == "col1 = 'test' and col2 = 'test2'"


def test_index_schema_str():
    index = IndexSchema(
        statement="""CREATE INDEX schema.index_name ON table_name (column_name1)
                        WHERE col1 = 'test' and col2 = 'test2';""",
        base_instruction="CREATE INDEX",
    )

    assert (
        str(index)
        == "CREATE INDEX schema.index_name ON table_name (column_name1) WHERE col1 = 'test' and col2 = 'test2';"
    )
