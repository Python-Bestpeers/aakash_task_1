# Generated by Django 4.2.17 on 2024-12-10 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Task_Management_System", "0002_alter_task_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.IntegerField(
                choices=[(1, "High"), (2, "Medium"), (3, "Low")], default=1
            ),
        ),
    ]
