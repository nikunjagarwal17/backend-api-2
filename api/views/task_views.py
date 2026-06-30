import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import Task


def task_to_dict(task):
    return {'id': task.id, 'title': task.title}


@method_decorator(csrf_exempt, name='dispatch')
class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.all().order_by('id')
        return JsonResponse([task_to_dict(t) for t in tasks], safe=False, status=200)

    def post(self, request):
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

        title = body.get('title', '').strip()
        if not title:
            return JsonResponse({'error': 'title is required.'}, status=400)

        task = Task.objects.create(title=title)
        return JsonResponse(task_to_dict(task), status=200)


@method_decorator(csrf_exempt, name='dispatch')
class TaskDetailView(View):
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found.'}, status=404)
        return JsonResponse(task_to_dict(task), status=200)

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found.'}, status=404)

        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

        title = body.get('title', '').strip()
        if not title:
            return JsonResponse({'error': 'title is required.'}, status=400)

        task.title = title
        task.save()
        return JsonResponse(task_to_dict(task), status=200)

    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found.'}, status=404)
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully.'}, status=200)
