# Generated by Django 2.2.16 on 2022-04-08 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220407_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'админ'), ('moderator', 'модератор'), ('user', 'юзер')], default='user', max_length=200, null=True),
        ),
    ]
