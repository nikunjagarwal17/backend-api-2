import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api.models import User


@method_decorator(csrf_exempt, name='dispatch')
class UserSearchView(View):
    def post(self, request):
        try:
            data = json.loads(request.body) if request.body else {}
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

        qs = User.objects.prefetch_related('orders').all()

        if data.get('name'):
            qs = qs.filter(name__icontains=data['name'])
        if data.get('email'):
            qs = qs.filter(email__icontains=data['email'])
        if data.get('minAge') is not None:
            qs = qs.filter(age__gte=data['minAge'])
        if data.get('maxAge') is not None:
            qs = qs.filter(age__lte=data['maxAge'])

        result = []
        for user in qs:
            result.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'age': user.age,
                'orders': [{'id': o.id, 'itemName': o.item_name} for o in user.orders.all()],
            })

        return JsonResponse(result, safe=False, status=200)


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
