"""
Main script to insert test data in the database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_factory.tickets_factory import TicketFactory
from data_factory.db_auth import DB_URL
from data_factory.db_write import upsert_data

if __name__ == "__main__":

    #
    engine = create_engine(DB_URL)
    session = sessionmaker(bind=engine)

    ticket_factory = TicketFactory()

    fake_tickets = ticket_factory.create_fake_tickets()

    print(f"Inserting {len(fake_tickets)} tickets in the database...")

    upsert_data(session, fake_tickets)
