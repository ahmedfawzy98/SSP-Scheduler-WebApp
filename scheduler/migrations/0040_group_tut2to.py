# Generated by Django 2.2 on 2019-05-21 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0039_group_tut2from'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='tut2To',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]
