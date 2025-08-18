"""Database configuration and connection module.

This module loads database credentials and configuration from a YAML
file with support for environment variable substitution. It provides
the SQLAlchemy-compatible database URL for connecting to PostgreSQL.
"""

import os
from typing import Any

import yaml
from dotenv import load_dotenv
from sqlalchemy.engine import URL


class EnvVarLoader(yaml.Loader):
    """Custom YAML loader that supports environment variable substitution.

    Any scalar value starting with '$' will be replaced with the
    corresponding environment variable value.
    """

    def construct_scalar(self, node: yaml.nodes.ScalarNode) -> Any:
        value = super().construct_scalar(node)
        if isinstance(value, str) and value.startswith("$"):
            return os.getenv(value[1:])
        return value


def load_db_config(yaml_path: str = "database/db_setup.yaml") -> dict[str, str]:
    """Load database configuration from the db_setup YAML file with env var support.

    Args:
        yaml_path (str): Path to the YAML configuration file.

    Returns:
        Dict[str, Any]: Dictionary containing database connection parameters.
    """
    with open(yaml_path) as f:
        cfg = yaml.load(f, Loader=EnvVarLoader)

    db = cfg["database"]
    return {
        "username": db["users"]["rw_username"],
        "password": db["users"]["rw_password"],
        "host": db.get("host", "localhost"),
        "port": db["port"],
        "database": db["name"],
        "schema": db["schema"]["name"]
    }


# Load environment variables from .env file
load_dotenv()

# Extract DB config and build SQLAlchemy URL
db_config = load_db_config()
DB_SCHEMA = db_config.pop("schema")
DB_URL = URL.create(drivername="postgresql",**db_config)
