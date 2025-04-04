Device Monitoring System \
Сервис для сбора и анализа данных с устройств. \
  Возможности: 
```
Сбор статистики устройств (координаты/измерения x, y, z)
Хранение данных с временными метками и идентификаторами устройств
Анализ статистики за определенные периоды времени или за все время
Расчет метрик: мин., макс., количество, сумма, медиана
Дополнительное управление пользователями
Дополнительная аналитика по идентификатору пользователя
```
Стек 
```
FastAPI: Web framework
SQLAlchemy: ORM for database operations
PostgreSQL: Database 
Celery: Asynchronous task processing 
Redis: Message broker for Celery 
Docker & Docker Compose: Containerization
Locust: Load testing 
```
Начало \
--Необходим Docker и Docker Compose 

Копируйте репозиторий: 
```
git clone <repository-url>

```
Запустите сервисы: 
```
Copydocker-compose up -d
```
API: 
```
http://localhost:8000/docs
```

API Endpoints 

Core Endpoints 
```
POST /api/devices/{device_id}/data

Add device statistics
Request body: {"x": float, "y": float, "z": float}
GET /api/analytics/devices/{device_id}

Get analytics for device

Query parameters:

start_time: Start of time period 
end_time: End of time period 

Add device statistics

POST /api/users/
Create a new user
Request body: {"username": string, "email": string}
POST /api/devices/

Create a new device

Request body: {"name": string, "user_id": string}
GET /api/analytics/users/{user_id}
Get analytics for all devices belonging to user

Query parameters:

start_time: Start of time period (optional)
end_time: End of time period (optional)
aggregate: Whether to aggregate results (default: true)
```
Optional Endpoints 
```
POST /api/users/

Create a new user

Request body: {"username": string, "email": string}
POST /api/devices/

Create a new device

Request body: {"name": string, "user_id": string}
GET /api/analytics/users/{user_id}
Get analytics for all devices belonging to user

Query parameters:

start_time: Start of time period 
end_time: End of time period 
aggregate: Whether to aggregate results (default: true)
Response: Analytics aggregated or per device
```


Нагрузочное тестирование \
Чтобы запустить понадобится Locust: 
```
Run the Locust test:
Copycd load_tests
locust -f locustfile.py --host=http://localhost:8000

Open Locust UI at http://localhost:8089
```
