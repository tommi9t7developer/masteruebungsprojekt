class TicketRepository:
    def __init__(self):
        self.tickets = []
        self.next_id = 1

    def save(self, ticket):
        ticket.id = self.next_id
        self.next_id += 1
        self.tickets.append(ticket)

    def find_all(self):
        return self.tickets

    def find_by_id(self, ticket_id):
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                return ticket

        return None

    def delete(self, ticket_id):
        ticket = self.find_by_id(ticket_id)

        if ticket is None:
            return False

        self.tickets.remove(ticket)
        return True