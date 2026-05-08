# Chuy Tourism Analysis API

Мини-проект для дипломной работы по анализу туристического спроса на территории Чуйской области.

## Технологии
- **FastAPI**: Основной фреймворк.
- **PostgreSQL**: База данных для хранения данных о туризме.
- **SQLAlchemy**: ORM для работы с БД.
- **Redis & FastAPI-Cache2**: Кеширование ответов API.
- **Docker & Docker Compose**: Контейнеризация и развертывание.
- **Pydantic Settings**: Управление конфигурацией через `.env`.

## Как запустить

1. Убедитесь, что у вас установлен Docker и Docker Compose.
2. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```
3. API будет доступно по адресу: `http://localhost:8000`
4. Документация Swagger: `http://localhost:8000/docs`

## Особенности безопасности
- **CORS**: Настроен в `app/main.py` через `BACKEND_CORS_ORIGINS`.
- **Environment Variables**: Все чувствительные данные (пароли, ключи) хранятся в `.env`.
- **Validation**: Строгая типизация и валидация входящих данных через Pydantic.

## Структура проекта
- `app/api`: Эндпоинты API.
- `app/core`: Конфигурация и безопасность.
- `app/db`: Подключение к БД и базовые классы.
- `app/models`: Модели SQLAlchemy.
- `app/schemas`: Схемы Pydantic.
- `app/cache`: Логика кеширования (настроено в `main.py`).
