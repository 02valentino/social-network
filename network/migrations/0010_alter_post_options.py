# Generated by Django 5.2.3 on 2025-07-08 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_alter_post_visibility'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': [('can_delete_any_post', 'Can delete any post')]},
        ),
    ]
