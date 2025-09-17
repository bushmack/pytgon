from database import DatabaseConfig, DatabaseConnection
from migrations import MigrationManager
from repository import TicketRepository
from service import TicketService
from fastapi import FastAPI, HTTPException
from ticket import Ticket

# Initialize
## DB config
db_config = DatabaseConfig(
    'ticketsdb',
    'postgres',
    'postgres',
    '123Secret_a',
    5432
)
db_connection = DatabaseConnection(db_config)
## Migrations
migration_manager = MigrationManager(db_config)
migration_manager.create_tables()
# Repository and Service
repository = TicketRepository(db_connection)
service = TicketService(repository)

app = FastAPI(
    title="Ticket API"
)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}


@app.get("/tickets")
async def get_tickets():
    try:
        return service.get_all()
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при получении билета: {str(e)}")

@app.get("/tickets/{ticket_id}")
async def get_ticket_by_id(ticket_id: int):
    try:
        ticket = service.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Билет не найден")
        return ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении билета: {str(e)}")


@app.post("/tickets")
async def create_ticket(ticket_data: dict):
    try:
        # Validation
        required_fields = ["row", "place", "name_movie", "price"]
        for field in required_fields:
            if field not in ticket_data:
                raise HTTPException(status_code=400, detail=f"Отсутствует обязательное поле {field}")

        ticket = Ticket(
            row=ticket_data['row'],
            place=ticket_data['place'],
            name_movie=ticket_data['name_movie'],
            price=ticket_data['price']
        )

        created_ticket = service.create_ticket(ticket)
        return created_ticket

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при добавлении билета: {str(e)}")



@app.delete("/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int):
    try:
        result = service.delete_ticket(ticket_id)
        if not result:
            raise HTTPException(status_code=404, detail="Билет не найден для удаления")
        return {"message": "Билет успешно удалён"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении билета: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)