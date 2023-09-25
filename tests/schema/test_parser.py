from schema import parser


def test_parser_create_trigger():
  content = """
  CREATE TRIGGER categories_on_insert AFTER INSERT ON categories
   BEGIN
    UPDATE categories SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
   END;

  """

  result = parser.parse(content)

  assert "categories_on_insert" in result.triggers

