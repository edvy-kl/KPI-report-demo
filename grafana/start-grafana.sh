#!/bin/bash
set -euo pipefail

# Load .env and export everything (handles spaces/quotes safely)
set -a
source .env
set +a

# Helper to validate environment variables
check_env() {
    local var_name="$1"
    if [ -z "${!var_name:-}" ]; then
        echo "Error: $var_name environment variable is not set"
        exit 1
    fi
}

# Validate required environment variables
required_vars=("GRAFANA_ADMIN_USER" "GRAFANA_ADMIN_PASSWORD")
for var in "${required_vars[@]}"; do
    check_env "$var"
done

# Container and volume names
CONTAINER_NAME="grafana-dashforge"
VOLUME_NAME="dashforge_grafana_data"
NETWORK_NAME="dashforge"

# Create network and volume if they don't exist
docker network create "$NETWORK_NAME" || true
docker volume create "$VOLUME_NAME" || true

# Stop and remove container if it already exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    docker rm -f "$CONTAINER_NAME"
fi

# Start Grafana container
docker run --name "$CONTAINER_NAME" \
    --network "$NETWORK_NAME" \
    -v "$VOLUME_NAME:/var/lib/grafana" \
    -e "GF_SECURITY_ADMIN_USER=$GRAFANA_ADMIN_USER" \
    -e "GF_SECURITY_ADMIN_PASSWORD=$GRAFANA_ADMIN_PASSWORD" \
    -e "GF_USERS_ALLOW_SIGN_UP=false" \
    -p 3000:3000 \
    --restart unless-stopped \
    -d grafana/grafana

# Wait until Grafana is ready
echo "Waiting for Grafana to start..."
until curl -s -f http://localhost:3000/api/health >/dev/null 2>&1; do
    echo "Waiting for Grafana..."
    sleep 2
done

echo "Grafana setup completed successfully!"
