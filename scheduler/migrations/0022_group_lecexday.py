# Generated by Django 2.2 on 2019-05-21 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0021_group_lecexplace'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='lecExDay',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]