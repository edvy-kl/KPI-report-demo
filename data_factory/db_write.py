"""Database write operations module.

This module provides functions for writing data to the database,
including bulk upserting (insert or update) ticket records.
"""

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from data_factory.sqlalchemy_models import Ticket


def upsert_data(session, fake_tickets: list[Ticket]):
    """Bulk upsert ticket records into the database.

    Args:
        session: SQLAlchemy session factory
        fake_tickets: List of ticket data dictionaries
    """

    with session() as session:
        try:

            stmt = insert(Ticket).values(
                [
                    {
                        "ticket_id": c.ticket_id,
                        "active": c.active,
                        "time_created": c.time_created,
                        "time_assigned": c.time_assigned,
                        "time_closed": c.time_closed,
                        "status": c.status,
                        "success_rate": c.success_rate,
                        "needed_call": c.needed_call,
                    }
                    for c in fake_tickets
                ]
            )

            # Use the 'on_conflict_do_update' method to handle conflicts
            stmt = stmt.on_conflict_do_update(
                index_elements=["ticket_id"],  # The column(s) for conflict resolution
                set_=dict(
                    active=stmt.excluded.active,
                    time_created=stmt.excluded.time_created,
                    time_assigned=stmt.excluded.time_assigned,
                    time_closed=stmt.excluded.time_closed,
                    status=stmt.excluded.status,
                    success_rate=stmt.excluded.success_rate,
                    needed_call=stmt.excluded.needed_call,
                ),
            )

            # Execute the statement
            session.execute(stmt)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise SQLAlchemyError(f"Failed to bulk upsert data: {str(e)}") from e
