from server.repository import TicketRepository
from server.ticket import Ticket


class TicketService:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def create_ticket(self, ticket: Ticket):
        """Добавление рейса"""
        return self.repository.create_ticket(ticket)

    def get_all(self):
        '''Получить все полёты'''
        return self.repository.get_all()

    def get_by_id(self, ticket_id: int):
        '''Получить полёт по id'''
        return self.repository.get_by_id(ticket_id)

    def update_ticket(self, ticket: Ticket):
        """Изменить существующий рейс.
            Если рейса не существует, ничего не делать."""
        return self.repository.update_ticket(ticket)

    def delete_ticket(self, ticket_id: int):
        """Удалить существующий рейс.
            Если рейса не существует, ничего не делать."""
        return self.repository.delete_ticket(ticket_id)