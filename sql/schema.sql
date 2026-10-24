PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS offering;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS discipline;

CREATE TABLE discipline (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    credits INTEGER NOT NULL
);

CREATE TABLE offering (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discipline_id INTEGER NOT NULL,
    teacher TEXT NOT NULL,
    total_seats INTEGER NOT NULL,
    taken_seats INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (discipline_id) REFERENCES discipline(id) ON DELETE CASCADE
);

CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL UNIQUE,
    max_credits INTEGER NOT NULL DEFAULT 30
);

CREATE TABLE enrollment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    offering_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
    FOREIGN KEY (offering_id) REFERENCES offering(id) ON DELETE CASCADE,
    UNIQUE(student_id, offering_id)
);