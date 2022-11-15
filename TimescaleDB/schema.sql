CREATE DATABASE solarlabmonitoring;

\ c solarlabmonitoring 

CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE unit (
    id SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL,
    unit TEXT NOT NULL,
    UNIQUE("name", unit)
);

CREATE TABLE string_mapping (
    id SERIAL PRIMARY KEY,
    measurement_id VARCHAR(50) NOT NULL REFERENCES measurement(id),
    "value" FLOAT NOT NULL,
    string TEXT NOT NULL,
    UNIQUE(measurement_id, "value")
);

CREATE TABLE measurement (
    id VARCHAR(50) PRIMARY KEY,
    "name" TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    has_string_values BOOLEAN DEFAULT FALSE,
    UNIQUE("name")
);

CREATE TABLE laboratory (
    id VARCHAR(50) PRIMARY KEY,
    "name" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    UNIQUE("name")
    UNIQUE(latitude, longitude)
);

CREATE TABLE device (
    id VARCHAR(50) PRIMARY KEY,
    lab_id VARCHAR(50) NOT NULL REFERENCES laboratory(id),
    "name" TEXT NOT NULL,
    port TEXT NOT NULL,
);

CREATE TABLE "value" {
    time TIMESTAMPTZ,
    lab_id VARCHAR(50) NOT NULL REFERENCES laboratory(id),
    device_id VARCHAR(50) NOT NULL REFERENCES device(id),
    measurement_id VARCHAR(50) NOT NULL REFERENCES measurement(id),
    value FLOAT
}

CREATE TABLE temp_value (
    time TIMESTAMPTZ,
    lab_id VARCHAR(50) NOT NULL REFERENCES laboratory(id),
    device_id VARCHAR(50) NOT NULL REFERENCES device(id),
    measurement_id VARCHAR(50) NOT NULL REFERENCES measurement(id),
    value FLOAT
);

CREATE TYPE "role" AS ENUM ('ADMIN', 'EDITOR', 'VIEWER');

CREATE TABLE user (
    "login" TEXT PRIMARY KEY,
    "role" "role" NOT NULL,
    email TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    
    UNIQUE(email)
);

SELECT create_hypertable('value', 'time');

-- Continuous Aggregates Example
CREATE VIEW measurements_15min WITH (timescaledb.continuous) AS
SELECT time_bucket('15 minute', time) as bucket,
    parameter_id,
    avg(value) as avg,
    max(value) as max,
    min(value) as min
FROM measurements
GROUP BY bucket,
    parameter_id;
CREATE VIEW measurements_hourly WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) as bucket,
    parameter_id,
    avg(value) as avg,
    max(value) as max,
    min(value) as min
FROM measurements
GROUP BY bucket,
    parameter_id;
CREATE VIEW measurements_daily WITH (timescaledb.continuous) AS
SELECT time_bucket('1 day', time) as bucket,
    parameter_id,
    avg(value) as avg,
    max(value) as max,
    min(value) as min
FROM measurements
GROUP BY bucket,
    parameter_id;