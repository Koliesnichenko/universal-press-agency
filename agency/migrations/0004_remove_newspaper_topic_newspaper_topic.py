# Generated by Django 5.1.4 on 2025-01-05 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("agency", "0003_alter_redactor_years_of_experience"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="newspaper",
            name="topic",
        ),
        migrations.AddField(
            model_name="newspaper",
            name="topic",
            field=models.ManyToManyField(related_name="newspapers", to="agency.topic"),
        ),
    ]
