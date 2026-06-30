import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import User
from api.serializers import UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserSearchView(View):
  def post(self, request):
    # TODO: Step3 - Search the users table with the conditions (name / email / minAge / maxAge)
    #               from the request body using AND conditions, and return the results
    #
    # Hint:
    #   data = json.loads(request.body)
    #   qs = User.objects.all()
    #   if data.get('name'):
    #       qs = qs.filter(name__icontains=data['name'])
    #   ...
    return JsonResponse({}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class UserOrdersView(View):
  def get(self, request):
    # TODO: Step4 - The implementation below has an N+1 problem. Resolve it using prefetch_related
    users = User.objects.all()
    result = []
    for user in users:
      orders = [{'id': o.id, 'itemName': o.item_name} for o in user.orders.all()]
      result.append({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'age': user.age,
        'orders': orders,
      })
    return JsonResponse(result, safe=False)