SET sql_safe_updates = FALSE;
USE defaultdb;
DROP DATABASE IF EXISTS todos CASCADE;


CREATE DATABASE todos;
USE todos;
CREATE TABLE todos (
    todo_id INT8 NOT NULL DEFAULT unique_rowid(),
    title VARCHAR(60) NULL,
    text VARCHAR NULL,
    done BOOL NULL,
    pub_date TIMESTAMP NULL,
    CONSTRAINT "primary" PRIMARY KEY (todo_id ASC),
    FAMILY "primary" (todo_id, title, text, done, pub_date)
  );


CREATE USER IF NOT EXISTS example;
GRANT ALL ON DATABASE todos TO example;