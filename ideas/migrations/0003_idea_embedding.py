# Generated by Django 4.1.5 on 2023-01-29 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ideas", "0002_idea_related"),
    ]

    operations = [
        migrations.AddField(
            model_name="idea",
            name="embedding",
            field=models.BinaryField(blank=True),
        ),
    ]