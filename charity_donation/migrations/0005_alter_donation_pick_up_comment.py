# Generated by Django 3.2.9 on 2021-11-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity_donation', '0004_auto_20211111_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
