"""Customer data factory module for generating fake customer records.

This module provides functionality to create fake customer data for testing
and development purposes.
"""

import uuid
from datetime import UTC, datetime

from faker import Faker

from .sqlalchemy_models import Customer


class CustomerFactory:
    """Factory class for generating fake customer data.

    This class provides methods to create individual fake customers or
    bulk generate multiple customer records for testing purposes.

    Attributes:
        fake (Faker): Instance of Faker used to generate fake data.
    """

    def __init__(self) -> None:
        """Initialize the CustomerFactory with a Faker instance."""
        self.fake = Faker()

    def create_fake_customer(self) -> Customer:
        """Create a single fake customer record.

        Returns:
            Customer: A new Customer instance with randomly generated data.
        """
        return Customer(
            customer_id=uuid.uuid4(),
            name=self.fake.first_name(),
            surname=self.fake.last_name(),
            username=self.fake.user_name(),
            is_active=self.fake.boolean(chance_of_getting_true=80),
            time_created=datetime.now(UTC),
            time_updated=None,
            age=self.fake.random_int(min=18, max=100),
        )

    def create_fake_customers(self, count: int) -> list[Customer]:
        """Create multiple fake customer records.

        Args:
            count (int): Number of fake customers to generate.

        Returns:
            List[dict]: List of customer records as dictionaries.
        """
        return [self.create_fake_customer() for _ in range(count)]
