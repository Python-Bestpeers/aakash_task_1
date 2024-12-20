# Generated by Django 4.2.17 on 2024-12-19 10:53

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Task_Management_System", "0006_alter_task_end_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[("Pending", "Pending"), ("Completed", "Completed")],
                        default="Pending",
                        max_length=50,
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sub_tasks",
                        to="Task_Management_System.task",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
