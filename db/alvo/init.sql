CREATE TABLE signal (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    signal_id INT REFERENCES signal(id),
    value FLOAT NOT NULL
);
