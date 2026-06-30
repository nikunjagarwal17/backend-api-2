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

---

## Step 2 — Task List Page

URL: `/tasks`

Renders an HTML page listing all tasks using Django's template inheritance.

- `templates/common.html` defines the shared header and footer
- `templates/list.html` extends it via `{% extends "common.html" %}` and fills `{% block content %}`
- Task titles are output with `{{ task.title }}` — Django auto-escapes HTML, so a title like `<script>alert(1)</script>` renders as plain text and is never executed

---

## Step 3 — User Search

### POST /api/users/search

Search users with dynamic AND conditions. All fields are optional. Omitting all fields returns every user.

**Request body:**

| Field | Type | Description |
|-------|------|-------------|
| name | string | Partial, case-insensitive match on name |
| email | string | Partial, case-insensitive match on email |
| minAge | integer | Age >= minAge |
| maxAge | integer | Age <= maxAge |

**Response `200`** — list of matching users with their orders:

```json
[
  {
    "id": 1,
    "name": "Emma Davis",
    "email": "emma@example.com",
    "age": 29,
    "orders": [
      {"id": 3, "itemName": "Notebook"}
    ]
  }
]
```

No matches returns `200` with `[]`.

### Examples

**Search by name (partial match):**
```bash
curl -X POST http://localhost:8000/api/users/search \
  -H "Content-Type: application/json" \
  -d '{"name": "son"}'
```

**Search by age range:**
```bash
curl -X POST http://localhost:8000/api/users/search \
  -H "Content-Type: application/json" \
  -d '{"minAge": 20, "maxAge": 30}'
```

**Combined conditions (AND):**
```bash
curl -X POST http://localhost:8000/api/users/search \
  -H "Content-Type: application/json" \
  -d '{"name": "Emma", "minAge": 29}'
```

**Return all users (no conditions):**
```bash
curl -X POST http://localhost:8000/api/users/search \
  -H "Content-Type: application/json" \
  -d '{}'
```
