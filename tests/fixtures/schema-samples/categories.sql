PRAGMA foreign_keys = ON;
PRAGMA synchronous = OFF;
PRAGMA journal_mode = MEMORY;
PRAGMA temp_store = MEMORY;
PRAGMA cache_size = 500000;

CREATE TABLE categories (
	id INTEGER NOT NULL,
	name VARCHAR(200) NOT NULL,
	parent_category_id INTEGER NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(parent_category_id) REFERENCES categories(id),
	UNIQUE (name)
);

ALTER TABLE categories ADD COLUMN description VARCHAR(200) DEFAULT '';

CREATE INDEX myindex_test ON categories (name);
DROP INDEX myindex_test;
