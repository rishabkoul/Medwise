# Generated by Django 3.1.3 on 2020-12-01 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0007_query_heading'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='title',
        ),
    ]
