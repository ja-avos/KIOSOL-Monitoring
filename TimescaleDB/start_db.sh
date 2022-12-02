# For Windows
docker run --name timescaledb -dit -p 5432:5432 -v "//$PWD/data:/var/postgres/pgdata/data" -e POSTGRES_PASSWORD=IOT2022! -e POSTGRES_USER=labmonitoring -e POSTGRES_DB=solarlabmonitoring timescale/timescaledb:latest-pg14

# For Linux
docker run --name timescaledb -dit -p 5432:5432 -v $(pwd)/data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=IOT2022! -e POSTGRES_USER=labmonitoring -e POSTGRES_DB=solarlabmonitoring timescale/timescaledb:latest-pg14