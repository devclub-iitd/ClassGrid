# Generated by Django 5.0.4 on 2024-12-23 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_notification_added_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='semesterCode',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]