# Generated by Django 5.0.4 on 2024-07-29 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_courselist_labroom_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courselist',
            name='overrideSlotChange',
            field=models.BooleanField(default=False),
        ),
    ]
