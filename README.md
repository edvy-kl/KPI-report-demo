# DashForge Lab

A lightweight framework for containerized Postgres and Grafana setups, enabling rapid database seeding and visualization **for local testing and data exploration only**.  
Perfect for development, QA, and dashboard prototyping — not production use.  

---

## Overview

DashForge Lab streamlines setting up PostgreSQL + Grafana locally by letting you:

- Define schema, users, and tables with simple YAML configs  
- Launch Postgres and Grafana containers with one command  
- Preconfigure Grafana dashboards (via YAML)  
- Seed test data easily with Python/SQLAlchemy examples  

---
## Motivation

Working with datasets from different runs and software versions often leads to repetitive plotting and one-off scripts. This setup provides a more streamlined approach:

* **Centralized storage**: Test data from multiple runs and versions is stored in a single PostgreSQL database.
* **Simple visualization**: Grafana dashboards replace ad-hoc plotting scripts, making it easy to compare results over time.
* **Reusability**: Once the dashboards are configured, they can be reused across datasets without extra coding.
* **Collaboration ready**: A Docker-based setup makes it easy to share the environment with teammates or replicate on new machines.

#### Use Cases
- Validate applications with realistic local database and dashboards  
- Run QA checks without touching production  
- Prototype and iterate on dashboards quickly  
- Spin up demo/training environments  
- Experiment with SQL queries or ETL pipelines safely  

---

## Prerequisites
- **Docker**  
- **Python 3.12+**  
- [`yq`](https://github.com/mikefarah/yq) + `jq` for YAML/JSON processing  

---

## Installation

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get install yq jq

# macOS
brew install yq jq
````

### Python Dependencies

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

---

## Quick Start

### 1. Database Setup

1. Create a `.env` file with database variables (see `database/db_setup.yaml`):

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_database_name
   RW_USERNAME=read_write_user
   RW_PASSWORD=rw_password
   RO_USERNAME=read_only_user
   RO_PASSWORD=ro_password
   PG_PASSWORD=postgres_password
   ```
2. Configure schema in `database/db_setup.yaml`.
3. Start Postgres:

   ```bash
   ./database/start-postgres-db.sh
   ```

### 2. Grafana Setup

1. Add Grafana credentials in `.env`:

   ```env
   GRAFANA_ADMIN_USER=admin
   GRAFANA_ADMIN_PASSWORD=your_secure_password
   ```
2. Start Grafana:

   ```bash
   ./grafana/start-grafana.sh
   ```
3. Access Grafana → [http://localhost:3000](http://localhost:3000)

---

## Data Seeding

A Python example (`insert_dummy_data.py`) shows how to insert data with SQLAlchemy.

* Define models in `data_factory/sqlalchemy_models.py`
* Customize relationships, validations, and constraints
* Run seeding:

  ```bash
  python insert_dummy_data.py
  ```

> **Note:** For larger/time-series datasets, consider batching inserts, tuning Postgres configs, and adding indexes.

---

## Customization

### Database

* Update `database/db_setup.yaml` for schema, tables, and permissions
* Tweak `database/postgresql.conf` for performance

### Grafana

* Configure a PostgreSQL datasource (`postgres-dashforge`) with your DB credentials

---

Here’s an updated version reflecting that the Postgres container now uses a persistent volume (`dashforge_pg_data`), so you probably don’t want to remove it unless you really want to clear the data:

---

## Cleanup

To stop and remove Postgres/Grafana containers:

```bash
# Stop containers
docker kill <container_id_or_name>

# Remove containers
docker rm <container_id_or_name>
```

> **Note:** The Postgres container uses a persistent Docker volume (`dashforge_pg_data`) to store data. Removing the container does **not** delete the data.

If you want to also remove the volume and clear the database:

```bash
# List volumes
docker volume ls

# Remove the volume (this deletes all stored data!)
docker volume rm dashforge_pg_data
```

---

## Limitations

DashForge Lab is designed **only for local development and testing**.
It is not intended for production or long-running environments.

* ❌ **Not secure** — credentials are stored in `.env` and containers run with minimal hardening
* ❌ **No persistence** — data is lost when volumes are removed
* ❌ **Not optimized for scale** — container configs use defaults, not tuned for heavy loads or large datasets
* ❌ **Limited scope** — supports PostgreSQL + Grafana only (no clustering, HA, or multi-DB setups)

Use it as a sandbox for exploration, prototyping, QA, or demos — not for hosting production dashboards!

---

## License

MIT License

