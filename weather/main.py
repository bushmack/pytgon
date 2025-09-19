from database import DatabaseConfig, DatabaseConnection
from migrations import MigrationManager
from repository import FlightRepository
from service import FlightService
from fastapi import FastAPI, HTTPException
from flight import Flight

# Initialize
## DB config
db_config = DatabaseConfig(
    'flightsdb',
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
repository = FlightRepository(db_connection)
service = FlightService(repository)

app = FastAPI(
    title="Flight API"
)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}


@app.get("/flights")
async def get_flights():
    try:
        return service.get_all()
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при получении полётов: {str(e)}")

@app.get("/flights/{flight_id}")
async def get_flight_by_id(flight_id: int):
    try:
        flight = service.get_by_id(flight_id)
        if not flight:
            raise HTTPException(status_code=404, detail="Полёт не найден")
        return flight
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении полёта: {str(e)}")


@app.post("/flights")
async def create_flight(flight_data: dict):
    try:
        # Validation
        required_fields = ["price", "plane"]
        for field in required_fields:
            if field not in flight_data:
                raise HTTPException(status_code=400, detail=f"Отсутствует обязательное поле {field}")

        flight = Flight(
            price=flight_data['price'],
            plane=flight_data['plane']
        )

        created_flight = service.create_flight(flight)
        return created_flight

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при добавлении полёта: {str(e)}")

@app.put("/flights/{flight_id}")
async def update_flight(flight_id: int, flight_data: dict):
    try:
        # Проверка наличия данных для обновления
        if not flight_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления")
        # Создаем объект Flight с обновленными данными
        flight = Flight(
            id=flight_id,
            price=flight_data.get('price'),
            plane=flight_data.get('plane')
        )
        updated_flight = service.update_flight(flight_id, flight)
        if not updated_flight:
            raise HTTPException(status_code=404, detail="Полёт не найден для обновления")
        return updated_flight
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении полёта: {str(e)}")


@app.delete("/flights/{flight_id}")
async def delete_flight(flight_id: int):
    try:
        result = service.delete_flight(flight_id)
        if not result:
            raise HTTPException(status_code=404, detail="Полёт не найден для удаления")
        return {"message": "Полёт успешно удалён"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении полёта: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
