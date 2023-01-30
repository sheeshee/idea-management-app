# Generated by Django 4.1.5 on 2023-01-30 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ideas", "0003_idea_embedding"),
    ]

    operations = [
        migrations.CreateModel(
            name="Similarity",
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
                ("score", models.FloatField(null=True)),
                ("ideas", models.ManyToManyField(to="ideas.idea")),
            ],
        ),
    ]
