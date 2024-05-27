DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS days;

create table events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_day TEXT,
    time TEXT NOT NULL,
    tz TEXT NOT NULL DEFAULT 'УРАЛ',
    lead TEXT NOT NULL,
    theme TEXT NOT NULL,
    actors TEXT,
    enable INTEGER NOT NULL
);
create table days (
    id INTEGER PRIMARY KEY,
    day TEXT NOT NULL
);
create table leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)