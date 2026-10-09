from app.database import get_connection
from app.models.ticket import Ticket, Priority, Status


class TicketRepository:

    def _to_ticket(self, row):
        ticket = Ticket(
            row["id"],
            row["title"],
            row["description"],
            Priority(row["priority"]),
        )
        ticket.status = Status(row["status"])
        return ticket

    def save(self, ticket):
        with get_connection() as connection:
            row = connection.execute(
                """
                INSERT INTO tickets (title, description, priority, status)
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
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, title, description, priority, status
                FROM tickets
                ORDER BY id
                """
            ).fetchall()

        return [
            TicketRepository._row_to_ticket(row)
            for row in rows
        ]

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

    def find_by_id(self, ticket_id):
        with get_connection() as connection:
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
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE tickets
                SET status = %s
                WHERE id = %s
                """,
                (status.value, ticket_id),
            )

    def delete(self, ticket_id):
        with get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM tickets WHERE id = %s",
                (ticket_id,),
            )
            return cursor.rowcount > 0