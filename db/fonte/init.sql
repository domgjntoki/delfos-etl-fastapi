CREATE TABLE data (
    timestamp TIMESTAMP PRIMARY KEY,
    wind_speed FLOAT NOT NULL,
    power FLOAT NOT NULL,
    ambient_temperature FLOAT NOT NULL
);

INSERT INTO data (timestamp, wind_speed, power, ambient_temperature)
SELECT
    generate_series(
        NOW() - INTERVAL '10 days',
        NOW(),
        '1 minute'::INTERVAL
    ) AS timestamp,
    random() * 30 AS wind_speed,
    random() * 100 AS power,
    random() * 40 + 10 AS ambient_temperature;
