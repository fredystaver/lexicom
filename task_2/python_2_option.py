import psycopg2
import time


def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS short_names (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        status INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS full_names (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        status INTEGER DEFAULT NULL
    );
    """)


def insert_data_into_short_names(cursor):
    cursor.execute("""
    INSERT INTO short_names (name, status)
    SELECT
        'nazvanie' || i AS name,
        (RANDOM() * 2)::INT AS status
    FROM generate_series(1, 700000) AS s(i)
    ON CONFLICT (name) DO NOTHING;
    """)


def insert_data_into_full_names(cursor):
    cursor.execute("""
    INSERT INTO full_names (name)
    SELECT
        'nazvanie' || i || ext.extension AS name
    FROM generate_series(1, 500000) AS s(i),
    LATERAL (VALUES ('.mp3'), ('.wav'), ('.flac'), ('.aac')) AS ext(extension)
    ON CONFLICT (name) DO NOTHING;
    """)


def update_status_in_full_names(cursor):
    cursor.execute("""
    UPDATE full_names AS f_n
    SET status = s_n.status
    FROM short_names AS s_n
    WHERE LEFT(f_n.name, LENGTH(f_n.name) - LENGTH(SUBSTRING(f_n.name FROM '\\.[^\\.]+$'))) = s_n.name;
    """)


def main():
    with psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="postgres",
    ) as connection:
        with connection.cursor() as cursor:
            start_time = time.time()

            create_tables(cursor)
            connection.commit()

            insert_data_into_short_names(cursor)
            connection.commit()

            insert_data_into_full_names(cursor)
            connection.commit()

            update_status_in_full_names(cursor)
            connection.commit()

            end_time = time.time()
            print(f"Время выполнения: {end_time - start_time} секунд.")


if __name__ == "__main__":
    main()
