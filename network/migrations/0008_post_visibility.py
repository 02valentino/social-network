# Generated by Django 5.2.3 on 2025-07-04 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_delete_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('public', 'Public'), ('friends', 'Friends only'), ('private', 'Private')], default='public', max_length=10),
        ),
    ]
