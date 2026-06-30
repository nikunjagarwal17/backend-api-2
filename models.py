from django.db import models


class Task(models.Model):
  title = models.CharField(max_length=255)

  class Meta:
    db_table = 'tasks'


class User(models.Model):
  name = models.CharField(max_length=100, null=True, blank=True)
  email = models.CharField(max_length=200, null=True, blank=True)
  age = models.IntegerField(null=True, blank=True)

  class Meta:
    db_table = 'users'


class Order(models.Model):
  item_name = models.CharField(max_length=200, null=True, blank=True)
  user = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='orders',
    db_column='user_id',
  )

  class Meta:
    db_table = 'orders'