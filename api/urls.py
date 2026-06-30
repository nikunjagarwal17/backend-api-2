from django.urls import path

from api.views.task_views import TaskListView, TaskDetailView
from api.views.user_views import UserSearchView, UserOrdersView

urlpatterns = [
    path('tasks', TaskListView.as_view()),
    path('tasks/<int:pk>', TaskDetailView.as_view()),
    path('users/search', UserSearchView.as_view()),
    path('users/orders', UserOrdersView.as_view()),
]
