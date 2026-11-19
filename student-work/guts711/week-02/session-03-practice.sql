-- psql (SQL SHELL) promt:
-- CREATE DATABASE campus_practice;
--\connect campus_practice;
-- SELECT current_database();


-- EXERCISE 1: 
-- A) Create the tables
CREATE TABLE events
(
    id integer PRIMARY KEY,
    title text NOT NULL,
    event_on date NOT NULL,
);

CREATE TABLE students
(
    id integer PRIMARY KEY,
    name text NOT NULL,
);

CREATE TABLE registrations
(
    id integer PRIMARY KEY,
    event_id integer NOT NULL REFERENCES events (id),
    student_id integer NOT NULL REFERENCES students (id),
    registered_on date NOT NULL,
    cancelled_on date,
);

-- B) Insert the starter rows
INSERT INTO events (id, title)
VALUES
    (1, 'Robotics Demo', DATE '2026-11-26'),
    (2, 'AI Study Jam', DATE '2026-11-27')
;

INSERT INTO students (id, name)
VALUES
    (11, "Jin")
;

INSERT INTO registrations (id, event_id, student_id, registration_date, cancelled_date)
VALUES
    (101, 1, 11, DATE '2026-11-19', NULL)
;

SELECT *
FROM events;

SELECT *
FROM students;

SELECT *
FROM registrations;


-- EXERCISE 2 - Find records
SELECT (id, title)
FROM events
ORDER BY title;

SELECT (id, event_id, student_id, registration_date)
FROM registrations
WHERE cancelled_on is NULL;

SELECT (id, name)
FROM students
WHERE id = (
    SELECT (id, event_id, student_id, registration_date)
    FROM registrations
    WHERE cancelled_on is NULL;
);

-- EXERCISE 3 - Update, delete, and check a constraint
-- Part A:
SELECT *
FROM registrations
WHERE id = 101;

UPDATE registrations
SET cancelled_on = DATE '2026-11-20'
WHERE id = 101;

SELECT *
FROM registrations
WHERE id = 101;

-- PART B:
-- INSERT INTO registrations 
-- VALUES
--     (199, 99, 11, DATE '2026-11-22');

--ERROR:  insert or update on table "registrations" violates foreign key constraint "registrations_event_id_fkey"
--DETAIL:  Key (event_id)=(99) is not present in table "events".

SELECT *
FROM registrations
WHERE id = 199;

--PART C:
INSERT INTO registrations
VALUES
    (102, 2, 11, DATE '2026-11-22');

SELECT *
FROM registrations
WHERE id = 102;

DELETE FROM registrations
WHERE ID = 102;

SELECT *
FROM registrations
WHERE id = 102;

SELECT *
FROM registrations;
