PRAGMA foreign_keys = ON;
PRAGMA synchronous = OFF;
PRAGMA journal_mode = MEMORY;
PRAGMA temp_store = MEMORY;
PRAGMA cache_size = 500000;
PRAGMA default_cache_size = 500000;

CREATE TABLE categories (
	id INTEGER NOT NULL,
	name VARCHAR(200) NOT NULL default(';'),
	parent_category_id INTEGER NULL,
	last_update TIMESTAMP NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(parent_category_id) REFERENCES categories(id),
	UNIQUE (name)
);

CREATE TRIGGER categories_on_insert AFTER INSERT ON categories
 BEGIN
  UPDATE categories SET last_update = DATETIME('NOW')  WHERE rowid = new.rowid;
 END;

INSERT INTO categories (id, name) VALUES (1, 'category-test-1');
INSERT INTO categories (id, name) VALUES (2, 'category-test-2');
INSERT INTO categories (id, name) VALUES (3, 'category-test-3');
INSERT INTO categories (id, name) VALUES (4, 'category-test-5');
UPDATE categories SET name = 'category-test-4' WHERE id = 3;
DELETE FROM categories WHERE id = 4;

ALTER TABLE categories ADD COLUMN description VARCHAR(200) DEFAULT '';

DROP INDEX IF EXISTS myindex_test;
CREATE INDEX myindex_test ON categories (name);



