# 1 Вариант (SQL)

CREATE TABLE short_names ( id SERIAL PRIMARY KEY, name VARCHAR(255) UNIQUE, status INTEGER );

INSERT INTO short_names (name, status) SELECT "nazvanie" || i AS name, (RANDOM() * 2)::INT AS status FROM
generate_series(1, 700000) AS s(i);

CREATE TABLE full_names ( id SERIAL PRIMARY KEY, name VARCHAR(255) UNIQUE, status INTEGER DEFAULT NULL, base_name
VARCHAR(255) );

CREATE INDEX idx_base_name ON full_names (base_name);

INSERT INTO full_names (name) SELECT "nazvanie" || i || ext.extension AS name FROM generate_series(1, 500000) AS s(i),
LATERAL (VALUES (".mp3"), (".wav"), (".flac"), (".aac")) AS ext(extension) ORDER BY RANDOM() LIMIT 500000;

UPDATE full_names SET base_name = LEFT(name, LENGTH(name) - POSITION("." IN REVERSE(name)));

DELETE FROM full_names WHERE id NOT IN ( SELECT MIN(id) FROM full_names GROUP BY base_name );

UPDATE full_names AS f_n SET status = s_n.status FROM short_names AS s_n WHERE f_n.base_name = s_n.name;

# 2 Вариант (Python)

```
import time
import psycopg2

def execute_with_pause(cursor, query, limit=50000) -> None:
    offset = 0 while True: batch_query = query.format(offset=offset, limit=limit)
    cursor.execute(batch_query)
    if cursor.rowcount < limit:
        break
    time.sleep(1)
    offset += limit

def main(
    query1, query2, query3, query4, query5, query6, query7, query8, query9
    ) -> None:
    with psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="postgres",
        ) as connection:
        with  connection.cursor() as cursor:
            cursor.execute(query=query1)
            cursor.execute(query=query2)
            cursor.execute(query=query3)
            cursor.execute(query=query4)
            cursor.execute(query=query5)
            cursor.execute(query=query6)
            cursor.execute(query=query7)
            cursor.execute(query=query8)

        execute_with_pause(cursor, query9)

    connection.commit()

create_short_names_table = """
CREATE TABLE IF NOT EXISTS short_names (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    status INTEGER
);
"""

insert_short_names = """
INSERT INTO short_names (name, status)
    SELECT "nazvanie" || i AS name,
    (RANDOM() * 2)::INT AS
    status FROM generate_series(1, 700000) AS s(i);
"""

create_full_names_table = """
CREATE TABLE IF NOT EXISTS full_names (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    status INTEGER DEFAULT NULL,
    base_name VARCHAR(255)); 
"""

set_index = """
CREATE INDEX IF NOT EXISTS idx_base_name ON full_names (base_name);
"""

insert_full_names = """
INSERT INTO full_names (name)
    SELECT "nazvanie" || i || ext.extension AS name
    FROM
        generate_series(1, 500000) AS s(i),
        LATERAL (VALUES (".mp3"), (".wav"), (".flac"), (".aac")) AS ext(extension)
        ORDER BY RANDOM() LIMIT 500000;
        """

insert_in_base_name = """
UPDATE full_names
    SET base_name = LEFT(name, LENGTH(name) - POSITION("." IN REVERSE(name)));
"""

delete_dublicates = """
DELETE FROM full_names
    WHERE id NOT IN ( SELECT MIN(id)
    FROM full_names
    GROUP BY base_name );
"""

update_statuses = """
UPDATE full_names f_n
    SET status = tmp.status
    FROM tmp_updates tmp
        WHERE f_n.id = tmp.id;
"""

create_temp_table = """
CREATE TEMP TABLE tmp_updates AS
    SELECT
    f_n.id, s_n.status
    FROM full_names f_n JOIN short_names s_n ON f_n.base_name = s_n.name;
 """

main(
    create_short_names_table,
    insert_short_names,
    create_full_names_table,
    set_index,
    insert_full_names,
    insert_in_base_name,
    delete_dublicates,
    create_temp_table,
    update_statuses,
)
```
