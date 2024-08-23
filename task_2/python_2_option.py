# import time
# import psycopg2
#
#
# def main(query1, query2, query3, query4, query5, query6, ):
#     start = time.time()
#     with psycopg2.connect(
#         host="localhost",
#         port="5432",
#         database="postgres",
#         user="postgres",
#         password="postgres",
#     ) as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(query=query1)
#             cursor.execute(query=query2)
#             cursor.execute(query=query3)
#             cursor.execute(query=query4)
#             cursor.execute(query=query5)
#             cursor.execute(query=query6)
#
#         connection.commit()
#         finish = time.time()
#         print(finish - start)
#
#
# create_full_names_table = """
# CREATE TABLE full_names (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255) UNIQUE,
#     status INTEGER DEFAULT NULL
# );
# """
# create_short_names_table = """
# CREATE TABLE short_names (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255),
#     status INTEGER
# )
# """
# insert_in_full_names = """
# INSERT INTO full_names (name)
# SELECT
#     'nazvanie' || i || ext.extension AS name
# FROM generate_series(1, 500000) AS s(i),
#     LATERAL (VALUES ('.mp3'), ('.wav'), ('.flac'), ('.aac')) AS ext(extension)
#     ORDER BY RANDOM()
#     LIMIT 500000
# """
# insert_in_short_names = """
# INSERT INTO short_names (name, status)
# SELECT
#     'nazvanie' || i AS name,
#     (RANDOM() * 2)::INT AS status
# FROM generate_series(1, 700000) AS s(i)
# """
# create_temp_table_query = """
# CREATE TEMPORARY TABLE temp_short_names AS
#     SELECT name AS base_name, status
#     FROM short_names
# """
#
# update_status_query = """
# UPDATE full_names f
#     SET status = t.status
#     FROM (
#         SELECT LEFT(base_name, LENGTH(base_name) - POSITION('.' IN REVERSE(base_name))) AS base_name, status
#         FROM temp_short_names
#     ) t
#     WHERE LEFT(f.name, LENGTH(f.name) - POSITION('.' IN REVERSE(f.name))) = t.base_name
# """
#
# main(
#     create_full_names_table, create_short_names_table, insert_in_short_names, insert_in_full_names,
#     create_temp_table_query, update_status_query
# )
import time

import psycopg2


def execute_with_pause(cursor, query, limit=50000) -> None:
    offset = 0
    while True:
        batch_query = query.format(offset=offset, limit=limit)
        cursor.execute(batch_query)
        if cursor.rowcount < limit:
            break
        time.sleep(1)
        offset += limit


def main(query1, query2, query3, query4, query5, query6, query7, query8, query9) -> None:
    start = time.time()
    with psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="postgres",
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query=query1)
            print(1)
            cursor.execute(query=query2)
            print(12)
            cursor.execute(query=query3)
            print(13)
            cursor.execute(query=query4)
            print(14)
            cursor.execute(query=query5)
            print(15)
            cursor.execute(query=query6)
            print(16)
            cursor.execute(query=query7)
            print(17)
            cursor.execute(query=query8)
            print(18)

            execute_with_pause(cursor, query9)

        connection.commit()
        finish = time.time()
        print(finish - start)


create_short_names_table = '''
CREATE TABLE IF NOT EXISTS short_names (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    status INTEGER
);
'''

insert_short_names = '''
INSERT INTO short_names (name, status)
SELECT
    'nazvanie' || i AS name,
    (RANDOM() * 2)::INT AS status
FROM generate_series(1, 700000) AS s(i);
'''

create_full_names_table = '''
CREATE TABLE IF NOT EXISTS full_names (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    status INTEGER DEFAULT NULL,
    base_name VARCHAR(255)
);
'''

set_index = '''
CREATE INDEX IF NOT EXISTS idx_base_name ON full_names (base_name);
'''

insert_full_names = '''
INSERT INTO full_names (name)
SELECT
    'nazvanie' || i || ext.extension AS name
FROM generate_series(1, 500000) AS s(i),
LATERAL (VALUES ('.mp3'), ('.wav'), ('.flac'), ('.aac')) AS ext(extension)
ORDER BY RANDOM()
LIMIT 500000;
'''

insert_in_base_name = '''
UPDATE full_names
SET base_name = LEFT(name, LENGTH(name) - POSITION('.' IN REVERSE(name)));
'''

delete_dublicates = '''
DELETE FROM full_names
WHERE id NOT IN (
    SELECT MIN(id)
    FROM full_names
    GROUP BY base_name
);
'''

update_statuses = '''
    UPDATE full_names f_n
    SET status = tmp.status
    FROM tmp_updates tmp
    WHERE f_n.id = tmp.id;
'''

create_temp_table = """
CREATE TEMP TABLE tmp_updates AS
SELECT f_n.id, s_n.status
FROM full_names f_n
JOIN short_names s_n
ON f_n.base_name = s_n.name;
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
