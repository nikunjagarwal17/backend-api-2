import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import Task
from api.serializers import TaskSerializer


@method_decorator(csrf_exempt, name='dispatch')
class TaskListView(View):
  def get(self, request):
    # TODO: Step1 - Retrieve and return all records in the tasks table, ordered by ID ascending
    return JsonResponse({}, status=404)

  def post(self, request):
    # TODO: Step1 - Read the title from the request body, create a new task, and return it
    return JsonResponse({}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class TaskDetailView(View):
  def get(self, request, pk):
    # TODO: Step1 - Retrieve and return the single task with the specified id
    return JsonResponse({}, status=404)

  def put(self, request, pk):
    # TODO: Step1 - Update the title of the task with the specified id and return it
    return JsonResponse({}, status=404)

  def delete(self, request, pk):
    # TODO: Step1 - Delete the task with the specified id (return 200)
    return JsonResponse({}, status=404)