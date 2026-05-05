# To-Do Manager with Microservices

Веб-приложение для управления задачами на Python Flask.

Проект состоит из трех сервисов:

1. `todo-app` — основное приложение To-Do Manager.
2. `priority-service` — микросервис определения приоритета задачи.
3. `stats-service` — микросервис расчета статистики задач.

## Запуск проекта

```bash
docker compose up --build
```

или:

```bash
docker-compose up --build
```

## Адреса сервисов

Основное приложение:

```text
http://localhost:5000
```

Микросервис приоритетов:

```text
http://localhost:5001
```

Микросервис статистики:

```text
http://localhost:5002
```

## Проверка priority-service

```bash
curl -X POST http://localhost:5001/priority \
-H "Content-Type: application/json" \
-d "{\"title\":\"Срочно сделать отчет\"}"
```

## Проверка stats-service

```bash
curl -X POST http://localhost:5002/stats \
-H "Content-Type: application/json" \
-d "{\"tasks\":[{\"title\":\"Задача 1\",\"completed\":true,\"priority\":\"high\"},{\"title\":\"Задача 2\",\"completed\":false,\"priority\":\"normal\"}]}"
```
