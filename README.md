# Chuy Tourism Analysis API

Мини-проект для дипломной работы по анализу туристического спроса на территории Чуйской области.

## Технологии
- **Django & DRF**: Основной фреймворк для разработки API.
- **PostgreSQL**: База данных для хранения данных о туризме.
- **Django ORM**: ORM для работы с БД.
- **Redis**: Кеширование через `django-redis`.
- **Docker & Docker Compose**: Контейнеризация и развертывание.
- **Swagger (drf-spectacular)**: Автоматическая документация API.

## Как запустить
1. Убедитесь, что у вас установлен Docker и Docker Compose.
2. Создайте файл `.env` на основе `.env.example`.
3. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```
4. Примените миграции:
   ```bash
   docker-compose exec web python manage.py migrate
   ```
5. API будет доступно по адресу: `http://localhost:8000/api/`
6. Документация Swagger: `http://localhost:8000/api/docs/`

## Особенности безопасности
- **JWT Authentication**: Защита эндпоинтов через SimpleJWT.
- **CORS**: Настроен через `django-cors-headers`.
- **Environment Variables**: Все чувствительные данные хранятся в `.env`.

## Структура проекта
- `core/`: Настройки проекта Django.
- `tourism/`: Основное приложение с логикой туризма.
  - `models.py`: Модели данных (Места, Отзывы, Фото).
  - `serializers.py`: Преобразование данных в JSON.
  - `views.py`: Обработка запросов и бизнес-логика.
- `static/` & `media/`: Статические файлы и загруженные изображения.
