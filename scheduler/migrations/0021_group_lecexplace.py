# Generated by Django 2.2 on 2019-05-21 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0020_auto_20190521_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='lecExPlace',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
    ]