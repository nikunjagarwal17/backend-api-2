from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

  initial = True

  dependencies = []

  operations = [
    migrations.CreateModel(
      name='Task',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('title', models.CharField(max_length=255)),
      ],
      options={
        'db_table': 'tasks',
      },
    ),
    migrations.CreateModel(
      name='User',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('name', models.CharField(blank=True, max_length=100, null=True)),
        ('email', models.CharField(blank=True, max_length=200, null=True)),
        ('age', models.IntegerField(blank=True, null=True)),
      ],
      options={
        'db_table': 'users',
      },
    ),
    migrations.CreateModel(
      name='Order',
      fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('item_name', models.CharField(blank=True, max_length=200, null=True)),
        ('user', models.ForeignKey(
          blank=True,
          db_column='user_id',
          null=True,
          on_delete=django.db.models.deletion.SET_NULL,
          related_name='orders',
          to='api.user',
        )),
      ],
      options={
        'db_table': 'orders',
      },
    ),
  ]