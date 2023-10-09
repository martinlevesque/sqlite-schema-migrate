from schema import parser


def test_parser_happy_path():
    content = """
  
CREATE TABLE categories (
    id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL default(';'),
    parent_category_id INTEGER NULL,
    last_update TIMESTAMP NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(parent_category_id) REFERENCES categories(id),
    UNIQUE (name)
);


  """

    result = parser.parse(content)

    assert len(result.tables) == 1
    assert (
        str(result.tables["categories"])
        == "CREATE TABLE categories (     id INTEGER NOT NULL,     name VARCHAR(200) NOT NULL default(';'),     parent_category_id INTEGER NULL,     last_update TIMESTAMP NULL,     PRIMARY KEY (id),     FOREIGN KEY(parent_category_id) REFERENCES categories(id),     UNIQUE (name) );"
    )


def test_parser_create_trigger():
    content = """
  CREATE TRIGGER categories_on_insert AFTER INSERT ON categories
   BEGIN
    UPDATE categories SET last_updatend = DATETIME('NOW')  WHERE rowid = new.rowid;
   END;

  """

    result = parser.parse(content)

    assert "categories_on_insert" in result.triggers

    expected_statement = (
        "CREATE TRIGGER categories_on_insert AFTER INSERT ON "
        "categories    BEGIN     UPDATE categories SET last_updatend = DATETIME('NOW')"
        "  WHERE rowid = new.rowid;    END;"
    )

    result_statement = str(result.triggers["categories_on_insert"])

    assert result_statement == expected_statement


def test_parser_strip_single_line_comments_happy_path():
    content = 'CREATE TRIGGER categories_on_insert AFTER INSERT "dd--dd" ON categories -- hello'
    result = parser.strip_single_line_comments(content)

    assert (
        result
        == 'CREATE TRIGGER categories_on_insert AFTER INSERT "dd--dd" ON categories '
    )


def test_parser_strip_single_line_comments_with_many_quotes():
    content = 'CREATE TRIGGER categories_on_insert AFTER INSERT "-- --" "dd--dd" ON categories -- hello'
    result = parser.strip_single_line_comments(content)

    assert (
        result
        == 'CREATE TRIGGER categories_on_insert AFTER INSERT "-- --" "dd--dd" ON categories '
    )


def test_parser_strip_single_line_comments_with_many_lines():
    content = """CREATE TRIGGER categories_on_insert AFTER INSERT \"dd--dd\" ON categories -- hello\"
CREATE TRIGGER testline2 AFTER INSERT \"dd--dd\" ON categories -- helloworld"
    """
    result = parser.strip_single_line_comments(content)

    expected_result = """CREATE TRIGGER categories_on_insert AFTER INSERT \"dd--dd\" ON categories 
CREATE TRIGGER testline2 AFTER INSERT \"dd--dd\" ON categories 
    """

    assert result == expected_result


def test_parser_strip_multiline_comments_happy_path():
    content = ' /* CREATE TRIGGER categories_on_insert AFTER INSERT "ddd" ON categories -- hello */ '
    result = parser.strip_multiline_comments(content)

    assert result == "  "


def test_parser_strip_multiline_comments_skip_in_quotes():
    content = "CREATE TRIGGER categories_on_insert AFTER INSERT \"/*ddd*/\" '/**/' ON categories/*toto*/"
    result = parser.strip_multiline_comments(content)

    assert (
        result
        == "CREATE TRIGGER categories_on_insert AFTER INSERT \"/*ddd*/\" '/**/' ON categories"
    )
