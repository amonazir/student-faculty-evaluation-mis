# Generated by Django 4.1.2 on 2022-11-21 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stem", "0003_studentsessionsheet_registered"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="studentsessionsheet",
            name="registered",
        ),
        migrations.AddField(
            model_name="gradesheet",
            name="current",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="gradesheet",
            name="registered",
            field=models.BooleanField(default=False),
        ),
    ]
