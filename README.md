# Tasks REST API

A simple CRUD REST API for managing tasks, built with Django and SQLite.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Server runs at `http://localhost:8000`

---

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/tasks` | Get all tasks |
| POST | `/api/tasks` | Create a new task |
| GET | `/api/tasks/{id}` | Get a task by ID |
| PUT | `/api/tasks/{id}` | Update a task by ID |
| DELETE | `/api/tasks/{id}` | Delete a task by ID |

---

## Examples

### Create a task

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'
```

Response `200`:
```json
{"id": 1, "title": "Buy groceries"}
```

---

### Get all tasks

```bash
curl http://localhost:8000/api/tasks
```

Response `200`:
```json
[
  {"id": 1, "title": "Buy groceries"},
  {"id": 2, "title": "Write code"}
]
```

---

### Get a task by ID

```bash
curl http://localhost:8000/api/tasks/1
```

Response `200`:
```json
{"id": 1, "title": "Buy groceries"}
```

---

### Update a task

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and milk"}'
```

Response `200`:
```json
{"id": 1, "title": "Buy groceries and milk"}
```

---

### Delete a task

```bash
curl -X DELETE http://localhost:8000/api/tasks/1
```

Response `200`:
```json
{"message": "Task deleted successfully."}
```

---

## Error Responses

**Task not found (404)**
```json
{"error": "Task not found."}
```

**Missing title (400)**
```json
{"error": "title is required."}
```

**Invalid JSON body (400)**
```json
{"error": "Invalid JSON."}
```
