CREATE TABLE short_names (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    status INTEGER
);

INSERT INTO short_names (name, status)
SELECT
    'nazvanie' || i AS name,
    (RANDOM() * 2)::INT AS status
FROM generate_series(1, 700000) AS s(i);

CREATE TABLE full_names (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    status INTEGER DEFAULT NULL,
    base_name VARCHAR(255)
);

CREATE INDEX idx_base_name ON full_names (base_name);

INSERT INTO full_names (name)
SELECT
    'nazvanie' || i || ext.extension AS name
FROM generate_series(1, 500000) AS s(i),
LATERAL (VALUES ('.mp3'), ('.wav'), ('.flac'), ('.aac')) AS ext(extension)
ORDER BY RANDOM()
LIMIT 500000;

UPDATE full_names
SET base_name = LEFT(name, LENGTH(name) - POSITION('.' IN REVERSE(name)));

DELETE FROM full_names
WHERE id NOT IN (
    SELECT MIN(id)
    FROM full_names
    GROUP BY base_name
);

UPDATE full_names AS f_n
SET status = s_n.status
FROM short_names AS s_n
WHERE f_n.base_name = s_n.name;
