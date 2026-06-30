# Project Explanation

---

## Step 1 — Task CRUD REST API

- Created a full Django project structure including `manage.py`, `backend/settings.py`, and URL routing so the app can actually run.
- Defined the `Task` model in `api/models.py` with two fields: `id` (auto-increment primary key) and `title` (varchar 255), mapped to a `tasks` table in SQLite.
- Implemented `TaskListView` to handle `GET /api/tasks` (returns all tasks ordered by id) and `POST /api/tasks` (reads `title` from the JSON body, creates a new record, and returns it).
- Implemented `TaskDetailView` to handle `GET`, `PUT`, and `DELETE` on `/api/tasks/{id}` — each method first looks up the task by primary key and returns a `404` if it does not exist, then performs the requested operation.
- All responses are plain JSON using Django's built-in `JsonResponse`. Input validation (missing title, bad JSON) returns a `400` with an error message. No third-party serializer library was used — a simple `task_to_dict` helper converts model instances to dicts inline.

---

## Step 2 — Task List HTML Page

- Created `templates/list.html` to render the task list as an HTML page at `/tasks`, using Django's template engine rather than returning raw JSON.
- Used `{% extends "common.html" %}` so the page automatically inherits the shared header (`<h1>Task App</h1>`) and footer (`© 2025 TaskApp`) defined in `templates/common.html` without duplicating that markup.
- Placed all page-specific content inside `{% block content %}...{% endblock %}`, which is the slot defined in `common.html` — this is Django's template inheritance pattern.
- Rendered the task list with a `{% for task in tasks %}` loop that produces a `<ul>` containing one `<li><span>title</span></li>` per task, matching the required DOM structure exactly.
- Applied XSS protection by using `{{ task.title }}` without the `|safe` filter — Django escapes HTML characters by default, so a malicious title like `<script>alert(1)</script>` is rendered as `&lt;script&gt;` plain text and never executed by the browser.

---

## Step 3 — Dynamic User Search

- Implemented `POST /api/users/search` in `UserSearchView` which accepts a JSON body with up to four optional filters: `name`, `email`, `minAge`, and `maxAge`.
- Started with `User.objects.all()` as the base queryset and conditionally chained `.filter()` calls — each filter is only applied when its corresponding field is present in the request body, so omitting all fields returns every user.
- Used `name__icontains` and `email__icontains` for case-insensitive partial matching, meaning a search for `"son"` matches names like `"Johnson"` or `"Sonata"`.
- Used `age__gte` for `minAge` and `age__lte` for `maxAge` — when both are provided Django combines them as a single AND condition, filtering users within the age range.
- Each user in the result includes their associated orders (fetched via `prefetch_related('orders')`) formatted as `{"id": ..., "itemName": ...}`. When no users match the conditions, the endpoint returns `200` with an empty array `[]`.

---

## Step 4 — Fixing the N+1 Query Problem

- The original `UserOrdersView` fetched the user list with `User.objects.all()` and then called `user.orders.all()` inside a loop — this issued one extra database query per user, meaning 100 users caused 101 queries total (the N+1 problem).
- Fixed it by adding `prefetch_related('orders')` to the queryset: `User.objects.prefetch_related('orders').all()`. Django now fetches all users in one query and all related orders in a single second query, regardless of how many users exist.
- When the loop calls `user.orders.all()` after prefetching, Django returns the already-cached results instead of hitting the database again — so the total query count is always exactly 2.
- The response format was kept completely unchanged — same JSON structure, same field names (`id`, `name`, `email`, `age`, `orders`, `itemName`), same array shape. Only the internal query strategy changed.
- This kind of fix matters at scale: with 1000 users the old code issued 1001 queries; the fixed code still issues exactly 2, making the endpoint vastly more efficient under real load.
