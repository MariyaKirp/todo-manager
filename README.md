# To-Do Manager Microservices

Проект демонстрирует запуск To-Do менеджера и двух микросервисов через Docker Compose.

## Сервисы
- `todo-app` — основное Flask-приложение.
- `priority-service` — микросервис определения приоритета задачи.
- `stats-service` — микросервис статистики по задачам.

## Запуск
```bash
docker compose up --build
```

После запуска приложение доступно по адресу http://localhost:5000
