📝 Task Management API
📌 Описание проекта

Task Management API — это бэкенд-сервис для управления задачами, категориями и напоминаниями.
Реализован на Django REST Framework, использует PostgreSQL в качестве основной базы данных, Redis + Celery для очередей задач и фоновых напоминаний, а также JWT-аутентификацию для защиты API.

🔑 Ключевые возможности

Регистрация пользователей и JWT-аутентификация

Создание, обновление и удаление задач

Привязка задач к категориям

Приоритеты, статусы, дедлайны

Фильтрация задач по параметрам (status, priority, category, deadline)

Отправка напоминаний о задаче через Celery (email)

Защищённые эндпоинты — пользователь может управлять только своими задачами и категориями

Полная контейнеризация через Docker (web + db + redis + celery + celery beat)

🏗 Архитектура
Используемые технологии:

Django — основной веб-фреймворк

Django REST Framework — реализация API

PostgreSQL — основная БД

Redis — брокер очередей для Celery

Celery Worker + Celery Beat — обработка фоновых задач и планировщик

JWT Authentication — авторизация пользователей

Docker Compose — запуск всего проекта одной командой

Основная схема работы:

Пользователь создаёт задачу → сохраняется в PostgreSQL

Пользователь может запросить «Напомнить о задаче»

Django отправляет задачу в Celery → Celery Worker обрабатывает

Redis используется как брокер сообщений

Celery отправляет email-напоминание

Celery Beat выполняет периодические фоновые задания (если добавишь в будущем)

📂 Основные эндпоинты
🔐 Аутентификация

POST /api/auth/register/ — регистрация
POST /api/auth/login/ — получение JWT токенов

🗂 Категории

GET /api/categories/ — список
POST /api/categories/ — создание
PUT /api/categories/{id}/ — обновление
DELETE /api/categories/{id}/ — удаление

✅ Задачи

GET /api/tasks/ — список задач

поддержка фильтров:
?status=TODO&priority=HIGH&category=1&deadline_before=2025-01-01

POST /api/tasks/ — создание
PATCH /api/tasks/{id}/ — обновление
DELETE /api/tasks/{id}/ — удаление

🔔 Напоминание о задаче

POST /api/tasks/{id}/remind/
Запускает Celery задачу → отправляется email пользователю.

⚙ Установка и запуск
1️⃣ Клонируем репозиторий
git clone https://github.com/akiraliebert/Task-Management-Api.git
cd Task-Management-Api

2️⃣ Создаём .env файл

Важно: .env не хранится в репозитории.

Пример:

SECRET_KEY=super-secret-key

POSTGRES_DB=task_db
POSTGRES_USER=task_user
POSTGRES_PASSWORD=task_password
POSTGRES_HOST=db
POSTGRES_PORT=5442

REDIS_HOST=redis
REDIS_PORT=6379

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@example.com

3️⃣ Запуск через Docker
docker-compose up -d --build

Сервисы:
Сервис	Назначение
web	Django + DRF API
db	PostgreSQL
redis	брокер очередей
celery	Celery worker
celery-beat	периодические задачи
🚀 Использование API (Примеры)
➕ Создание задачи

POST /api/tasks/

{
  "title": "Buy milk",
  "description": "2 liters",
  "priority": "HIGH",
  "status": "TODO",
  "deadline": "2025-12-20T12:00:00Z",
  "category": 1
}

🔔 Напоминание о задаче

POST /api/tasks/3/remind/

Ответ:

{
  "detail": "Reminder scheduled"
}


Celery отправит email пользователю.

🧪 Тестирование

Тестирование API производится через:

Postman

Django Test Framework (можно добавить позже)

Автоматические проверки Docker контейнеров

💡 Особенности реализации

Чёткое разграничение доступа: пользователи видят только свои данные

Фильтрация реализована через django-filters

Напоминания вынесены в Celery для стабильной асинхронной работы

Redis используется как брокер, но легко расширяется до кэширования

Все конфиги вынесены в .env — проект удобен для деплоя

🛠 Стек технологий

Python 3.12

Django 5

Django REST Framework

PostgreSQL

Redis

Celery

Docker + Docker Compose

JWT
