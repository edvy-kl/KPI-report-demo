"""
Main script to insert test data in the database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_factory.customer_factory import CustomerFactory
from data_factory.db_auth import DB_URL
from data_factory.db_write import upsert_data

if __name__ == "__main__":

    #
    engine = create_engine(DB_URL)
    session = sessionmaker(bind=engine)

    user_factory = CustomerFactory()

    fake_customers = user_factory.create_fake_customers(100)

    upsert_data(session, fake_customers)
