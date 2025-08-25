## Сервис реализованный на FastAPI для доступа к итогам торгов Секции «Нефтепродукты» СПбМТСБ
Приложение использует уже наполненную парсером [**SPIMEX Async Parser**](https://github.com/KuznetcovIvan/asyncio-section) таблицу.

---

### Реализовано:
- эндпоинты:
    - со списком дат последних торговых дней (с фильтрацией по кол-ву последних торговых дней);
    - со списком торгов за заданный период (с фильтрацией по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date);
    - со списком последних торгов (с фильтрацией по oil_id, delivery_type_id, delivery_basis_id);
- кеширование запросов (Redis);
- ежедневный сброс кэша в `14:11`.
---

### Установка и запуск:
1. Установить, при необходимости, менеджер пакетов `pip install uv`
2. Клонировать репозиторий 
- `git clone https://github.com/KuznetcovIvan/fastapi-section.git`
3. Перейти в корневую директорию проекта
- `cd fastapi-section`
4. Установить зависимости проекта
- `uv sync`
- `uv sync --group dev` (с dev-инструментами)
5. Создать файл с переменными окружения (.env)
- образец в [`.env.example`](.env.example).
6. Запустить сервис в режиме разработки
- `uv run uvicorn app.main:app --reload`

---

### Документация доступна по URL:
- Swagger UI
[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- ReDoc
[`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)

---

### Для работы требуется:
- запущенный PostgreSQL **с заполненной таблицей** данными торгов;
- запущенный Redis для кеширования.

---

### Стек:
- uv
- PostgreSQL  
- Redis  
- FastAPI  
- Uvicorn  
- Pydantic  
- SQLAlchemy + asyncpg  
- fastapi-cache2  
- APScheduler

---

### Пример работы:

![example](image/example_1.PNG)
![example](image/example_2.PNG)
![example](image/example_3.PNG)
![example](image/example_4.PNG)