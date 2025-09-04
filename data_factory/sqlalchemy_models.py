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


class Ticket(Base):
    """Customer model representing the customers table.

    Attributes:
        ticket_id (UUID): Unique identifier for the ticket.
        active (bool): Whether the ticket is active.
        time_created (datetime): Timestamp when the record was created.
         time_assigned (datetime): Timestamp when the record was assigned to an agent.
        time_closed (datetime): Timestamp when the record was closed.
        status (str): Status of the ticket.
        success_rate (int): Customer rating.
        needed_call (bool): Whether the followup call was needed.
    """

    __tablename__ = "tickets"
    __table_args__ = {"schema": "regional_office"}

    ticket_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    active = Column(Boolean, nullable=False)
    time_created = Column(DateTime, nullable=False)
    time_assigned = Column(DateTime, nullable=False)
    time_closed = Column(DateTime, nullable=True)
    status = Column(String, nullable=False)
    success_rate = Column(Integer, nullable=True)
    needed_call = Column(Boolean, nullable=False)
