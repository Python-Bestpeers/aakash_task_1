# Generated by Django 4.2.17 on 2024-12-10 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Task_Management_System", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.IntegerField(
                choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")],
                default=1,
            ),
        ),
    ]
