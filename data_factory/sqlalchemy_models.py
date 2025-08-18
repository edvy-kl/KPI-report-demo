"""SQLAlchemy models module.

This module defines the SQLAlchemy ORM models that represent
database tables and their relationships.
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Customer(Base):
    """Customer model representing the customers table.

    Attributes:
        customer_id (UUID): Unique identifier for the customer.
        name (str): Customer's first name.
        surname (str): Customer's last name.
        username (str): Customer's username.
        is_active (bool): Whether the customer account is active.
        time_created (datetime): Timestamp when the record was created.
        time_updated (datetime): Timestamp when the record was last updated.
        age (int): Customer's age.
    """

    __tablename__ = "customers"
    __table_args__ = {"schema": "ESHOP_EU"}

    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    time_created = Column(DateTime, nullable=False, default=datetime.now(UTC))
    time_updated = Column(DateTime, nullable=True)
    age = Column(Integer, nullable=False)
