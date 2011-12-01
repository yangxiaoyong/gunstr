CREATE TABLE IF NOT EXISTS entries (
    id INTEGER NOT NULL PRIMARY KEY,
    author_id INTEGER NOT NULL,
    slug NOT NULL,
    title NOT NULL,
    markdown TEXT,
    html TEXT,
    published INTEGER,
    updated INTEGER
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users (id, email, name, password) VALUES (
    1, 'yan5yang@gmail.com', 'yxy', 'xxxxxxxxx'
);
