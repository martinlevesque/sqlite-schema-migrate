from sqlite_db import Database


def test_sqlite_db_strip_comments_in_line_happy_path():
    input_str = "CREATE TABLE hello -- this is a comment"
    assert Database.strip_comments_in_line(input_str) == "CREATE TABLE hello "


def test_sqlite_db_strip_comments_in_line_when_no_comment():
    input_str = "CREATE TABLE hello -"
    assert Database.strip_comments_in_line(input_str) == "CREATE TABLE hello -"


def test_sqlite_db_strip_comments_happy_path():
    input_str = "CREATE TABLE hello -- this is a comment\nCREATE TABLE world -- this is another comment"
    result = Database.strip_comments(input_str)
    print(f"result = -{result}-")
    assert (
        Database.strip_comments(input_str) == "CREATE TABLE hello \nCREATE TABLE world "
    )
