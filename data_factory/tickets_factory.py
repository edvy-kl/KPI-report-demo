"""Ticket data factory module for generating fake ticket records.

This module provides functionality to create fake ticket data for testing
and development purposes.
"""

import random
import uuid
from datetime import UTC, datetime, timedelta

from faker import Faker

from .sqlalchemy_models import Ticket


class TicketFactory:
    """Factory class for generating fake Ticket data.

    This class provides methods to create individual fake tickets or
    bulk generate multiple ticket records for testing purposes.

    Attributes:
        fake (Faker): Instance of Faker used to generate fake data.
    """

    def __init__(self) -> None:
        """Initialize the ticketFactory with a Faker instance."""
        self.fake = Faker()

    @staticmethod
    def _hours_to_minute(hours: float) -> int:
        return int(hours * 60)

    def _time_assigned(
        self,
        time_created: datetime,
        minimum_interval: float = 0.5,
        maximum_interval: float = 24,
    ) -> datetime | None:
        """Add random time interval to time created depending on the year"""

        return time_created + timedelta(
            minutes=self.fake.random_int(
                self._hours_to_minute(minimum_interval),
                self._hours_to_minute(maximum_interval),
            )
        )

    def _time_closed(
        self,
        active: bool,
        time_assigned: datetime,
        minimum_closed_interval: float = 0.5,
        maximum_closed_interval: float = 72,
    ) -> datetime | None:
        if active:
            return None
        else:
            return time_assigned + timedelta(
                minutes=self.fake.random_int(
                    self._hours_to_minute(minimum_closed_interval),
                    self._hours_to_minute(maximum_closed_interval),
                )
            )

    def _is_active(self, time_created) -> bool:
        """return false if ticket was created more than 2 days ago, otherwise return false or true with 80% probability of true"""
        if time_created < datetime.now(tz=UTC) - timedelta(days=2):
            return False
        else:
            return self.fake.boolean(chance_of_getting_true=80)

    @staticmethod
    def _status(active: bool) -> str:
        """
        If ticket is active return a random active status, otherwise return a random inactive status based
        on predefined weight
        """

        ACTIVE_STATUS = ["new", "in_progress", "waiting_for_customer"]

        # inactive statuses have weights that represent the relative probability of the status being chosen
        INACTIVE_STATUS = {"resolved": 0.7, "cancelled": 0.10, "need_development": 0.20}

        if active:
            return random.choice(ACTIVE_STATUS)
        else:
            return random.choices(
                list(INACTIVE_STATUS.keys()), list(INACTIVE_STATUS.values()), k=1
            )[0]

    def _success_rate(self, active: bool, time_created: datetime) -> int | None:
        """Fake the success rate depending on the year and the ticket active status"""
        # When ticket is active success rate must not be set
        if active:
            return None

        if time_created.year == 2023:
            return self.fake.random_int(1, 5)
        elif time_created.year == 2024:
            return self.fake.random_int(2, 5)
        else:
            return self.fake.random_int(3, 5)

    def create_fake_ticket(
        self,
        active: bool,
        time_created: datetime,
        time_assigned: datetime,
        time_closed: datetime,
        success_rate: int,
        status: str,
    ) -> Ticket:
        """Create a single fake ticket record.

        Returns:
            Ticket: A new Ticket instance with randomly generated data.
        """

        if status == "new":
            needed_call = False
        else:
            needed_call = self.fake.boolean(chance_of_getting_true=30)

        return Ticket(
            ticket_id=uuid.uuid4(),
            active=active,
            time_created=time_created,
            time_assigned=time_assigned,
            time_closed=time_closed,
            status=status,
            success_rate=success_rate,
            needed_call=needed_call,
        )

    def create_fake_tickets(self) -> list[Ticket]:
        """Create multiple fake ticket records.

        Returns:
            List[dict]: List of ticket records as dictionaries.
        """

        time_created = datetime(2023, 2, 12, tzinfo=UTC)

        tickets_records = []
        max_hour_interval = 24
        max_closed_interval = 72

        while time_created <= datetime.now(tz=UTC):

            time_created = time_created + timedelta(
                minutes=self.fake.random_int(30, 300)
            )

            time_assigned = self._time_assigned(
                time_created, maximum_interval=max_hour_interval
            )

            active = self._is_active(time_created)

            time_closed = self._time_closed(
                active, time_assigned, maximum_closed_interval=max_closed_interval
            )

            status = self._status(active)

            success_rate = self._success_rate(active, time_created)

            tickets_records.append(
                self.create_fake_ticket(
                    active,
                    time_created,
                    time_assigned,
                    time_closed,
                    success_rate,
                    status,
                )
            )
            # increase max interval for time_assigned and time_closed in order to show the time to first response and time to resolution is getting shorter
            max_hour_interval -= 0.002
            max_closed_interval -= 0.004

        return tickets_records
