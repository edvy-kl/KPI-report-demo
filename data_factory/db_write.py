"""Database write operations module.

This module provides functions for writing data to the database,
including bulk upserting (insert or update) customer records.
"""

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from data_factory.sqlalchemy_models import Customer


def upsert_data(session, fake_customers: list[Customer]):
    """Bulk upsert customer records into the database.

    Args:
        session: SQLAlchemy session factory
        fake_customers: List of customer data dictionaries
    """

    with session() as session:
        try:

            stmt = insert(Customer).values(
                [
                    {
                        "customer_id": c.customer_id,
                        "name": c.name,
                        "surname": c.surname,
                        "username": c.username,
                        "is_active": c.is_active,
                        "time_created": c.time_created,
                        "time_updated": c.time_updated,
                        "age": c.age,
                    }
                    for c in fake_customers
                ]
            )

            # Use the 'on_conflict_do_update' method to handle conflicts
            stmt = stmt.on_conflict_do_update(
                index_elements=["customer_id"],  # The column(s) for conflict resolution
                set_=dict(
                    name=stmt.excluded.name,
                    surname=stmt.excluded.surname,
                    username=stmt.excluded.username,
                    is_active=stmt.excluded.is_active,
                    time_created=stmt.excluded.time_created,
                    time_updated=stmt.excluded.time_updated,
                    age=stmt.excluded.age,
                ),
            )

            # Execute the statement
            session.execute(stmt)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise SQLAlchemyError(f"Failed to bulk upsert data: {str(e)}") from e
