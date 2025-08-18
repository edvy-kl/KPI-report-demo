#!/bin/bash
set -euo pipefail

# Load .env and export everything (handles spaces/quotes safely)
set -a
source .env
set +a

# Helper: expand env vars in the YAML, then query with yq
cfg() {
  envsubst < database/db_setup.yaml | yq -r "$1"
}

# Pull values from the substituted YAML
DB_NAME=$(cfg '.database.name')
DB_PORT=$(cfg '.database.port')
RW_USERNAME=$(cfg '.database.users.rw_username')
RW_PASSWORD=$(cfg '.database.users.rw_password')
RO_USERNAME=$(cfg '.database.users.ro_username')
RO_PASSWORD=$(cfg '.database.users.ro_password')
PG_PASSWORD=$(cfg '.database.users.pg_password')


DB_SCHEMA=$(cfg '.database.schema.name')
TABLE_NAME=$(cfg '.database.schema.table.name')

# Validate
for var in DB_NAME DB_PORT RW_USERNAME RW_PASSWORD RO_USERNAME RO_PASSWORD PG_PASSWORD; do
  if [ -z "${!var:-}" ]; then
    echo "Error: $var is empty after env substitution. Check .env and db_setup.yaml."
    exit 1
  fi
done

# Generate CREATE TABLE statement from YAML
TABLE_SQL=$(yq -r '[.database.schema.table.columns[] |
  "    \"" + .name + "\" " + .type +
  (if has("primary_key") and .primary_key then " PRIMARY KEY" else "" end) +
  (if has("not_null") and .not_null then " NOT NULL" else "" end) +
  (if has("default") then
    if .default == true then " DEFAULT true"
    elif .default == false then " DEFAULT false"
    elif .default == "now" then " DEFAULT CURRENT_TIMESTAMP"
    else " DEFAULT " + (.default | tostring)
    end
  else "" end) +
  (if has("check") then " CHECK (" + .check + ")" else "" end)] | join(",\n")' database/db_setup.yaml)


# Check if container exists and is running
CONTAINER_NAME="postgres-dashforge"

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    docker rm -f $CONTAINER_NAME
fi

# Create network and volume for postgres service
docker network create dashforge || true
docker volume create dashforge_pg_data || true

docker run --name $CONTAINER_NAME \
    --network dashforge \
    -e POSTGRES_PASSWORD=$PG_PASSWORD \
    -v dashforge_pg_data:/var/lib/postgresql/data \
    -v "$(pwd)/database/postgresql.conf:/etc/postgresql/postgresql.conf" \
    -p $DB_PORT:$DB_PORT \
    -d postgres:latest \
    -c "config_file=/etc/postgresql/postgresql.conf"

until docker exec $CONTAINER_NAME pg_isready -U postgres -p $DB_PORT; do
echo "Waiting for Postgres..."
sleep 2
done

# Execute database commands and store the exit status
if docker exec -i $CONTAINER_NAME psql -U postgres -p $DB_PORT -v ON_ERROR_STOP=1 -q << EOF
SELECT 'CREATE DATABASE $DB_NAME'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

\c $DB_NAME

CREATE SCHEMA IF NOT EXISTS "$DB_SCHEMA";

-- Create table if it doesn't exist
CREATE TABLE IF NOT EXISTS "$DB_SCHEMA"."$TABLE_NAME" (
$TABLE_SQL
);

-- Create users if they don't exist and update passwords
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$RW_USERNAME') THEN
        CREATE USER $RW_USERNAME WITH PASSWORD '$RW_PASSWORD';
    ELSE
        ALTER USER $RW_USERNAME WITH PASSWORD '$RW_PASSWORD';
    END IF;

    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$RO_USERNAME') THEN
        CREATE USER $RO_USERNAME WITH PASSWORD '$RO_PASSWORD';
    ELSE
        ALTER USER $RO_USERNAME WITH PASSWORD '$RO_PASSWORD';
    END IF;
END
\$\$;

-- Grant permissions
GRANT USAGE ON SCHEMA "$DB_SCHEMA" TO $RW_USERNAME;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "$DB_SCHEMA" TO $RW_USERNAME;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA "$DB_SCHEMA" TO $RW_USERNAME;
ALTER DEFAULT PRIVILEGES IN SCHEMA "$DB_SCHEMA" GRANT ALL ON TABLES TO $RW_USERNAME;
ALTER DEFAULT PRIVILEGES IN SCHEMA "$DB_SCHEMA" GRANT ALL ON SEQUENCES TO $RW_USERNAME;

GRANT USAGE ON SCHEMA "$DB_SCHEMA" TO $RO_USERNAME;
GRANT SELECT ON ALL TABLES IN SCHEMA "$DB_SCHEMA" TO $RO_USERNAME;
ALTER DEFAULT PRIVILEGES IN SCHEMA "$DB_SCHEMA" GRANT SELECT ON TABLES TO $RO_USERNAME;

EOF
then
    echo "Database setup completed successfully!"
else
    echo "Error: Database setup failed!"
    exit 1
fi