
from app.database import get_connection
from app.models.ticket import Ticket, Priority, Status


class TicketRepository:
    def __init__(self, connection_factory=None):
        self.connection_factory = connection_factory or get_connection

    @staticmethod
    def _row_to_ticket(row):
        ticket = Ticket(
            row[0],
            row[1],
            row[2],
            Priority(row[3]),
        )

        ticket.status = Status(row[4])

        return ticket

    def save(self, ticket):
        with self.connection_factory() as connection:
            row = connection.execute(
                """
                INSERT INTO tickets (
                    title,
                    description,
                    priority,
                    status
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    ticket.title,
                    ticket.description,
                    ticket.priority.value,
                    ticket.status.value,
                ),
            ).fetchone()

        ticket.id = row[0]

    def find_all(self):
        with self.connection_factory() as connection:
            rows = connection.execute(
                """
                SELECT id, title, description, priority, status
                FROM tickets
                ORDER BY id
                """
            ).fetchall()

        return [
            self._row_to_ticket(row)
            for row in rows
        ]

    def find_by_id(self, ticket_id):
        with self.connection_factory() as connection:
            row = connection.execute(
                """
                SELECT id, title, description, priority, status
                FROM tickets
                WHERE id = %s
                """,
                (ticket_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_ticket(row)

    def update_status(self, ticket_id, status):
        with self.connection_factory() as connection:
            connection.execute(
                """
                UPDATE tickets
                SET status = %s
                WHERE id = %s
                """,
                (
                    status.value,
                    ticket_id,
                ),
            )

    def delete(self, ticket_id):
        with self.connection_factory() as connection:
            cursor = connection.execute(
                """
                DELETE FROM tickets
                WHERE id = %s
                """,
                (ticket_id,),
            )

            return cursor.rowcount > 0